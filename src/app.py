from logging import debug
from flask import Flask, render_template, redirect, request
from flask.helpers import url_for

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    return redirect(url_for("sort", type="selection"))
#    return render_template('home.html')

@app.route("/sort/<type>", methods=["POST", "GET"])
def sort(type):
    if request.method == "GET":
        return render_template('index.html', type=type)
    else:
        user = request.form["user"]
        return redirect(url_for("result", name=user))

@app.route("/sort/result/<name>")
def result(name):
    return render_template('result.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)