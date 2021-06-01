from flask import Flask, render_template, redirect, request, url_for

from sorts import Sorter
from utility import init, insert, get_content, html_table

selection_sort = Sorter.selection
insertion_sort = Sorter.insertion
merge_sort = Sorter.merge
bubble_sort = Sorter.bubble

app = Flask(__name__)
app.config["DEBUG"] = True
init()

@app.route("/")
def home():
    return "";
#    return render_template('home.html')

@app.route("/sort/<type>", methods=["POST", "GET"])
def sort(type):
#    csvFile = request.files["file"]
    pivot = request.args.get("col")
    orientation = request.args.get("sort")
    if request.method == "GET":
        return render_template('index.html', type=type, col=pivot, sort=orientation)
    else:
        csvFile = request.form["file"]
        return ""

@app.route("/sort/result", methods=["GET"])
def result():
    ID = request.args.get("id")
    if ID == None:
        return html_table(get_content())
    else:
        return html_table(get_content(ID=ID))

if __name__ == '__main__':
    app.run()