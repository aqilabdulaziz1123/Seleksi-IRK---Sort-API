from flask import Flask, render_template, request, Markup
from py.sorter import sort, csvtostr, csvtohtml, strtocsv, listalgo
from py.database import select, insert
from py.util import validate

app = Flask(__name__, template_folder='public')

@app.route('/')
def indeks():
  html, time = sort("username.csv", 2, "selection")
  return str("%.5f"%time)

@app.route("/sort/result", methods=['GET'])
def result():
  id = request.args.get("id")

  if id is not None and (not id.isnumeric() or int(id) < 0):
    return "bad argument (invalid id)"
  
  data = select(id)
  
  if data is None:
    return "404 not found"

  return render_template("index.html", html=Markup(csvtohtml(strtocsv(data[3]))), time="%.5f"%data[4], algorithm=data[2])

@app.route("/sort/<algo>", methods=['POST'])
def selection(algo):
  listalg = listalgo()

  if not (algo in listalg):
    return {"error": "Such algorithm is not exist in our system"}

  args = request.form.to_dict()

  file = request.files["csv"]
  if not file:
    return {"error": "Bad arguments (there should be file [csv])"}
  
  col, order, err1 = validate(args)
  if err1 is not None:
    return {"error": err1}

  # result
  arr, html, time, err2 = sort(file, col, algo, order)

  if err2 is not None:
    return {"error": err2}

  # insert
  insert(algo, csvtostr(arr), time)

  return render_template("index.html", html=Markup(html), time="%.5f"%time, algorithm=algo)
