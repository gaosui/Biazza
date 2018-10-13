const express = require('express')
const app = express()

app.get('/preload', (req, res) => {
  console.log(req.query.id)
  res.set('Access-Control-Allow-Origin', '*')
  res.sendStatus(200)
})

app.listen(3000)