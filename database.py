import mysql.connector

config = {
    "user" : "root",
    "password" : "",
    "host" : "localhost",
    "database" : "sort_api"
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
