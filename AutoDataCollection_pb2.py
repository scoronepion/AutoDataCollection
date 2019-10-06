# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AutoDataCollection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='AutoDataCollection.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x18\x41utoDataCollection.proto\"*\n\x04\x61uth\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1b\n\tresultXML\x12\x0e\n\x06result\x18\x01 \x01(\t2T\n\x12\x41utoDataCollection\x12\x1e\n\x07txt2xml\x12\x05.auth\x1a\n.resultXML\"\x00\x12\x1e\n\x07\x63sv2xml\x12\x05.auth\x1a\n.resultXML\"\x00\x62\x06proto3')
)




_AUTH = _descriptor.Descriptor(
  name='auth',
  full_name='auth',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='auth.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='auth.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=70,
)


_RESULTXML = _descriptor.Descriptor(
  name='resultXML',
  full_name='resultXML',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='resultXML.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=99,
)

DESCRIPTOR.message_types_by_name['auth'] = _AUTH
DESCRIPTOR.message_types_by_name['resultXML'] = _RESULTXML
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

auth = _reflection.GeneratedProtocolMessageType('auth', (_message.Message,), {
  'DESCRIPTOR' : _AUTH,
  '__module__' : 'AutoDataCollection_pb2'
  # @@protoc_insertion_point(class_scope:auth)
  })
_sym_db.RegisterMessage(auth)

resultXML = _reflection.GeneratedProtocolMessageType('resultXML', (_message.Message,), {
  'DESCRIPTOR' : _RESULTXML,
  '__module__' : 'AutoDataCollection_pb2'
  # @@protoc_insertion_point(class_scope:resultXML)
  })
_sym_db.RegisterMessage(resultXML)



_AUTODATACOLLECTION = _descriptor.ServiceDescriptor(
  name='AutoDataCollection',
  full_name='AutoDataCollection',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=101,
  serialized_end=185,
  methods=[
  _descriptor.MethodDescriptor(
    name='txt2xml',
    full_name='AutoDataCollection.txt2xml',
    index=0,
    containing_service=None,
    input_type=_AUTH,
    output_type=_RESULTXML,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='csv2xml',
    full_name='AutoDataCollection.csv2xml',
    index=1,
    containing_service=None,
    input_type=_AUTH,
    output_type=_RESULTXML,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUTODATACOLLECTION)

DESCRIPTOR.services_by_name['AutoDataCollection'] = _AUTODATACOLLECTION

# @@protoc_insertion_point(module_scope)
