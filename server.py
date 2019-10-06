from concurrent import futures
import time
import grpc
import utils
import AutoDataCollection_pb2
import AutoDataCollection_pb2_grpc

default_usr = 'lab106@ces@SHU'
default_pwd = 'E0KF04JXjXFKwggGP#4yb@HX5LuyITyQFZitEmpiBsfCbZ^7'

class AutoDataCollection(AutoDataCollection_pb2_grpc.AutoDataCollectionServicer):
    def txt2xml(self, request, context):
        if request.username == default_usr and \
            request.password == default_pwd:
            return AutoDataCollection_pb2.resultXML(result=utils.txt2xml(incremental_read=False))
        else:
            return AutoDataCollection_pb2.resultXML(result='')

    def csv2xml(self, request, context):
        if request.username == default_usr and \
            request.password == default_pwd:
            return AutoDataCollection_pb2.resultXML(result=utils.csv2xml(incremental_read=False))
        else:
            return AutoDataCollection_pb2.resultXML(result='')

def run():
    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    AutoDataCollection_pb2_grpc.add_AutoDataCollectionServicer_to_server(AutoDataCollection(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run()