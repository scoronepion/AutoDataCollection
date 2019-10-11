# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import AutoDataCollection_pb2 as AutoDataCollection__pb2


class AutoDataCollectionStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.healthCheck = channel.unary_unary(
        '/adc.AutoDataCollection/healthCheck',
        request_serializer=AutoDataCollection__pb2.auth.SerializeToString,
        response_deserializer=AutoDataCollection__pb2.healthCheckRes.FromString,
        )
    self.txt2xml = channel.unary_unary(
        '/adc.AutoDataCollection/txt2xml',
        request_serializer=AutoDataCollection__pb2.auth.SerializeToString,
        response_deserializer=AutoDataCollection__pb2.resultXML.FromString,
        )
    self.csv2xml = channel.unary_unary(
        '/adc.AutoDataCollection/csv2xml',
        request_serializer=AutoDataCollection__pb2.auth.SerializeToString,
        response_deserializer=AutoDataCollection__pb2.resultXML.FromString,
        )
    self.mysql2xml = channel.unary_unary(
        '/adc.AutoDataCollection/mysql2xml',
        request_serializer=AutoDataCollection__pb2.auth.SerializeToString,
        response_deserializer=AutoDataCollection__pb2.resultXML.FromString,
        )


class AutoDataCollectionServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def healthCheck(self, request, context):
    """服务端心跳检测
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def txt2xml(self, request, context):
    """客户端发起请求，服务端返回 xml 字符串
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def csv2xml(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def mysql2xml(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AutoDataCollectionServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'healthCheck': grpc.unary_unary_rpc_method_handler(
          servicer.healthCheck,
          request_deserializer=AutoDataCollection__pb2.auth.FromString,
          response_serializer=AutoDataCollection__pb2.healthCheckRes.SerializeToString,
      ),
      'txt2xml': grpc.unary_unary_rpc_method_handler(
          servicer.txt2xml,
          request_deserializer=AutoDataCollection__pb2.auth.FromString,
          response_serializer=AutoDataCollection__pb2.resultXML.SerializeToString,
      ),
      'csv2xml': grpc.unary_unary_rpc_method_handler(
          servicer.csv2xml,
          request_deserializer=AutoDataCollection__pb2.auth.FromString,
          response_serializer=AutoDataCollection__pb2.resultXML.SerializeToString,
      ),
      'mysql2xml': grpc.unary_unary_rpc_method_handler(
          servicer.mysql2xml,
          request_deserializer=AutoDataCollection__pb2.auth.FromString,
          response_serializer=AutoDataCollection__pb2.resultXML.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'adc.AutoDataCollection', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))