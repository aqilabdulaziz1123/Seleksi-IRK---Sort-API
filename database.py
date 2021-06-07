import mysql.connector as msql
from mysql.connector import Error
from decouple import config

DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')

def create_db_connection():
    conn = None
    try:
        conn = msql.connect(host='localhost',database=DB_NAME, user=DB_USER,password=DB_PASS)#give ur username, password
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return conn

def insertData(connection,jsonArray, method, exectime):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO sorts (algoritma, result, time) values ('%s', \"%s\", %f);" %(method,jsonArray,exectime))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def getLastId(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT max(id) from sorts;")
        row = cursor.fetchone()
        if(row == None):
            return -1
        else:
            return row[0]
    except Error as err:
        print(f"Error: '{err}'")

def getdata(connection, id = -1):
    cursor = connection.cursor()
    try:
        if(id == -1):
            return "No data"
        else:
            cursor.execute("select result from sorts where id = %d;" %id)
            data = cursor.fetchone()
            if(data == None):
                return "No data"
            else:
                return data[0]
    except Error as err:
        print(f"Error: '{err}'")
