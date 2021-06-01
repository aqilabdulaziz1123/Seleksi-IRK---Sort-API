from flask import Flask, request, jsonify
import io

from sorts import Sorter
from utility import convert_BLOB_to_list, convert_list_to_BLOB, init, insert, get_content, html_table, preprocess

selection = Sorter.selection
merge = Sorter.merge
bubble = Sorter.bubble

app = Flask(__name__)
app.config["DEBUG"] = True
init()

@app.route("/sort/selection", methods=["POST"])
def selection_sort():
    csvFile = request.files["file"]
    pivot = request.args.get("col")
    orientation = request.args.get("sort")

    blob = csvFile.stream.read()

    data = convert_BLOB_to_list(blob)
    data = preprocess(data, pivot)

    try:
        result, execution_time = selection(data, pivot, orientation)
        table = html_table(result)

        blob = convert_list_to_BLOB(result)
        insert(blob, execution_time, "selection")

        return table
    except:
        return jsonify(Error="Index invalid!")

@app.route("/sort/bubble", methods=["POST"])
def bubble_sort():
    csvFile = request.files["file"]
    pivot = request.args.get("col")
    orientation = request.args.get("sort")

    blob = csvFile.stream.read()

    data = convert_BLOB_to_list(blob)
    data = preprocess(data, pivot)

    try:
        result, execution_time = bubble(data, pivot, orientation)
        table = html_table(result)
        
        blob = convert_list_to_BLOB(result)
        insert(blob, execution_time, "bubble")

        return table
    except:
        return jsonify(Error="Index invalid!")

@app.route("/sort/merge", methods=["POST"])
def merge_sort():
    csvFile = request.files["file"]
    pivot = request.args.get("col")
    orientation = request.args.get("sort")

    blob = csvFile.stream.read()

    data = convert_BLOB_to_list(blob)
    data = preprocess(data, pivot)

    try:
        result, execution_time = merge(data, pivot, orientation)
        table = html_table(result)
        
        blob = convert_list_to_BLOB(result)
        insert(blob, execution_time, "merge")

        return table
    except:
        return jsonify(Error="Index invalid!")

@app.route("/sort/result", methods=["GET"])
def result():
    ID = request.args.get("id")
    temp = ""
    if ID == None:
        temp = html_table(get_content(-1))
    else:
        temp = html_table(get_content(ID))
    
    if temp == None:
        return jsonify(Error="ID not found!")
    return temp

if __name__ == '__main__':
    app.run()