const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')
const downloadImg = require('image-downloader')


const exec = require('child_process').exec

const app = express()
app.use(cors())
app.use(bodyParser.json())


app.get('/test', async (req, res, next) => {
    try {
      res.status(201).json({ message: 'merge' })
    } catch (err) {
      next(err)
    }
})

app.get('/args',async (req, res, next) =>
{
    try{
        exec('python C:/Users/Willestur/Desktop/test/argTest.py argumentTest', (e,stdout, stderr) => {
            if(e instanceof Error){
                console.error(e)
                throw e
            } 
            console.log('stderr ',stderr)
            console.log('stdout ',stdout)
           
        })
        setTimeout( ()=> 
        {res.status(200).json({message: 'mergePitonu'})},3000)
        
    }
    catch(error)
    {
        next(error)
    }
})

app.post('/py',async (req, res, next) =>
{
    try{
        exec('python E:/Faculta/_LICENTA/_Aplicatie/pozeModel1SauBinaryModel/verificareModelCuFisierPython.py', (e,stdout, stderr) => {
            if(e instanceof Error){
                console.error(e)
                throw e
            } 
            console.log('stderr ',stderr)
            console.log('stdout ',stdout)
           
        })
        setTimeout( ()=> 
        {res.status(200).json({message: 'mergePitonu'})},300000)
        
    }
    catch(error)
    {
        next(error)
    }
})


app.use(express.static('./public')).get('*',function (req,res) {
        res.sendfile('./index.html');
        })

module.exports = app