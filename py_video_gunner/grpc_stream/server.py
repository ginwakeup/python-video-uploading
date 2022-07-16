"""This module contains the example gRPC server for video upload.

The server offers two services:

- Upload: stream request (client) -> single response (server)
- UploadBi: stream request (client) -> stream response (server)

The only difference between the two is that the client can stop send files in the second method,
because the server can make it aware of any exception while it's still uploading the data.
"""
import grpc
import os
import cv2
import numpy as np
import base64
import logging

from concurrent import futures

from py_video_gunner.grpc_stream.grpc_video import service_pb2_grpc, response_pb2

logging.basicConfig(level=logging.INFO)


class VideoUploadServer(service_pb2_grpc.VideoUploadServicer):
    """Main service class."""
    def __init__(self):
        if not os.path.exists("output"):
            os.makedirs("output", exist_ok=True)

        self._count = 0
        self._upload_status = response_pb2.UNKNOWN

    @property
    def upload_status(self):
        return self._upload_status

    def _frame_to_file(self, frame: bytes):
        """Saves frame bytes to a file.
        The file naming is incremental, and they can be found in grc_stream/output folder.

        The output format is jpg.

        Args:
            frame: bytes making the frame.
        """
        try:
            b64e = base64.b64decode(frame)

            image = np.asarray(bytearray(b64e), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

            cv2.imwrite(f"output/output_{self._count}.jpg", image)
            self._count += 1

        except Exception as error:
            logging.error(f"Exception during upload, stopping. Error: {error}.")
            self._upload_status = response_pb2.FAILED

    def Upload(self, request_iterator, context) -> response_pb2.UploadStatus:
        """Unidirectional streaming upload example."""
        for request in request_iterator:
            self._frame_to_file(request.data)

        return response_pb2.UploadStatus(message="", code=response_pb2.OK)

    def UploadBi(self, request_iterator, context) -> response_pb2.UploadStatus:
        """Bidirectional Streaming Upload example."""
        self._upload_status = response_pb2.UNKNOWN

        for request in request_iterator:
            self._frame_to_file(request.data)

            if self._upload_status == response_pb2.FAILED:
                yield response_pb2.UploadStatus(message="", code=response_pb2.FAILED)
            else:
                self._upload_status = response_pb2.OK
                yield response_pb2.UploadStatus(message="", code=self._upload_status)


def serve():
    """Starts the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_VideoUploadServicer_to_server(VideoUploadServer(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("Starting gRPC Video Uploader Server.")
    server.start()
    server.wait_for_termination()

    while True:
        pass


if __name__ == '__main__':
    serve()
