# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: py_video_gunner/grpc_stream/grpc_video/service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from py_video_upload.grpc_stream.grpc_video import data_pb2 as py__video__gunner_dot_grpc__stream_dot_grpc__video_dot_data__pb2
from py_video_upload.grpc_stream.grpc_video import response_pb2 as py__video__gunner_dot_grpc__stream_dot_grpc__video_dot_response__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4py_video_gunner/grpc_stream/grpc_video/service.proto\x12.py_video_gunner.grpc_stream.grpc_video.service\x1a\x31py_video_gunner/grpc_stream/grpc_video/data.proto\x1a\x35py_video_gunner/grpc_stream/grpc_video/response.proto2\x94\x02\n\x0bVideoUpload\x12\x7f\n\x06Upload\x12\x32.py_video_gunner.grpc_stream.grpc_video.data.Chunk\x1a=.py_video_gunner.grpc_stream.grpc_video.response.UploadStatus\"\x00(\x01\x12\x83\x01\n\x08UploadBi\x12\x32.py_video_gunner.grpc_stream.grpc_video.data.Chunk\x1a=.py_video_gunner.grpc_stream.grpc_video.response.UploadStatus\"\x00(\x01\x30\x01\x62\x06proto3')



_VIDEOUPLOAD = DESCRIPTOR.services_by_name['VideoUpload']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _VIDEOUPLOAD._serialized_start=211
  _VIDEOUPLOAD._serialized_end=487
# @@protoc_insertion_point(module_scope)
