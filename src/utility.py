import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv()
import os

# database Utility
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
    cursor.execute("CREATE TABLE IF NOT EXISTS sorts (ID INT AUTO_INCREMENT PRIMARY KEY, Waktu TIMESTAMP DEFAULT current_timestamp(), Algoritma VARCHAR(9), Result BLOB, ExecutionTime DOUBLE, CHECK (Algoritma IN ('selection', 'bubble', 'merge')))")

def insert(Result, ExecutionTime, Algoritma):
    database = mysql.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="SortAPI"
    )
    database.autocommit = True
    cursor = database.cursor()

    Result = Result.replace("\r", "\\r").replace("\n", "\\n")
    query = "INSERT INTO sorts (Algoritma, Result, ExecutionTime) VALUES ({0}, {1}, {2})".format("'" + Algoritma + "'", Result, ExecutionTime)
#    query = query + "\'" + Algoritma + "\'" + "," + Result + "," + ExecutionTime + ")"
    cursor.execute(query)

    print(cursor.rowcount, "record inserted.")

def get_content(ID):
    database = mysql.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="SortAPI"
    )
    database.autocommit = True
    cursor = database.cursor()

    query = "SELECT * FROM sorts "
    if(ID == -1):
        query = query + "ORDER BY ID DESC"
    else:
        query = query + "WHERE ID=" + str(ID)
    query = query + " LIMIT 1"
    cursor.execute(query)

    all_attributes = cursor.fetchone()

    if all_attributes == None:
        return convert_BLOB_to_list(all_attributes)
        
    (dummy, dummy, dummy, res, dummy) = all_attributes
    result = convert_BLOB_to_list(res)
    print(result)
    return convert_BLOB_to_list(res)


# Other functional utility
def is_number(i):
    try:
        int(i)
        return True
    except:
        return False

def preprocess(data, pivot):
    is_header = True
    is_first = True
    is_a_number = True
    pivot = int(pivot)

    invalid_row = []

    for row in data:
        if is_header:
            is_header = False
            continue
        if is_first:
            is_a_number = is_number(row[pivot])
            is_first = False
            continue
        
        is_number_type = is_number(row[pivot])
        if (is_a_number and is_number_type) or (not is_a_number and not is_number_type):
            continue
        invalid_row.append(row)
    
    for invalid in invalid_row:
        data.remove(invalid)
    
    return data

def convert_list_to_BLOB(data):
    text = '"'

    for i in range(len(data)):
        data[i] = ",".join(data[i])
    
    text = text + "\r\n".join(data)
    text = text + '"'
    return text

def convert_BLOB_to_list(BLOB):
    '''
    convert a csv file into list of list

    i.e. 
    csv content (as a blob): b"a,b,c\r\n1,2,3\r\n4,5,6"
    
    after decoding, the content is
    a,b,c
    1,2,3
    4,5,6

    returns [['a', 'b', 'c'], ['1', '2', '3'], ['4', '5', '6']]
    '''
    if BLOB == None:
        return []

    text = BLOB.decode("UTF8")

    each_line = text.split("\n")
    
    for i in range(len(each_line)):
        each_line[i] = each_line[i].replace("\r", "")
    
    for i in range(len(each_line)):
        each_line[i] = each_line[i].split(",")
    
    return each_line

def html_table(content):
    if content == []:
        return None
    html = "<table>\n"

    is_header = True
    for row in content:
        html = html + "<tr>\n"
        if(is_header):
            is_header = False
            html = html + "<th>"
            html = html + "</th><th>".join(row)
            html = html + "</th>"
        else:
            html = html + "<td>"
            html = html + "</td><td>".join(row)
            html = html + "</td>"
        html = html + "</tr>\n"

    html = html + "</table>"
    return html