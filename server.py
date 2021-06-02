from flask import Flask, render_template, request, Markup
from py.auth import auth, login
from py.sorter import sort, csvtostr, csvtohtml, strtocsv, listalgo
from py.database import select, insert
from py.util import validate

app = Flask(__name__, template_folder='public')

@app.route('/')
def indeks():
  return "ok"

@app.route("/auth/login", methods=["POST"])
def loginpage():
  args = request.form.to_dict()

  if not ("username" in args and "password" in args):
    return {"error": "bad argument, need username and password"}, 400

  authkey = login(args["username"], args["password"])

  if authkey is None:
    return {"error": "wrong username or password"}, 401
  
  return {"auth_key": authkey}

@app.route("/sort/result", methods=['GET'])
@auth
def result():
  id = request.args.get("id")

  if id is not None and (id == "" or not id.isnumeric() or int(id) < 0):
    return {"error" :"bad argument (invalid id)"}, 400
  
  data = select(id)
  
  if data is None:
    return {"error" :"404 not found"}, 404

  return render_template("index.html", html=Markup(csvtohtml(strtocsv(data[3]))), time="%.5f"%data[4], algorithm=data[2])

@app.route("/sort/<algo>", methods=['POST'])
@auth
def selection(algo):
  listalg = listalgo()

  if not (algo in listalg):
    return {"error": "Such algorithm is not exist in our system"}, 400

  args = request.form.to_dict()

  if not ("csv" in request.files):
    return {"error": "Bad arguments (there should be file [csv])"}, 400
    
  file = request.files["csv"]
  
  col, order, err1 = validate(args)
  if err1 is not None:
    return {"error": err1}, 400

  # result
  arr, html, time, err2 = sort(file, col, algo, order)

  if err2 is not None:
    return {"error": err2}, 400

  # insert
  insert(algo, csvtostr(arr), time)

  return render_template("index.html", html=Markup(html), time="%.5f"%time, algorithm=algo)
