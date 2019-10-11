const path = require('path')
const grpc = require('grpc')
const protoLoader = require('@grpc/proto-loader')
const PROTO_PATH = path.join(__dirname, '../AutoDataCollection.proto')

const username = 'lab106@ces@SHU'
const password = 'E0KF04JXjXFKwggGP#4yb@HX5LuyITyQFZitEmpiBsfCbZ^7'

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
const adc = grpc.loadPackageDefinition(packageDefinition).adc
const stub = new adc.AutoDataCollection('localhost:50051', grpc.credentials.createInsecure())
const auth = {
    username: username,
    password: password
}

function get_txt2xml_res(stub) {
    stub.txt2xml(auth, (err, res) => {
        if (err) {
            console.log("[txt2xml error] " + err)
        } else {
            let buff = new Buffer.from(res.result, 'base64')
            console.log("[txt2xml] received " + buff.toString('utf-8'))
        }
    })
}

function get_healthCheck_res(stub) {
    stub.healthCheck(auth, (err, res) => {
        if (err) {
            console.log("[health check error] " + err)
        } else {
            console.log('[health check] server status ' + res.status)
        }
    })
}

setInterval(get_healthCheck_res, 3000, stub)