from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, make_response
from processing.database import insert_sort, select_id, last_id
from processing.sort import selection_sort, insertion_sort, bubble_sort, merge_sort
from processing.convert import *
from werkzeug import secure_filename
import csv
import os

app = Flask(__name__)
uploads_dir = os.path.join(app.instance_path, 'uploads')

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/sort/selection", methods=['POST'])
def selection():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    result, exec_time = selection_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Selection", result_string, exec_time)
    os.remove(file.filename)

    return render_template("index.html", result=result_html)

@app.route("/sort/bubble", methods=['POST'])
def bubble():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    result, exec_time = bubble_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Bubble", result_string, exec_time)
    os.remove(file.filename)

    return render_template("index.html", result=result_html)

@app.route("/sort/merge", methods=['POST'])
def merge():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    result, exec_time = merge_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Merge", result_string, exec_time)
    os.remove(file.filename)

    return render_template("index.html", result=result_html)

@app.route("/sort/insertion", methods=['POST'])
def insertion():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    result, exec_time = insertion_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Insertion", result_string, exec_time)
    os.remove(file.filename)

    return render_template("index.html", result=result_html)

@app.route("/sort/result", methods=['GET'])
def result():
    result = select_id(last_id())
    result_html = list_to_html(string_to_list(result))

    return render_template("result.html", result_for_id=result_html, result_id=last_id())

if __name__ == '__main__':
    app.run(debug = True)