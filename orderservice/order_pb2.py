# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: order.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'order.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x0corderservice\"3\n\x0cOrderRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x12\n\nproduct_id\x18\x02 \x01(\x05\" \n\rOrderResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2V\n\x0cOrderService\x12\x46\n\x0b\x43reateOrder\x12\x1a.orderservice.OrderRequest\x1a\x1b.orderservice.OrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDERREQUEST']._serialized_start=29
  _globals['_ORDERREQUEST']._serialized_end=80
  _globals['_ORDERRESPONSE']._serialized_start=82
  _globals['_ORDERRESPONSE']._serialized_end=114
  _globals['_ORDERSERVICE']._serialized_start=116
  _globals['_ORDERSERVICE']._serialized_end=202
# @@protoc_insertion_point(module_scope)
