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
const autoParam = {
    taskid: '0e7759c1fc65d7581c72a3',
    username: username,
    password: password,
    startid: 1,
    endid: 1
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
    // 设置延时 1s 自动关闭连接，否则前台响应会卡住
    // 但是若服务端网络环境不好，则可适当放宽限制，以免出现误判
    let deadline = new Date();
    deadline.setSeconds(deadline.getSeconds() + 1);
    stub.healthCheck(auth, {deadline: deadline}, (err, res) => {
        if (err) {
            console.log("[health check error] " + err)
        } else {
            console.log('[health check] server status ' + res.status)
        }
    })
}

function submit_auto_task(stub) {
    stub.autoTxt2xml(autoParam, (err, res) => {
        if (err) {
            console.log("[submit_auto_task error] " + err)
        } else {
            console.log('[submit_auto_task] server status ' + res.status)
        }
    })
}

setInterval(get_healthCheck_res, 3000, stub)
// submit_auto_task(stub)