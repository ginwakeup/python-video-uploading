import grpc
import cv2
import pickle
import numpy as np
import base64

from gunner.grpc_video import service_pb2_grpc, data_pb2


channel = grpc.insecure_channel("localhost:50051")
stub = service_pb2_grpc.VideoUploadStub(channel)


cap = cv2.VideoCapture("test_video.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    if frame is None:
        break

    np.savez("original.npz", image=frame)
    image = cv2.imencode(".jpg", frame)
    image = image[1].tobytes()
    bi64 = base64.b64encode(image)

    response = stub.Upload(iter((data_pb2.Chunk(data=bi64),)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
