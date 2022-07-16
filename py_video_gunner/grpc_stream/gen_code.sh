#!/bin/bash


python -m grpc_tools.protoc\
 -I$PWD/schemas\
 --python_out=./\
 $PWD/schemas/grpc_video/*.proto\
 --grpc_python_out=./

echo "" > ../grpc_video/__init__.py
