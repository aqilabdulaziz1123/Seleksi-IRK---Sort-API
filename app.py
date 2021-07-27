from models.sorts import database
from flask import Flask, request, render_template
import io
import csv
import time

app = Flask(__name__)


@app.route("/")
def main():
    return "Tugas Seleksi IRK 2021"

@app.route("/sort/selection", methods=["POST"])
def selectionSort():
    file = request.files["file"]
    column = request.form["column"]
    orientation = request.form["orientation"]
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    final_table = [row for row in csv_input]
    column_data = [row[int(column)] for row in final_table if len(row) > int(column)]

    # Preprocess
    numCount = 0
    strCount = 0
    for data in column_data:
        if data.isnumeric():
            numCount = numCount + 1
        else:
            strCount = strCount + 1
    
    if (numCount >= strCount):
        column_data = [data for data in column_data if data.isnumeric()]
    else:
        column_data = [data for data in column_data if not data.isnumeric()]

    # Selection Sort
    result = []
    start_time = time.time()
    if (orientation == "ASC"):
        while (len(column_data) != 0):
            minimum = column_data[0]
            for i in range(1,len(column_data)):
                if (column_data[i] < minimum):
                    minimum = column_data[i]
            result.append(minimum)
            column_data.remove(minimum)
    else:
        while (len(column_data) != 0):
            maximum = column_data[0]
            for i in range(1,len(column_data)):
                if (column_data[i] > maximum):
                    maximum = column_data[i]
            result.append(maximum)
            column_data.remove(maximum)
    exec_time = time.time() - start_time

    print(result)

    params = {
        "algorithm": "selection",
        "result": ",".join(result),
        "exec_time": str(exec_time)
    }

    mysqldb.postSort(**params)
    
    for i in range(len(final_table)):
        if(len(final_table[i]) > int(column) and len(result) > i):
            final_table[i][int(column)] = result[i]
        if(len(result) <= i and len(final_table[i]) > int(column)):
            final_table[i][int(column)] = None

    htmlResult = """<html><body><table style="width:100%">"""
    for row in final_table:
        htmlResult = htmlResult + """<tr>"""
        for col in row:
            if (col is not None):
                htmlResult = htmlResult + """<td>"""
                htmlResult = htmlResult + str(col)
                htmlResult = htmlResult + """</td>"""
        htmlResult = htmlResult + """</tr>"""
    htmlResult = htmlResult + """</table></body></html>"""

    return htmlResult

@app.route("/sort/insertion", methods=["POST"])
def insertionSort():
    file = request.files["file"]
    column = request.form["column"]
    orientation = request.form["orientation"]
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    final_table = [row for row in csv_input]
    column_data = [row[int(column)] for row in final_table if len(row) > int(column)]

    # Preprocess
    numCount = 0
    strCount = 0
    for data in column_data:
        if data.isnumeric():
            numCount = numCount + 1
        else:
            strCount = strCount + 1
    
    if (numCount >= strCount):
        column_data = [data for data in column_data if data.isnumeric()]
    else:
        column_data = [data for data in column_data if not data.isnumeric()]
    
    # Insertion Sort
    result = column_data
    start_time = time.time()
    if (orientation == "ASC"):
        for i in range(1, len(result)):
            pivot = result[i]
            j = i - 1
            while j >= 0 and pivot < result[j] :
                    result[j + 1] = result[j]
                    j -= 1
            result[j + 1] = pivot
    else:
        for i in range(1, len(result)):
            pivot = result[i]
            j = i - 1
            while j >= 0 and pivot > result[j] :
                    result[j + 1] = result[j]
                    j -= 1
            result[j + 1] = pivot
    exec_time = time.time() - start_time

    params = {
        "algorithm": "insertion",
        "result": ",".join(result),
        "exec_time": str(exec_time)
    }

    print(result)

    mysqldb.postSort(**params)
    
    for i in range(len(final_table)):
        if(len(final_table[i]) > int(column) and len(result) > i):
            final_table[i][int(column)] = result[i]
        if(len(result) <= i and len(final_table[i]) > int(column)):
            final_table[i][int(column)] = None

    print(final_table)

    htmlResult = """<html><body><table style="width:100%">"""
    for row in final_table:
        htmlResult = htmlResult + """<tr>"""
        for col in row:
            if (col is not None):
                htmlResult = htmlResult + """<td>"""
                htmlResult = htmlResult + str(col)
                htmlResult = htmlResult + """</td>"""
        htmlResult = htmlResult + """</tr>"""
    htmlResult = htmlResult + """</table></body></html>"""

    return htmlResult


@app.route("/sort/result", methods=["GET"])
def getResult():
    if "id" in request.args.keys():
        sort_id = request.args["id"]
        response = mysqldb.getSort(sort_id)
    else:
        response = mysqldb.getSort()

    response_dict = {
        "id": response[0],
        "date_time": response[1],
        "algorithm": response[2],
        "result": response[3],
        "exec_time": response[4]
    }
    return response_dict

if __name__ == "__main__":
    mysqldb = database()
    if mysqldb.db.is_connected():
        print('Connected to MySQL database')
    
    app.run(debug=True)
    
    if mysqldb.db is not None and mysqldb.db.is_connected():
        mysqldb.db.close()