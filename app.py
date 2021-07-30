from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from database import *
from main import list_to_string, list_to_table, string_to_list, selection_sort, insertion_sort, bubble_sort, csv_to_list
import pandas as pd

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'sort_api'

mysql = MySQL(app)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/sort/<algorithm>', methods=['POST'])
def sorting(algorithm):
    file = request.files['csv_file']
    # file.save(file.filename)
    col_idx = int(request.form.get("col_idx"))
    orientation = request.form.get("orientation")
    data = csv_to_list(file.filename)
    # data = list(csv_to_list(file.filename))
    # data = list(csv.reader(open(file.filename)))
    if algorithm == "selection":
        sorted_data, execution_time = selection_sort(data, col_idx, orientation)
    elif algorithm == "bubble":
        sorted_data, execution_time = bubble_sort(data, col_idx, orientation)
    elif algorithm == "insertion":
        sorted_data, execution_time = insertion_sort(data, col_idx, orientation)

    result_html = list_to_table(sorted_data)
    result_string = list_to_string(sorted_data)

    insert(algorithm,result_string,execution_time)

    return render_template("result.html", result=result_html)

@app.route('/sort/result', methods=['GET'])
def result():
    sorts_id = request.args.get("id")
    if sorts_id is None:
        sorts_id = select_last_id()
        result_string = select_last_id()[3]
    else:
        result_string = select_by_id(sorts_id)[3]
    result_html = list_to_table(string_to_list(result_string))
    return render_template('result.html', result=result_html, result_id=sorts_id)

if __name__ == "__main__":
    app.run(debug=True)