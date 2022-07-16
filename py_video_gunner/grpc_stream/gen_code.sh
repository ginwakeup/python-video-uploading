#!/bin/bash


python -m grpc_tools.protoc\
 -I$PWD/schemas\
 --python_out=../../\
 $PWD/schemas/py_video_gunner/grpc_stream/grpc_video/*.proto\
 --grpc_python_out=../../

echo "" > ./grpc_video/__init__.py
