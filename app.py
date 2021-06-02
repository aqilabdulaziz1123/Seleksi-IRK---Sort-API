from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import mysql.connector
from datetime import datetime, timedelta, date
from werkzeug.utils import secure_filename
import os
import csv
import time
import jwt


UPLOAD_FOLDER = 'test'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = "semoga masuk irk amin"

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="sortirk"
)
mycursor = mydb.cursor()

def isFloat(a):
    try:
        b = float(a)
        return True
    except:
        return False
def isInt(a):
    try:
        b = int(a)
        return True
    except:
        return False

def getTipe(a):
    if isInt(a):
        return "int"
    elif isFloat(a):
        return "float"
    else:
        return "string"

def preprocess(kolom, tabel):
    temp = tabel
    tempcol = kolom
    colbuang = []
    tipe = getTipe(kolom[0])
    for i in range(1, len(kolom)):
        if getTipe(kolom[i]) != tipe:
            colbuang.append(i)
    for i in colbuang:
        temp[i] = ""
        tempcol[i] = ""
    temp = [a for a in temp if a != ""]
    tempcol = [a for a in tempcol if a != ""]
    if tipe == "int":
        tempcol = [int(a) for a in tempcol]
    elif tipe == "float":
        tempcol = [float(a) for a in tempcol]
    return temp, tempcol

def sasc(kolom, tabel):
    for i in range(len(kolom)):
        min = kolom[i]
        idx = i
        for j in range(i, len(kolom)):
            if kolom[j] < min:
                min = kolom[j]
                idx = j
        tempcol = kolom[i]
        temp = tabel[i]
        kolom[i] = min
        tabel[i] = tabel[idx]
        kolom[idx] = tempcol
        tabel[idx] = temp
    return kolom, tabel

def sdesc(kolom, tabel):
    for i in range(len(kolom)):
        max = kolom[i]
        idx = i
        for j in range(i, len(kolom)):
            if kolom[j] > max:
                max = kolom[j]
                idx = j
        tempcol = kolom[i]
        temp = tabel[i]
        kolom[i] = min
        tabel[i] = tabel[idx]
        kolom[idx] = tempcol
        tabel[idx] = temp
    return kolom, tabel

def output(tabel, kolom):
    teks = ""
    for k in range(len(kolom)):
        if k != len(kolom) -1:
            teks += kolom[k] + ","
        else:
            teks += kolom[k]
    teks += " "
    for i in range(len(tabel)):
        for j in range(len(tabel[i])):
            if j != len(tabel[i]) - 1:
                teks += tabel[i][j] + ","
            else:
                teks += tabel[i][j]
        if i != len(tabel) - 1:
            teks += " "
    return teks

def getData(namafile, arah, kolom):
    found = True
    asc = True
    if arah != "asc":
        asc = False
    file = 'test/' + namafile
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')

        #baca csv
        columns = []
        temp = []
        tempcol = []
        first = True
        for row in csv_reader:
            if first:
                columns.append(row)
                first = False
                columnscount = len(columns[0])
                if (kolom < 1 or kolom > columnscount):
                    found = False
                    return [], [], found
            else:
                temp.append(row)
                tempcol.append(row[kolom-1])
    return temp,tempcol,asc, columns[0], found

def selection(namafile, arah, kolom):
    start_time = time.time()
    temp,tempcol,asc,columns,found = getData(namafile, arah, kolom)
    if found == False:
        return "", 0, found
    #preprocess
    tabel, kolom = preprocess(tempcol, temp)
    #sort
    if asc:
        col, res = sasc(kolom, tabel)
    else:
        col, res = sdesc(kolom, tabel)
    waktu = time.time() - start_time
    return output(res, columns), waktu, found

def basc(kolom, tabel):
    urut = False
    while urut == False:
        urut = True
        for i in range(len(kolom)-1):
            if kolom[i] > kolom[i+1]:
                temp = kolom[i]
                kolom[i] = kolom[i+1]
                kolom[i+1] = temp
                temptabel = tabel[i]
                tabel[i] = tabel[i+1]
                tabel[i+1] = temptabel
                urut = False
    return kolom, tabel

