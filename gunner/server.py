import grpc
import os
import cv2
import pickle

from concurrent import futures

from gunner.grpc_video import service_pb2_grpc, response_pb2


FILE_OUTPUT = 'output.mp4'


class VideoUploadServer(service_pb2_grpc.VideoUploadServicer):
    def __init__(self):
        if os.path.isfile(FILE_OUTPUT):
            os.remove(FILE_OUTPUT)

    def Upload(self, request_iterator, context):
        for request in request_iterator:
            frame = pickle.loads(request.data)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        response = response_pb2.UploadStatus(message="", code=response_pb2.OK)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_VideoUploadServicer_to_server(VideoUploadServer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

    while True:
        pass


if __name__ == '__main__':
    serve()
