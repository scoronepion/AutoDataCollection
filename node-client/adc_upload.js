const pgOpt = require('pg')
const axios = require('axios')
const auth = require('../data/auth')
const conStr = "postgres://postgres:lab106@192.168.1.19:5432/mdcs"

function connection_test() {
    let client = new pgOpt.Client(conStr)
    client.connect((err) => {
        if (err) {
            console.log('connect error:' + err.message)
            client.end()
            return
        }
        client.query('SELECT * FROM public."adcAutoTasks" WHERE uploadstatus=0',
            (err, res) => {
                if (err) {
                    console.log('query error:' + err.message)
                } else {
                    console.log(res.rows)
                }
                client.end()
            })
    })
}

// 依据 uploadstatus 获取 task 列表
function get_task_list(uploadstatus) {
    let client = new pgOpt.Client(conStr)
    return new Promise((resolve, reject) => {
        client.connect((err) => {
            if (err) {
                console.log('connect error:' + err.message)
                client.end()
                reject(err)
            }
            client.query(`SELECT * FROM public."adcAutoTasks" WHERE uploadstatus=${uploadstatus}`,
                (err, res) => {
                    if (err) {
                        client.end()
                        reject(err)
                    } else {
                        client.end()
                        resolve(res.rows)
                    }
                }
            )
        })
    })
}

// 依据 name 获取模板字符串
function get_template(name) {
    let client = new pgOpt.Client(conStr)
    return new Promise((resolve, reject) => {
        client.connect((err) => {
            if (err) {
                console.log('connect error:' + err.message)
                client.end()
                reject(err)
            }
            client.query(`SELECT * FROM public."adcXmlTemplates" WHERE name='${name}'`,
                (err, res) => {
                    if (err) {
                        client.end()
                        reject(err)
                    } else {
                        client.end()
                        resolve(res.rows)
                    }
                }
            )
        })
    })
}

function get_upload_status(taskid) {
    // 直接返回数字
    let client = new pgOpt.Client(conStr)
    return new Promise((resolve, reject) => {
        client.connect((err) => {
            if (err) {
                console.log('connect error:' + err.message)
                client.end()
                reject(err)
            }
            client.query(`SELECT uploadstatus FROM public."adcAutoTasks" WHERE taskid='${taskid}'`,
                (err, res) => {
                    if (err) {
                        client.end()
                        reject(err)
                    } else {
                        client.end()
                        resolve(res.rows[0].uploadstatus)
                    }
                }
            )
        })
    })
}

function set_upload_status(taskid, status) {
    let client = new pgOpt.Client(conStr)
    return new Promise((resolve, reject) => {
        client.connect(err => {
            if (err) {
                console.log('connect error:' + err.message)
                client.end()
                reject(err)
            }
            client.query(`UPDATE public."adcAutoTasks" SET uploadstatus=${status} WHERE taskid='${taskid}'`,
                (err, res) => {
                    if (err) {
                        client.end()
                        reject(false)
                    } else {
                        client.end()
                        resolve(true)
                    }
                }
            )
        })
    })
}

function check_and_set_uploadstatus() {
    // 检查所有 uploadstatus 为 -1 的任务，如果其中的设备 task status 全为 2 的话，表示该任务采集已完成，将 uploadstatus 改为 0（预备上传）
    return new Promise(async (resolve, reject) => {
        let taskList = await get_task_list(-1)
        for (let i in taskList) {
            let flag = false
            for (let key in taskList[i].status) {
                if (taskList[i].status[key] != 2) {
                    flag = true
                    break
                }
            }
            if (!flag) {
                // 此任务里，所有设备的 status 都为 2，因此可以准备上传
                await set_upload_status(taskList[i].taskid, 0)
            }
        }
        resolve(true)
    })
}

