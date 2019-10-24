const pgOpt = require('pg')
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
            client.query(`SELECT content FROM public."adcXmlTemplates" WHERE name='${name}'`,
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
        let template = await get_template(taskList[i].taskData.templateName)
        // console.log(template[0].content)
        // 大于 0，表示有数据
        // TODO：小于 0 的情况
        if (template.length > 0) {
            // 提取出每一个设备的设备名称与对应的 xml 字符串，并与模板拼接在一起
            for (let key in taskList[i].xmlcontents) {
                // key 为设备名称
                // let regExp = /(.*<deformation-processing>)(<\/deformation-processing>.*)/
                let reg = new RegExp("(.*<" + key + ">)(</" + key + ">.*)")
                let front = reg.exec(template[0].content)[1]
                let end = reg.exec(template[0].content)[2]
                let fullxml = front + taskList[i].xmlcontents[key] + end
                console.log(fullxml)
            }
        }
    }
}

get_full_xml_string()