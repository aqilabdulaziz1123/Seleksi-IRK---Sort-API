from datetime import datetime
import mysql.connector

def connect():
    db = mysql.connector.connect(
        host="localhost",
        user="newuser",
        passwd="password"
    )
    cursor = db.cursor()
    return db, cursor

def insert(algorithm, result, execution_time):
    db, cur = connect()
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("USE SORT_API")
    cur.execute("""INSERT INTO sorts (date, algorithm, result, execution_time)  VALUES (%s, %s, %s, %s)""",(time, algorithm, result, execution_time))
    db.commit()

def select_by_id(id):
    db, cur = connect()
    cur.execute("USE SORT_API")
    cur.execute("SELECT * FROM sorts WHERE id = %s", (id,))
    sort_tuple = cur.fetchone()
    return sort_tuple

def select_last_id():
    db, cur = connect()
    cur.execute("USE SORT_API")
    cur.execute("SELECT * FROM sorts ORDER BY id DESC")
    sort_tuple = cur.fetchone()
    return sort_tuple