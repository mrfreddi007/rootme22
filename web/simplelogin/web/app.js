var express = require('express');
var path = require('path');
var mysql = require('mysql');


var connection = mysql.createConnection({
    host: "127.0.0.1",
    user: "root",
    password: "dec369de7fbce7b10e640d88315a1813",
    database: "challenge",
});


var app = express();
app.use(express.json())


app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'login.html'));
});


app.post('/auth', function (req, res) {
    if (!req.is('application/json')) {
        res.send('Data must be send in JSON!', 400);

    } else {
        var credentials = req.body;

        if (typeof credentials.user === "object") {
            res.send("Attack detected!", 400);
        } else if (typeof credentials.password === "object") {
            res.send("Attack detected!", 400);

        } else {
            credentials = Object.assign({"flag": "RM{fake-flag}"}, credentials)

            var sql = "SELECT ? AS FLAG FROM users WHERE user = ? AND password = ?";
            connection.query(
                sql,
                [credentials.flag, credentials.user, credentials.password],
                (e, result, fields) => {
                    if (result.length > 0) {
                        res.send(result[0]["FLAG"], 200);
                    } else {
                        res.send("Invalid credentials!");
                    }
                }
            );
        }
    }
});


var server = app.listen(process.env.PORT || 3000, function () {
    console.log('Listening on port ' + server.address().port);
});
