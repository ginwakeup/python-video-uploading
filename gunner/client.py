import grpc
import cv2
import base64
import threading

from gunner.grpc_video import service_pb2_grpc, data_pb2

channel = grpc.insecure_channel("localhost:50051")
stub = service_pb2_grpc.VideoUploadStub(channel)

requests = []


def send_frame(frame, count):
    print(count)
    image = cv2.imencode(".jpg", frame)
    image = image[1].tobytes()
    bi64 = base64.b64encode(image)

    requests.append(data_pb2.Chunk(data=bi64),)




if __name__ == '__main__':
    cap = cv2.VideoCapture("test_video.mp4")

    count = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if frame is None:
            break
        thread = threading.Thread(target=send_frame, args=(frame, count))
        thread.start()
        thread.join()
        count += 1

    print(stub.Upload(iter(requests)))