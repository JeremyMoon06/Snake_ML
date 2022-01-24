/* Refer to README.md */
/* Set up connection to database within configConnection.js */
const express = require('express');
const bodyParser = require('body-parser');
const connection = require('./configConnection').connection;
const port = 3001;

const app = express();
const cors = require('cors');
app.use(cors());
app.use(bodyParser.json());

/* Query all database iterations for gameplay lists to port 3001 */
connection.connect();
for(let i = 1; i <= 100; i++){
  let url = `/get/${i}`;
  app.get(url, (req, res) => {
    connection.query(`SELECT * FROM Gameplay_results WHERE database_iteration=${i}`, function (err, result)
    {res.send(result[0].gameplay_list);}
  )})
}

app.listen(port, () => console.log(`Listening to port ${port}`));