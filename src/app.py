from flask import Flask, request, jsonify

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

    file = open(csvFile, "rb")
    blob = file.read()
    data = convert_BLOB_to_list(blob)
    data = preprocess(data, pivot)

    try:
        result, execution_time = selection(data, pivot, orientation)
    except:
        return jsonify(Error="Index invalid!")

    result = convert_list_to_BLOB(result)
    insert(result, execution_time, "selection")

@app.route("/sort/bubble", methods=["POST"])
def bubble_sort():
    csvFile = request.files["file"]
    pivot = request.args.get("col")
    orientation = request.args.get("sort")

    file = open(csvFile, "rb")
    blob = file.read()
    data = convert_BLOB_to_list(blob)
    data = preprocess(data, pivot)

    try:
        result, execution_time = bubble(data, pivot, orientation)
    except:
        return jsonify(Error="Index invalid!")

    result = convert_list_to_BLOB(result)
    insert(result, execution_time, "bubble")

@app.route("/sort/merge", methods=["POST"])
def merge_sort():
    csvFile = request.files["file"]
    pivot = request.args.get("col")
    orientation = request.args.get("sort")

    file = open(csvFile, "rb")
    blob = file.read()
    data = convert_BLOB_to_list(blob)
    data = preprocess(data, pivot)

    try:
        result, execution_time = merge(data, pivot, orientation)
    except:
        return jsonify(Error="Index invalid!")

    result = convert_list_to_BLOB(result)
    insert(result, execution_time, "merge")

@app.route("/sort/result", methods=["GET"])
def result():
    ID = request.args.get("id")
    temp = ""
    if ID == None:
        temp = html_table(get_content())
    else:
        temp = html_table(get_content(ID=ID))
    
    if temp == None:
        return jsonify(Error="ID not found!")
    return temp

if __name__ == '__main__':
    app.run()