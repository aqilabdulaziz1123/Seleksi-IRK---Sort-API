from datetime import datetime
import MySQLdb
import re

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "pass",
                           db = "seleksiirk1")
    c = conn.cursor()

    return c, conn

def insert_sort(algo, res, exe):
    c, conn = connection()
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    sql = 'INSERT INTO sorts (time, algoritma, result, exec) VALUES (%s, %s, %s, %s)'

    c.execute(sql, [time, algo, res, str(exe)])
    conn.commit()

def select_id(id):
    c, conn = connection()
    sql = 'SELECT result FROM sorts WHERE id=%s'

    c.execute(sql, [str(id)])
    result = str(c.fetchone())

    return result[3:(len(result)-3)]

def last_id():
    c, conn = connection()
    sql = 'SELECT max(id) FROM sorts'
    
    c.execute(sql)
    result = c.fetchone()

    return result[0]