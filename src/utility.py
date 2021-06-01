import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv()
import os

def init():
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

def insert(Waktu, Result, ExecutionTime, Algoritma="selection"):
    database = mysql.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="SortAPI"
    )
    database.autocommit = True
    cursor = database.cursor()

    query = "INSERT INTO sorts (Waktu, Algoritma, Result, ExecutionTime) VALUES (?, ?, ?, ?)"
    query_tuple = (Waktu, Algoritma, Result, ExecutionTime)
    cursor.execute(query, query_tuple)

    print(cursor.rowcount, "record inserted.")

def get_content(ID=-1):
    database = mysql.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="SortAPI"
    )
    database.autocommit = True
    cursor = database.cursor()

    query = "SELECT Result FROM sorts "
    if(ID == -1):
        query = query + "ORDER BY ID DESC"
    else:
        query = query + "WHERE ID=" + str(ID)
    cursor.execute(query)

    return cursor.fetchone();

def convert_BLOB_to_list(BLOB):
    '''
    convert a csv file into list of list

    i.e. csv content (as a blob): b"a,b,c\r\n1,2,3\r\n4,5,6"
    returns [['a', 'b', 'c'], ['1', '2', '3'], ['4', '5', '6']]
    '''
    if BLOB == None:
        return []

    text = BLOB.decode("UTF8")
    print(text)

    each_line = text.split("\n")
    
    for i in range(len(each_line)):
        each_line[i] = each_line[i].replace("\r", "")
    
    for i in range(len(each_line)):
        each_line[i] = each_line[i].split(",")
    
    return each_line

def html_table(BLOB):
    convert_body = lambda column : "<td>" + column + "</td>\n"
    convert_header = lambda column : "<th>" + column + "</th>\n" 

    content = convert_BLOB_to_list(BLOB)
    html = "<table>\n"

    is_header = True
    for row in content:
        html = html + "<tr>\n"
        if(is_header):
            is_header = False
            html = html + map(convert_header, row)
        else:
            html = html + map(convert_body, row)
        html = html + "</tr>\n"

    html = html + "</table>"

    print(html)
    return html