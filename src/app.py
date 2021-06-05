from flask import Flask, render_template, request, jsonify, make_response
from processing.database import insert_sort, select_id, last_id
from processing.sort import selection_sort, insertion_sort, bubble_sort, merge_sort
from processing.convert import *
from functools import wraps
import csv, os, jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seleksiirk1'
global message

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route("/", methods=['POST', 'GET'])
def home():
    global message
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username}, app.config['SECRET_KEY'])

        message = token.decode('UTF-8')
        return render_template("index.html", token_message=message)

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'}) 

@app.route("/sort", methods=['POST', 'GET'])
@token_required
def sort():
    return render_template("sort.html", token_message=message)

@app.route("/sort/selection", methods=['POST'])
@token_required
def selection():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    if (len(list(csv.reader(open(file.filename)))) == 0 or (col<1 or col>len(list(csv.reader(open(file.filename)))[0])-1)):
        os.remove(file.filename)
        return render_template("sort.html", result='<p style="text-align: center">Index out of range!</p>', token_message=message)

    result, exec_time = selection_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Selection", result_string, exec_time)
    os.remove(file.filename)

    return render_template("sort.html", result=result_html, token_message=message)

@app.route("/sort/bubble", methods=['POST'])
@token_required
def bubble():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    if (len(list(csv.reader(open(file.filename)))) == 0 or (col<1 or col>len(list(csv.reader(open(file.filename)))[0])-1)):
        os.remove(file.filename)
        return render_template("sort.html", result='<p style="text-align: center">Index out of range!</p>', token_message=message)

    result, exec_time = bubble_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Bubble", result_string, exec_time)
    os.remove(file.filename)

    return render_template("sort.html", result=result_html, token_message=message)

@app.route("/sort/merge", methods=['POST'])
@token_required
def merge():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    if (len(list(csv.reader(open(file.filename)))) == 0 or (col<1 or col>len(list(csv.reader(open(file.filename)))[0])-1)):
        os.remove(file.filename)
        return render_template("sort.html", result='<p style="text-align: center">Index out of range!</p>', token_message=message)

    result, exec_time = merge_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Merge", result_string, exec_time)
    os.remove(file.filename)

    return render_template("sort.html", result=result_html, token_message=message)

@app.route("/sort/insertion", methods=['POST'])
@token_required
def insertion():
    file = request.files['fileCsv']
    file.save(file.filename)
    col = int(request.form.get("column", False))
    ori = request.form.get("orient", False)

    if (len(list(csv.reader(open(file.filename)))) == 0 or (col<1 or col>len(list(csv.reader(open(file.filename)))[0])-1)):
        os.remove(file.filename)
        return render_template("sort.html", result='<p style="text-align: center">Index out of range!</p>', token_message=message)

    result, exec_time = insertion_sort(list(csv.reader(open(file.filename))), col, ori)
    result_html = list_to_html(result)
    result_string = list_to_string(result)

    insert_sort("Insertion", result_string, exec_time)
    os.remove(file.filename)

    return render_template("sort.html", result=result_html, token_message=message)

@app.route("/sort/result", methods=['GET'])
@token_required
def result():
    if request.args['id'] == '':
        required_id = last_id()
    else:
        required_id = request.args['id']

    result = select_id(required_id)
    result_html = list_to_html(string_to_list(result))

    return render_template("result.html", result_for_id=result_html, result_id=required_id, token_message=message)

if __name__ == '__main__':
    app.run(debug = True)