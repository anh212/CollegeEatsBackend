const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const knex = require('knex');

const config = require('./config')
const getSchedule = require('./controllers/schedule');
const getLocations = require('./controllers/locations');

const db = knex({
  client: 'pg',
  connection: config.config.development.database
});

const app = express();

app.use(bodyParser.json());
app.use(cors());

//Need to send school name and name of dining location
app.get('/getSchedule/:schoolName/:diningName', (req, res) => { getSchedule.getSchedule(req, res, db) });
app.get('/getLocations/:schoolName', (req, res) => { getLocations.getLocations(req, res, db)});

app.listen(3000, () => {
  console.log('app is running on port 3000');
})