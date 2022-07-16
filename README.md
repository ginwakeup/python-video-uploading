# py_video_gunner

py_video_gunner is an experimental repository to try various video upload and streaming methods.

## Contained Experiments and Examples

### gRPC
The first example is written using opencv and gRPC.

gRPC is used to define a client and a server which communicate in unidirectional or bidirectional streaming to upload a video.

1. Unidirectional Streaming Example:
  - The gRPC client sends a stream of upload requests to get a final single response for the video upload.
  
1. Bidirectional Streaming Example:
  - The gRPC client sends a stream of upload requests to get a stream of responses. This is useful to control the status of the upload while it's happening. This is not possible with the first method, where the server only replies at the end of the stream.


### VidGear
VidGear is a High-Performance Video Processing Python Library.
https://github.com/abhiTronix/vidgear

In this approach VidGear takes care of the network layer, encoding and decoding.

We have less control over things, but the transfer is way faster and quicker to implement, since it also come with decoding/encoding logic behind the curtain.
