#!/bin/bash


python -m grpc_tools.protoc\
 -I$PWD/schemas\
 --python_out=../gunner/grpc_stream\
 $PWD/schemas/grpc_video/*.proto\
 --grpc_python_out=../gunner/grpc_stream/

echo "" > ../gunner/grpc_stream/grpc_video/__init__.py
