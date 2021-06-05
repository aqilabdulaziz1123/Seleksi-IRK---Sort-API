from flask import Flask
import mysql.connector as msql
from mysql.connector import Error
app = Flask(__name__)
# Upload Folder
UPLOAD_FOLDER = 'sort/resources/uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'DTalone'

try:
    # Input host and user with/o password
    conn = msql.connect(host='127.0.0.1', user='root',  
                        password='', database='SORTS')
    if conn.is_connected():
        cursor = conn.cursor()
        print("Connected to Database")
except Error as e:
    print("Error while connecting to MySQL", e)
    conn = msql.connect(host='127.0.0.1', user='root',  
                    password='')
    if conn.is_connected():
        cursor = conn.cursor()
        # Masukkan Nama Database
        cursor.execute("CREATE DATABASE SORTS")
        print("Database is created")
        cursor.execute('USE SORTS;')

# Creating table for the first Time
try:
    # Creating Table
    print('Creating table....')
    cursor.execute("CREATE TABLE sorts(id INT NULL AUTO_INCREMENT, tanggal DATETIME NULL,algoritma VARCHAR(45) NULL, hasil BLOB NULL, duration FLOAT NULL, PRIMARY KEY (id))")
    print("Table is created....")
except Error as e:
    print("Table was created")


from sort import routes 