def bdesc(kolom,tabel):
    urut = False
    while urut == False:
        urut = True
        for i in range(len(kolom)-1):
            if kolom[i] < kolom[i+1]:
                temp = kolom[i]
                kolom[i] = kolom[i+1]
                kolom[i+1] = temp
                temptabel = tabel[i]
                tabel[i] = tabel[i+1]
                tabel[i+1] = temptabel
                urut = False
    return kolom, tabel

def bubble(namafile, arah, kolom):
    start_time = time.time()
    temp,tempcol,asc,columns,found = getData(namafile, arah, kolom)
    if found == False:
        return "", 0, found
    #preprocess
    tabel, kolom = preprocess(tempcol, temp)
    #sort
    if asc:
        col, res = basc(kolom, tabel)
    else:
        col, res = bdesc(kolom, tabel)
    waktu = time.time() - start_time
    return output(res, columns), waktu, found


@app.route('/', methods=['POST', 'GET'])
def index():
    session.clear()
    return render_template('login.html')

@app.route('/sort', methods = ['POST', 'GET'])
def sort():
    try:
        token = session['token']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        return render_template('index.html')
    except:
        return "Token Invalid"

@app.route('/login', methods = ['POST'])
def login():
    try:
        p = request.form['password']
        if request.form['username'] and p == '123456':
            token = jwt.encode({
                'username' : request.form['username'],
                'exp': datetime.utcnow() + timedelta(seconds=300)
            },
            app.config['SECRET_KEY'])
            session['token'] = token
            return redirect(url_for(".sort"))
        else:
            return "Invalid Login"
    except:
        return "Error"


@app.route('/sort/selection', methods=['POST'])
def selectionsort():
    try:
        token = session['token']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    except:
        return "Token Invalid"
    try:
        files = request.files['dataselection']
        namafile = files.filename
        arah = request.form['arah']
        kolom = int(request.form['kolom'])

        if namafile == "" or kolom =="":
            return "Ada error di input"

        if files:
            filename = secure_filename(files.filename)
            files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "Ada error di input"

        teks, etime, lanjut = selection(namafile, arah, kolom)

        if lanjut:
            sql = "INSERT INTO sorts (algoritma, hasil_sorting, execution_time) VALUES (%s, %s, %s)"
            val = ("Selection Sort", teks, etime)
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('.sort'))
        else:
            return "Ada error di input"
    except:
        return "Ada error di input"

@app.route('/sort/result', methods=['GET'])
def result():
    try:
        token = session['token']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    except:
        return "Token Invalid"
    mycursor.execute("SELECT hasil_sorting FROM sorts ORDER BY id DESC LIMIT 1")

    res = mycursor.fetchone()

    res = res[0]
    res1 = res.split(" ")
    kolom = ""
    isi = []
    for i in range(len(res1)):
        if i == 0:
            kolom += res1[i]
        else:
            isi.append(res1[i])
    kolom = kolom.split(",")
    temp = []
    for i in isi:
        temp.append(i.split(","))
    isi = temp
    return render_template('result.html', kolom = kolom, sorted = isi)


@app.route('/sort/bubble', methods=['POST'])
def bubblesort():
    try:
        token = session['token']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    except:
        return "Token Invalid"
    try:
        files = request.files['databubble']
        namafile = files.filename
        arah = request.form['arah']
        kolom = int(request.form['kolom'])

        if namafile == "" or kolom =="":
            return "Ada error di input"

        if files:
            filename = secure_filename(files.filename)
            files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "Ada error di input"

        teks, etime, lanjut = bubble(namafile, arah, kolom)

        if lanjut:
            sql = "INSERT INTO sorts (algoritma, hasil_sorting, execution_time) VALUES (%s, %s, %s)"
            val = ("Bubble Sort", teks, etime)
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('.sort'))
        else:
            return "Ada error di input"
    except:
        return "Ada error di input"

@app.route('/sort/temp', methods=['GET'])
def temp():
    mycursor.execute("SELECT * FROM sorts ORDER BY id DESC LIMIT 1")
    res = mycursor.fetchone()
    return render_template('temp.html', sort = res)

if __name__ == "__main__":
    app.run(debug = True)

