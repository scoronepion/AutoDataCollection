from concurrent import futures
import time
import grpc
import utils
import base64
import time
import AutoDataCollection_pb2
import AutoDataCollection_pb2_grpc

default_usr = 'lab106@ces@SHU'
default_pwd = 'E0KF04JXjXFKwggGP#4yb@HX5LuyITyQFZitEmpiBsfCbZ^7'

class AutoDataCollection(AutoDataCollection_pb2_grpc.AutoDataCollectionServicer):
    # 心跳检测
    def healthCheck(self, request, context):
        if request.username == default_usr and \
            request.password == default_pwd:
            localtime = time.asctime(time.localtime(time.time()))
            print(localtime + ' Health checking status: online')
            return AutoDataCollection_pb2.healthCheckRes(status='online')
        else:
            return AutoDataCollection_pb2.healthCheckRes(status='Auth Failed')

    # 避免中文编码问题，数据返回时同一进行 base64 编码
    def txt2xml(self, request, context):
        if request.username == default_usr and \
            request.password == default_pwd:
            res = base64.b64encode(utils.txt2xml(incremental_read=False).encode('utf-8'))
            return AutoDataCollection_pb2.resultXML(result=res)
        else:
            return AutoDataCollection_pb2.resultXML(result='Auth Failed')

    def csv2xml(self, request, context):
        if request.username == default_usr and \
            request.password == default_pwd:
            res = base64.b64encode(utils.csv2xml(incremental_read=False).encode('utf-8'))
            return AutoDataCollection_pb2.resultXML(result=res)
        else:
            return AutoDataCollection_pb2.resultXML(result='Auth Failed')

    def mysql2xml(self, request, context):
        if request.username == default_usr and \
            request.password == default_pwd:
            res = base64.b64encode(utils.read_mysql().encode('utf-8'))
            return AutoDataCollection_pb2.resultXML(result=res)
        else:
            return AutoDataCollection_pb2.resultXML(result='Auth Failed')

    def autoTxt2xml(self, request, context):
        if request.username == default_usr and \
            request.password == default_pwd:
            res = "success"
            return AutoDataCollection_pb2.autoTaskStatus(status=res)
        else:
            return AutoDataCollection_pb2.autoTaskStatus(status='Auth Failed')

def run():
    # 启动 rpc 服务
    # with open('../cert/server.key', 'rb') as f:
    #     private_key = f.read()
    # with open('../cert/server.crt', 'rb') as f:
    #     certificate_chain = f.read()
    # server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    AutoDataCollection_pb2_grpc.add_AutoDataCollectionServicer_to_server(AutoDataCollection(), server)
    # server.add_secure_port('localhost:50051', server_credentials)
    server.add_insecure_port('localhost:50051')
    server.start()
    print('service start...')
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run()