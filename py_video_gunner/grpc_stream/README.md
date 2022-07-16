# gRPC 

This example uses gRPC for video uploading.

To run it:

- Run `grpc_stream\server.py`
- Run `grpc_stream\client.py'
- Frames will be saved in `grpc_video\output.`
  - There's still some work in generating video from the frames to be done here, but it's easily
  achievable with cv2 once you have the frames.
