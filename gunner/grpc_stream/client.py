import grpc
import cv2
import base64
import threading
import os
import logging

from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

from gunner.grpc_stream.grpc_video import service_pb2_grpc, data_pb2, response_pb2


class UploadMode:
    UNIDIR = 0
    BIDIR = 1


LOGGER = logging.getLogger(__name__)


class VideoUploader:
    def __init__(self, executor, channel, video_url, mode: int):
        self._executor = executor
        self._response_consumer = None
        self._mode = mode
        self._channel = channel
        self._queue = []
        self._video_url = video_url

        self._upload_failed = threading.Event()

        self._stub = service_pb2_grpc.VideoUploadStub(channel)

    def __enter__(self):
        self._cap = cv2.VideoCapture(self._video_url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOGGER.info("Exit cv2.")

    def _on_upload_status(self, status):
        LOGGER.info(f"Upload status: {LOGGER.info(status)}")
        if status == response_pb2.FAILED:
            self._upload_failed.set()

    def _response_hanlder(self,
                          response_iterator: Iterator[response_pb2.UploadStatus]):
        try:
            for response in response_iterator:
                self._on_upload_status(response.code)

        except Exception as error:
            LOGGER.error(error)
            raise

    @staticmethod
    def frame_to_grpc_chunk(frame):
        image = cv2.imencode(".jpg", frame)
        image = image[1].tobytes()
        bi64 = base64.b64encode(image)

        return data_pb2.Chunk(data=bi64)

    def _queue_request(self, request):
        self._queue.append(request)

    def upload(self):
        if self._mode == UploadMode.UNIDIR:
            self.upload_unidir()
        else:
            self.upload_bidir()

    def upload_unidir(self):
        """This method uploads the video using unidirectional streaming.
        A stream is sent to the server containing the video bytes, and a single response
        is returned at the end."""
        count = 0
        while self._cap.isOpened():
            ret, frame = self._cap.read()
            if frame is None:
                break
            thread = threading.Thread(target=self._queue_request, args=(self.frame_to_grpc_chunk(frame),))
            thread.start()
            thread.join()
            count += 1

        print(self._stub.Upload(iter(self._queue)))

    def upload_bidir(self):
        """This method uploads the video using bidirectional streaming.
        A stream is sent to the server containing the video bytes, and a stream
        is returned during the calls."""
        while self._cap.isOpened():
            ret, frame = self._cap.read()
            if not ret:
                break
            request = self.frame_to_grpc_chunk(frame)
            responses = self._stub.UploadBi(iter((request,)))

            # Consumption of the response is done on a separate thread.
            self._response_consumer = self._executor.submit(self._response_hanlder, responses)


def upload_video(executor: ThreadPoolExecutor, channel: grpc.Channel, video_url: str, mode: int):
    with VideoUploader(executor, channel, video_url, mode) as video_uploader:
        video_uploader.upload()


if __name__ == '__main__':
    video_url = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_video.mp4")

    LOGGER.info("Initializing Thread Pool Executor")
    executor = ThreadPoolExecutor()

    with grpc.insecure_channel("localhost:50051") as channel:
        LOGGER.info("Opened gRPC channel.")
        future = executor.submit(upload_video, executor, channel, video_url, UploadMode.BIDIR)
        LOGGER.info("Submitted upload thread execution.")
        future.result()
