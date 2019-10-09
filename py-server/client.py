import grpc
import base64
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

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = AutoDataCollection_pb2_grpc.AutoDataCollectionStub(channel)
        get_txt2xml_result(stub)
        get_csv2xml_result(stub)
        # get_mysql2xml_result(stub)

if __name__ == '__main__':
    run()