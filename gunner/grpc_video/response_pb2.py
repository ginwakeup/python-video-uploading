# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_video/response.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19grpc_video/response.proto\x12\x13grpc_video.response\"T\n\x0cUploadStatus\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x33\n\x04\x63ode\x18\x02 \x01(\x0e\x32%.grpc_video.response.UploadStatusCode*3\n\x10UploadStatusCode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x06\n\x02OK\x10\x01\x12\n\n\x06\x46\x41ILED\x10\x02\x62\x06proto3')

_UPLOADSTATUSCODE = DESCRIPTOR.enum_types_by_name['UploadStatusCode']
UploadStatusCode = enum_type_wrapper.EnumTypeWrapper(_UPLOADSTATUSCODE)
UNKNOWN = 0
OK = 1
FAILED = 2


_UPLOADSTATUS = DESCRIPTOR.message_types_by_name['UploadStatus']
UploadStatus = _reflection.GeneratedProtocolMessageType('UploadStatus', (_message.Message,), {
  'DESCRIPTOR' : _UPLOADSTATUS,
  '__module__' : 'grpc_video.response_pb2'
  # @@protoc_insertion_point(class_scope:grpc_video.response.UploadStatus)
  })
_sym_db.RegisterMessage(UploadStatus)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _UPLOADSTATUSCODE._serialized_start=136
  _UPLOADSTATUSCODE._serialized_end=187
  _UPLOADSTATUS._serialized_start=50
  _UPLOADSTATUS._serialized_end=134
# @@protoc_insertion_point(module_scope)
