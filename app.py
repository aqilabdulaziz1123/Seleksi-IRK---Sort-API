from flask import Flask, request, jsonify
from converter import FileConverter as convert
from sorter import Sort as sort
from db import Database as db

# Init app
app = Flask(__name__)

# Init db
db.init()


@app.route('/sort/selection', methods=['POST'])
def selection_sort():
    file = request.files['file']
    column = int(request.form.get("column"))
    order = request.form.get('order')
    data_list = convert.text_to_list(file.read())
    execution_time = sort.selection_sort(data_list, column, order)
    table = convert.list_to_table(data_list)
    db.create("selection", convert.list_to_text(data_list), execution_time)
    return table


@app.route('/sort/merge', methods=['POST'])
def merge_sort():
    file = request.files['file']
    column = int(request.form.get("column"))
    order = request.form.get('order')
    data_list = convert.text_to_list(file.read())
    execution_time = sort.merge_sort(data_list, column, order)
    table = convert.list_to_table(data_list)
    db.create("merge", convert.list_to_text(data_list), execution_time)
    return table


@app.route('/sort/result', methods=["GET"])
def result():
    return convert.list_to_table(convert.text_to_list(db.read()))


@app.route('/sort/result/<id>', methods=["GET"])
def result_by_id(id):
    return convert.list_to_table(convert.text_to_list(db.read_by_id(id)))


if __name__ == "__main__":
    app.run(debug=True)
