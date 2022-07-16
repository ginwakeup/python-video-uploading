"""This module shows a client example for the gRPC video upload server.
UploadMode is used to pickup what service to use (stream to stream or stream to response).
"""
import grpc
import cv2
import base64
import threading
import os
import logging

from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

import numpy as np

from py_video_gunner.grpc_stream.grpc_video import service_pb2_grpc, data_pb2, response_pb2
from py_video_gunner.grpc_stream import exceptions


logging.basicConfig(level=logging.INFO)


class UploadMode:
    """Used to switch between the two different services."""
    UNIDIR = 0
    BIDIR = 1


class VideoUploader:
    """Class used to extract and encode video frames, finally sending them through the gRPC API."""
    def __init__(self,
                 executor: ThreadPoolExecutor,
                 channel: grpc.Channel,
                 video_url: str,
                 mode: int):
        """
        Init.

        Args:
            executor: ThreadPoolExecutor object.
            channel: grpc channel to connect to the API server.
            video_url: input video file path as string.
            mode: from UploadMode, UNIDIR or BIDIR (0, 1).
        """
        self._executor = executor
        self._response_consumer = None
        self._mode = mode
        self._channel = channel
        self._queue = []
        self._video_url = video_url

        self._stub = service_pb2_grpc.VideoUploadStub(channel)

        # We store the upload status from the server for the BIDIR mode, so we can
        # eventually stop to upload files if the server errored during the previous frames
        # upload.
        self._upload_status = response_pb2.UNKNOWN

    def __enter__(self):
        """Simple context manager to open cv2 capture."""
        self._cap = cv2.VideoCapture(self._video_url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("Exit cv2.")

    def _on_upload_status(self, status: response_pb2.UploadStatus):
        """Callback for upload status changes.
        If the status returned from the server is responses_pb2.FAILED, an exception is thrown.

        Args:
            status: the server upload status.

        Raises:
            exceptions.UploadFailedException: when the server returns FAILED upload status.
        """
        self._upload_status = status
        if status == response_pb2.FAILED:
            raise exceptions.UploadFailedException("Upload FAILED received from server, stopping...")

    def _response_handler(self, response_iterator: Iterator[response_pb2.UploadStatus]):
        """This method takes care of handling the server responses in BIDIR mode.
        Every response is handled in a different thread.

        Args:
            response_iterator: response stream from the server.
        """
        try:
            for response in response_iterator:
                self._on_upload_status(response.code)

        except exceptions.UploadFailedException as error:
            logging.warning(error)

        except Exception as error:
            logging.error(error)

    @staticmethod
    def frame_to_grpc_chunk(frame: np.ndarray) -> data_pb2.Chunk:
        """Method that encodes cv2 frames to bytes and finally to a gRPC Chunk object.

        Args:
            frame: frame ndarray to upload.
        """
        image = cv2.imencode(".jpg", frame)
        image = image[1].tobytes()
        bi64 = base64.b64encode(image)

        return data_pb2.Chunk(data=bi64)

    def _queue_request(self, request: data_pb2.Chunk):
        """Appends a grpc request to a list cache. This is used in unidir mode.

        Args:
            request: data_pb2.Chunk request.
        """
        self._queue.append(request)

    def upload(self):
        """Main uplaod method.
        Based on selected mode, will use unidirectional or bidirectional upload services to upload a video to the gRPC
        server."""
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

        logging.info(self._stub.Upload(iter(self._queue)))

    def upload_bidir(self):
        """This method uploads the video using bidirectional streaming.
        A stream is sent to the server containing the video bytes, and a stream
        is returned during the calls."""
        while self._cap.isOpened() and self._upload_status != response_pb2.FAILED:
            ret, frame = self._cap.read()
            if not ret:
                break
            request = self.frame_to_grpc_chunk(frame)
            responses = self._stub.UploadBi(iter((request,)))

            # Consumption of the response is done on a separate thread.
            self._response_consumer = self._executor.submit(self._response_handler, responses)


def upload_video(executor: ThreadPoolExecutor, channel: grpc.Channel, video_url: str, mode: int):
    """Call this to start an upload.

    Args:
        executor: thread pool executor.
        channel: grpc channel.
        video_url: video path to upload.
        mode: unidirectional or bidirectional upload.
    """
    with VideoUploader(executor, channel, video_url, mode) as video_uploader:
        video_uploader.upload()


def run_client():
    test_video = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test_video.mp4")

    logging.info("Initializing Thread Pool Executor")
    executor = ThreadPoolExecutor()

    with grpc.insecure_channel("localhost:50051") as channel:
        logging.info("Opened gRPC channel.")
        future = executor.submit(upload_video, executor, channel, test_video, UploadMode.BIDIR)
        logging.info("Submitted upload thread execution.")
        future.result()


if __name__ == '__main__':
    run_client()
