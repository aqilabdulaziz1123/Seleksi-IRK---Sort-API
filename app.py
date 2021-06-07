from flask import Flask, render_template, request, redirect, make_response, jsonify
import os
from werkzeug.utils import secure_filename
import json
from ast import literal_eval
from datetime import datetime, timedelta
from functools import wraps
import jwt

# import created function
from IOprocess import *
from algorithm import *
from database import *

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
# app.secret_key = "IRK" #random secret key, can be anything
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Max content length = 16 mb
# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads') #the directory name will be 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create connection
conn = create_db_connection()

# AUTH
# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(*args, **kwargs)
    return decorated

@app.route('/')
def base():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if(username == 'jafar' and password == '12345'):
        token = jwt.encode({'username': username,'exp' : datetime.utcnow() + timedelta(minutes = 30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    else:
        return redirect('/')

@app.route('/home')
# @token_required
def home():
    return render_template('home.html')

@app.route('/sort/<method>', methods=['POST'])
# @token_required
def upload_file(method):
    uploadedfile = request.files['file']
    kolomacuan = int(request.form['kolomacuan'])-1
    orientasi = request.form['orientasi']
    algoritma = method
    if uploadedfile.filename != '':
        filename = secure_filename(uploadedfile.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploadedfile.save(file_path)
        jsonarray = convertCSV(file_path)
    
    # Validasi kolom acuan
    column = len(list(jsonarray[0].keys()))
    if (kolomacuan >= column):
        return redirect('/')

    # SORT
    if (method == 'selection'):
        data, exectime = selectionsort(jsonarray, kolomacuan, orientasi)
    elif (method == 'bubble'):
        data,exectime = bubbleSort(jsonarray, kolomacuan, orientasi)
    else:
        return "<h1>Method %s not recognized </h1>" %method

    insertData(conn, jsonarray, method, exectime)
    keys = list(data[0].keys())
    return render_template('result.html',data = data, keys = keys)

@app.route('/sort/result', methods=['GET'])
@token_required
def showresult():
    # if key doesn't exist, returns None
    id = request.args.get('id')
    if(id == None):
        id = getLastId(conn)
    databyte = getdata(conn,int(id))
    if(databyte == 'No data'):
        return "<h1>Id %s not found  </h1>" %id
    jsonData = databyte.decode('utf8').replace("'", '"')
    data = json.loads(jsonData)
    data = json.dumps(data)
    finaldata = literal_eval(data)
    keys = list(finaldata[0].keys())
    return render_template('result.html', data= finaldata, keys=keys)

if __name__ == "__main__":
    app.run(debug=True)