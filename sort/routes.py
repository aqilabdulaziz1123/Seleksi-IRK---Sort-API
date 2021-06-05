from sort.authentication import token_required
from sort import app
from flask import render_template, request, jsonify
from sort.database import *
from sort.dataprocessing import *
from sort.algorithm import *
from ast import literal_eval
from sort.authentication import token_required
import json
import os
import datetime
import jwt


from sort import app
    
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username=='faziz' and password == 'hahaha':
        token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return render_template('login.html')

#  Root URL
@app.route('/')
@app.route('/Home')
def home_page():
    return render_template('login.html')


@app.route('/sort/<methods>', methods=['POST'])
@token_required
def sort_page(methods):
    methods = methods
    items =[]
    uploaded_file = request.files['file']
    column = int(request.form['column'])-1
    order = request.form['order'].lower()
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        items = parseCSV(file_path)

    if methods=="selection":
        items = selection_sort(items, column, order)
    elif methods=="bubble":
        items = bubble_sort(items, column, order)
    elif methods=="insertion":
        items = insertion_sort(items, column, order)
    elif methods=="merge":
        items = merge_sort(items, column, order)
    # Add more Sort 
    else:
        return "Coming Soon.."
    return render_template('sort.html', items=items)


@app.route('/sort/result', methods=['GET'])
@token_required
def result():
    id = request.args.get('id', default=str(-1))
    latest = get_latest_id()
    if (id==str(-1)):
        id = str(latest)
    encoder = get_data(id)
    to_json = encoder.decode('utf8').replace("'", '"')
    data_json = json.loads(to_json)
    result = json.dumps(data_json)
    return render_template('sort.html', items=literal_eval(result))