async function get_full_xml_string() {
    await check_and_set_uploadstatus()
    // 获取 uploadstatus 为 0 的任务
    let taskList = await get_task_list(0)
    for (let i in taskList) {
        // 每个 i 都代表一个任务
        let empty_template = await get_template(taskList[i].taskData.templateName)
        if (empty_template.length <= 0) {
            console.log("ID " + taskList[i].taskid + " 的模板名称不存在，请检查后重试")
            return
        }
        let xml_name = taskList[i].taskData.xmlName
        // console.log(template[0].content)
        // 大于 0，表示模板名称正确，已查询到模板
        // TODO：小于 0 的情况，模板名称错误，该任务上传状态应该为中止（uploadstatus）
        let mdcsid = ""
        let fullxml = ""

        // 填充上传日期 upload-date 标签
        let date = new RegExp("(.*<upload-date>)(</upload-date>.*)")
        let before = date.exec(empty_template[0].content)[1]
        let after = date.exec(empty_template[0].content)[2]
        let today = new Date()
        empty_template[0].content = before + today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate() + after

        // 填充 xml name
        let name = new RegExp("(.*<name>)(</name>.*)")
        before = name.exec(empty_template[0].content)[1]
        after = name.exec(empty_template[0].content)[2]
        empty_template[0].content = before + taskList[i].taskData.xmlName + after

        if (empty_template.length > 0) {
            // 提取出每一个设备的设备名称与对应的 xml 字符串，并与模板拼接在一起
            fullxml = empty_template[0].content
            mdcsid = empty_template[0].mdcsid
            let key_list = []
            for (let key in taskList[i].xmlcontents) {
                // key 为设备名称
                // let regExp = /(.*<deformation-processing>)(<\/deformation-processing>.*)/
                key_list.push(key)
                let reg = new RegExp("(.*<" + key + ">)(</" + key + ">.*)")
                before = reg.exec(fullxml)[1]
                after = reg.exec(fullxml)[2]
                fullxml = before + taskList[i].xmlcontents[key] + after
            }
        }
        // console.log(fullxml)
        // 上传前再检查 uploadstatus
        let uploadStatus = await get_upload_status(taskList[i].taskid)
        // 为 0，允许上传
        if (uploadStatus === 0) {
            // 上传进程
            axios({
                method: 'POST',
                url: 'http://matdata.shu.edu.cn/mdcs/rest/data/',
                data: {
                    "title": xml_name,
                    "template": mdcsid,
                    "xml_content": fullxml
                },
                auth: {
                    username: auth.username,
                    password: auth.password
                }
            }).then(async (res) => {
                // 上传成功，将 uploadstatus 置为 1
                let flag = await set_upload_status(taskList[i].taskid, 1)
                if (flag) {
                    console.log(new Date().toLocaleString() + ` id:${taskList[i].taskid} 上传成功, 上传状态已置为1`)
                } else {
                    console.log(new Date().toLocaleString() + ` id:${taskList[i].taskid} 上传成功，上传状态置1失败`)
                }
            }).catch(async (err) => {
                if (err.response.status === 500) {
                    let flag = await set_upload_status(taskList[i].taskid, 1)
                    if (flag) {
                        console.log(new Date().toLocaleString() + ` id:${taskList[i].taskid} 上传成功, 上传状态已置为1`)
                    } else {
                        console.log(new Date().toLocaleString() + ` id:${taskList[i].taskid} 上传成功，上传状态置1失败`)
                    }
                } else {
                    // 上传失败，将 uploadstatus 置为 2
                    let flag = await set_upload_status(taskList[i].taskid, 2)
                    if (flag) {
                        console.log(new Date().toLocaleString() + ` id:${taskList[i].taskid} 上传失败, 上传状态已置为2`)
                    } else {
                        console.log(new Date().toLocaleString() + ` id:${taskList[i].taskid} 上传失败, 上传状态置2失败`)
                    }
                    console.log(err)
                }
            })
        }
    }
    console.log(new Date().toLocaleString() + " 所有上传任务已完成，程序将于10秒后重新扫描。")
}

console.log("上传程序已启动...")
setInterval(get_full_xml_string, 10000)
// check_and_set_uploadstatus().then(res => {
//     console.log(res)
// }).catch(err => {
//     console.log(err)
// })  