# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: checkConnection.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'checkConnection.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63heckConnection.proto\x12\x0f\x63heckConnection\"\x1f\n\x0c\x63heckMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1d\n\ncheckReply\x12\x0f\n\x07message\x18\x01 \x01(\t2`\n\x0f\x63heckConnection\x12M\n\x0f\x43heckConnection\x12\x1d.checkConnection.checkMessage\x1a\x1b.checkConnection.checkReplyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'checkConnection_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CHECKMESSAGE']._serialized_start=42
  _globals['_CHECKMESSAGE']._serialized_end=73
  _globals['_CHECKREPLY']._serialized_start=75
  _globals['_CHECKREPLY']._serialized_end=104
  _globals['_CHECKCONNECTION']._serialized_start=106
  _globals['_CHECKCONNECTION']._serialized_end=202
# @@protoc_insertion_point(module_scope)
