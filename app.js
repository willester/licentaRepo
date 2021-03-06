const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')
const downloadImg = require('image-downloader')
const fs = require("fs")


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



app.post('/args',async (req, res, next) =>
{
    try{

        let generatedHashName = hashCodeGenerator(`${req.body.URL}`)
        console.log(generatedHashName)
        createDirectories(generatedHashName)
        downloadImage(req.body.URL,generatedHashName)

        exec(`python D:/Faculta/_LICENTA/_Aplicatie/pozeModel1SauBinaryModel/verificareModelCuFisierPython.py ${generatedHashName}`, (e,stdout, stderr) => {
            if(e instanceof Error){
                console.error(e)
                throw e
            } 
            console.log('stderr ',stderr)
            console.log('stdout ',stdout)
        })
        let returnJson
        setTimeout( ()=> 
        {fs.readFile(`C:/Users/Willestur/Desktop/test/${generatedHashName}/${generatedHashName}.json`, 'utf8', (err, data) => {
          if (err) {
              console.log(`Error reading file from disk: ${err}`);
          } else {
            returnJson = JSON.parse(data);
            res.status(200).json(returnJson)
          }
      })},30000)
    }
    catch(error)
    {
        next(error)
    }
})

app.post('/rediagnose',async (req, res, next) =>
{
    try{
        let photoFolderPath = req.body.Path
        console.log(photoFolderPath)
        exec(`python D:/Faculta/_LICENTA/_Aplicatie/pozeModel1SauBinaryModel/verificareModelClase.py ${photoFolderPath}`, (e,stdout, stderr) => {
            if(e instanceof Error){
                console.error(e)
                throw e
            } 
            console.log('stderr ',stderr)
            console.log('stdout ',stdout)
        })
        let returnJson
        setTimeout( ()=> 
        {fs.readFile(`C:/Users/Willestur/Desktop/test/${photoFolderPath}/${photoFolderPath}Rediagnose.json`, 'utf8', (err, data) => {
          if (err) {
              console.log(`Error reading file from disk: ${err}`);
          } else { 
            returnJson = JSON.parse(data);
            res.status(200).json(returnJson)
          }   
      })},30000)
    }
    catch(error)
    {
        next(error)
    }
})

function downloadImage(URL,hashName)
{
    const downloadDetails = {
        url: URL,
        dest: `C:/Users/Willestur/Desktop/test/${hashName}/folderSecundar/${hashName}.png`
    }
    downloadImg.image(downloadDetails).then(({ filename }) => {
        console.log('Saved to', filename)  
      })
    .catch((err) => console.error(err))
}

function createDirectories(URL)
{
    fs.mkdir( `C:/Users/Willestur/Desktop/test/${URL}`, (error) => {
        if (error) {
          console.log(error);
        } 
      });
      fs.mkdir( `C:/Users/Willestur/Desktop/test/${URL}/folderSecundar`, (error) => {
        if (error) {
          console.log(error);
        } 
      });
}

const hashCodeGenerator = function(URL) {
    let hash = 0
    for (let i = 0; i < URL.length; i++) {
      let char   = URL.charCodeAt(i)
      hash  = Math.round((((hash << 5) + Math.floor((Math.random() * 10) + 1) - hash*0.5) + char)/2)
    }
    return hash;
  };


app.use(express.static('./public')).get('*',function (req,res) {
        res.sendFile('./index.html');
        })

module.exports = app