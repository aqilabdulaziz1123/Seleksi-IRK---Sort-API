import mysql.connector
import os

def connection():
  db = mysql.connector.connect(
    host=os.environ.get("dbhost"),
    user=os.environ.get("dbuser"),
    password=os.environ.get("dbpass"),
    database=os.environ.get("dbdb")
  )
  return db

def insert(algo, result, exectime):
  db = connection()
  cursor = db.cursor()

  query = "INSERT INTO sorts (algoritma, result, exectime) VALUES (%s, %s, %s)"
  args = (algo, result, exectime)

  cursor.execute(query, args)
  db.commit()

def select(id = None):
    db = connection()
    cursor = db.cursor()

    data = ""

    if id is None:
        cursor.execute("SELECT * FROM sorts ORDER BY time DESC")
    else:
        cursor.execute("SELECT * FROM sorts WHERE id = %s", (id,))
    
    data = cursor.fetchone()

    return data
