const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const knex = require('knex');

const config = require('./config')
const getSchedule = require('./controllers/schedule');
const db = knex({
  client: 'pg',
  connection: config.config.development.database
});

const app = express();

app.use(bodyParser.json());
app.use(cors());

app.get('/get', (req, res) => { getSchedule.getSchedule(req, res, db) })

app.listen(3000, () => {
  console.log('app is running on port 3000');
})