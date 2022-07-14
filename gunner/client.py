import grpc
import cv2
import pickle

from gunner.grpc_video import service_pb2_grpc, data_pb2


channel = grpc.insecure_channel("localhost:50051")
stub = service_pb2_grpc.VideoUploadStub(channel)


cap = cv2.VideoCapture("test_video.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    if frame is None:
        break

    frame = pickle.dumps(frame)

    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)


    response = stub.Upload(iter((data_pb2.Chunk(data=frame),)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
