const axios = require('axios')
const auth = require('../data/auth')
const url = 'http://matdata.shu.edu.cn/mdcs/data?id=5db3dfcb69af1a332e4999fe'
const regExp = /.*(matdata.shu.edu.cn).*/
console.log(Date.now())

// const regExp = /.*id=(.*)/
// let id = regExp.exec(url)[1]

// axios({
//     method: 'GET',
//     url: `http://matdata.shu.edu.cn/mdcs/rest/data/download/${id}`,
//     auth: {
//         username: auth.username,
//         password: auth.password
//     }
// }).then(res => {
//     console.log(res.data)
// }).catch(err => {
//     console.log(err)
// })