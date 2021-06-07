from flask import Flask, redirect, url_for, render_template, request, Markup, make_response, jsonify, flash
from pyUtil.sorting import selection_sort, insertion_sort, bubble_sort
from pyUtil.fileUtility import filetoarr, list_to_html, arrtofilestring, filestringtoarr, allowed_columnnum, allowed_file, fileformtoarr
import mysql.connector
import datetime
import jwt 
from functools import wraps

app = Flask(__name__, template_folder= 'templates')
app.config['SECRET_KEY'] = 'secret'
session = {'login' : False}

def connectdb():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password= "",
        database="sorts")
    return db

def authentication(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return wrapped

@app.route('/')
def index():
    if not session.get('login'):
        return render_template('login.html')
    else:
        return redirect(url_for("home"))

@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    pw = request.form['password']

    if user == 'user' and pw == 'password':
        session['login'] = True
        token = jwt.encode({'user' : user}, app.config['SECRET_KEY'], algorithm='HS256')
        message = 'token : ' + token
        flash(message)
        return render_template('login.html')

    flash("Incorrect username and/or password")
    return render_template('login.html')

@app.route("/home", methods = ["POST", "GET"])
@authentication
def home():
    #jika ada masukan
    if request.method == "POST" :
        algorithm = request.form["sort-algorithm"]
        return redirect(url_for("sort", algoname = algorithm))
    #jika belum ada masukan di box
    else :
        return render_template("home.html")

@app.route("/sort/<algoname>", methods = ["POST", "GET"])
@authentication
def sort(algoname):
    #jika ada masukan
    if request.method == "POST" :
        file = request.files.get('csvfile')
        csvarray = fileformtoarr(file)
        columnidx = int(request.form["column-number"])-1
        orientation = request.form["orientation"]
        
        if not allowed_file(file.filename):
            flash("Only csv filetype allowed!", "error")
            return redirect(url_for("sort", algoname = algoname))
        if not allowed_columnnum(csvarray, columnidx):
            flash("Column number exceeded file's actual column size!", "error")
            return redirect(url_for("sort", algoname = algoname))

        if algoname == "insertion":
            sortedarr, exectime = insertion_sort(csvarray, columnidx, orientation)
        elif algoname == "selection":
            sortedarr, exectime = selection_sort(csvarray, columnidx, orientation)
        else:
            sortedarr, exectime = bubble_sort(csvarray, columnidx, orientation)

        htmltable = list_to_html(sortedarr)
        tablestring = arrtofilestring(sortedarr)

        # insert ke db
        db = connectdb()
        cur = db.cursor()
        cur.execute("INSERT INTO sorts(algoritma, result_table, execute_time) VALUES (%s, %s, %s)", (algoname, tablestring, exectime))
        db.commit()
        db.close()

        return render_template("result.html", tabel = Markup(htmltable), waktu = round(exectime, 5), algo = algoname, namakolom = sortedarr[0][columnidx], orient = orientation)
    #jika belum ada masukan di box
    else :
        return render_template("selection.html")

@app.route("/sort/result", methods = ["GET"])
@authentication
def result():
    id = request.args.get("id")
    db = connectdb()
    cur = db.cursor()
    
    if id is None:
        cur.execute("SELECT * FROM sorts ORDER BY time DESC")
    else:
        cur.execute("SELECT * FROM sorts WHERE id = %s", (id,))

    data = cur.fetchone()

    if data is None:
        flash("id tersebut tidak tersedia di dalam database!")
        return render_template("result.html")
    
    htmltable = list_to_html(filestringtoarr(data[3]))

    db.close()

    return render_template("result.html", tabel = Markup(htmltable), waktu = round(data[4], 5), algo = data[2])

@app.route("/instructions")
def instruc():
    return render_template("instructions.html")

@app.route("/aboutus")
def about():
    return render_template("aboutus.html")

if __name__ == "__main__":
    app.run(debug = True)