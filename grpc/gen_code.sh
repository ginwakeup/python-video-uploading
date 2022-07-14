#!/bin/bash


python -m grpc_tools.protoc\
 -I$PWD/schemas\
 --python_out=../gunner\
 $PWD/schemas/grpc_video/*.proto\
 --grpc_python_out=../gunner/

echo "" > ../gunner/grpc_video/__init__.py
