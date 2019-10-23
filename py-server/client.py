import grpc
import base64
import time
import threading as thd
import AutoDataCollection_pb2
import AutoDataCollection_pb2_grpc

default_usr = 'lab106@ces@SHU'
default_pwd = 'E0KF04JXjXFKwggGP#4yb@HX5LuyITyQFZitEmpiBsfCbZ^7'

def get_txt2xml_result(stub):
    auth = AutoDataCollection_pb2.auth(
        username=default_usr,
        password=default_pwd
    )
    resultXML = stub.txt2xml(auth)
    print('[txt] received {result}'.format(
        result=base64.b64decode(resultXML.result).decode(encoding='utf-8')
    ))

def get_csv2xml_result(stub):
    auth = AutoDataCollection_pb2.auth(
        username=default_usr,
        password=default_pwd
    )
    resultXML = stub.csv2xml(auth)
    print('[csv] received {result}'.format(
        result=base64.b64decode(resultXML.result).decode(encoding='utf-8')
    ))

def get_mysql2xml_result(stub):
    auth = AutoDataCollection_pb2.auth(
        username=default_usr,
        password=default_pwd
    )
    resultXML = stub.mysql2xml(auth)
    print('[mysql] received {result}'.format(
        result=base64.b64decode(resultXML.result).decode(encoding='utf-8')
    ))

def get_healthCheck(stub):
    auth = AutoDataCollection_pb2.auth(
        username=default_usr,
        password=default_pwd
    )
    status = stub.healthCheck(auth).status
    print('received health check result: ' + status)

def get_autoTaskStatus(stub):
    param = AutoDataCollection_pb2.autoTaskParam(
        taskid="b5b5e6b99e699c40c61ad8",
        username=default_usr,
        password=default_pwd,
        startid = 1,
        endid = 6
    )
    status = stub.autoTxt2xml(param).status
    print('received auto txt2xml result: ' + status)

def run():
    # with open('../cert/server.crt', 'rb') as f:
    #     trusted_certs = f.read()
    # credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    # with grpc.secure_channel('localhost:50051', credentials) as channel:
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = AutoDataCollection_pb2_grpc.AutoDataCollectionStub(channel)
        # get_txt2xml_result(stub)
        get_autoTaskStatus(stub)
        # get_csv2xml_result(stub)
        # 每隔 3 秒检测服务在线情况
        # for _ in range(10):
        #     get_healthCheck(stub)
        #     time.sleep(3)
        # thd.Timer(3, get_healthCheck(stub)).start()     # 每隔 3 秒检测服务在线情况
        # get_mysql2xml_result(stub)

if __name__ == '__main__':
    run()