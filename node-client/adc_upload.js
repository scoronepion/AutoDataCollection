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

// 获取 task 列表
function get_task_list() {
    let client = new pgOpt.Client(conStr)
    return new Promise((resolve, reject) => {
        client.connect((err) => {
            if (err) {
                console.log('connect error:' + err.message)
                client.end()
                reject(err)
            }
            // TODO：这里还要考虑 status 的情况，必须是所有的 status 都为 2 才能 resolve
            client.query('SELECT * FROM public."adcAutoTasks" WHERE uploadstatus=0',
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

async function get_full_xml_string() {
    let taskList = await get_task_list()
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
        // 首先填充上传日期 upload-date 标签
        let date = new RegExp("(.*<upload-date>)(</upload-date>.*)")
        let before = date.exec(empty_template[0].content)[1]
        let after = date.exec(empty_template[0].content)[2]
        let today = new Date()
        empty_template[0].content = before + today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate() + after
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
        console.log(fullxml)
        // axios({
        //     method: 'POST',
        //     url: 'http://matdata.shu.edu.cn/mdcs/rest/data/',
        //     data: {
        //         "title": xml_name,
        //         "template": mdcsid,
        //         "xml_content": fullxml
        //     },
        //     auth: {
        //         username: auth.username,
        //         password: auth.password
        //     }
        // }).then(res => {
        //     console.log(res)
        // }).catch(err => {
        //     console.log(err)
        // })
    }
}

get_full_xml_string()