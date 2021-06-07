import mysql.connector as msql
from mysql.connector import Error
from decouple import config

DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')

# CREATE TABLE
query = '''CREATE TABLE sorts (
    id int(11) auto_increment primary key,
    dateSort TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    algoritma varchar(50),
    result blob NULL,
    time float NULL
);
'''

try:
    conn = msql.connect(host='localhost',database=DB_NAME, user=DB_USER,  
                        password=DB_PASS)#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(query)
        print("Tabel berhasil dimasukan")
        conn.commit()
        print("record inserted")
except Error as e:
    print("Error while connecting to MySQL", e)