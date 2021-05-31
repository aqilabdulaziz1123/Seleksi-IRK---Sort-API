import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv()
import os

database = mysql.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
)
database.autocommit = True

cursor = database.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS SortAPI")
cursor.execute("USE SortAPI")

cursor.execute("CREATE TABLE IF NOT EXISTS sorts (ID INT AUTO_INCREMENT PRIMARY KEY, Waktu TIMESTAMP, Algoritma VARCHAR(9) DEFAULT 'selection', Result BLOB, ExecutionTime DOUBLE)")

def INSERT(Waktu, Result, ExecutionTime, Algoritma="selection", ):
    query = "INSERT INTO sorts (Waktu, Algoritma, Result, ExecutionTime) VALUES (?, ?, ?, ?)"
    query_tuple = (Waktu, Algoritma, Result, ExecutionTime)
    cursor.execute(query, query_tuple)

    print(cursor.rowcount, "record inserted.")

def GET_CONTENT(ID=-1):
    if(ID == -1):
        cursor.execute("SELECT Result FROM sorts ORDER BY ID DESC LIMIT 1")
    else:
        query = "SELECT Result FROM sorts WHERE ID = ?"
        cursor.execute(query, ID)
    
    return cursor.fetchall();