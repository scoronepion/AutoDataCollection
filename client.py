import grpc
import AutoDataCollection_pb2
import AutoDataCollection_pb2_grpc

def get_txt2xml_result(stub):
    auth = AutoDataCollection_pb2.auth(
        username='lab106@ces@SHU',
        password='E0KF04JXjXFKwggGP#4yb@HX5LuyITyQFZitEmpiBsfCbZ^7'
    )
    result = stub.txt2xml(auth)
    print('received {result}'.format(
        result=result
    ))

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = AutoDataCollection_pb2_grpc.AutoDataCollectionStub(channel)
        get_txt2xml_result(stub)

if __name__ == '__main__':
    run()