const path = require('path')
const grpc = require('grpc')
const protoLoader = require('@grpc/proto-loader')
const PROTO_PATH = path.join(__dirname, '../AutoDataCollection.proto')

const packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true
    }
)
const protoDescriptor = grpc.loadPackageDefinition(packageDefinition)
const adc = protoDescriptor.adc
const stub = new adc.AutoDataCollection('localhost:50051', grpc.credentials.createInsecure())