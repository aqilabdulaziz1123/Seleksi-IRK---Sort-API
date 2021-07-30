from flask import Flask, request, jsonify, make_response
from converter import FileConverter as convert
from sorter import Sort as sort
from db import Database as db
from functools import wraps
import jwt
import datetime

# Init app
app = Flask(__name__)

# Init db
db.init()

app.config['SECRET_KEY'] = 'secretkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'msg': 'Token is missing!'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'msg': 'Token is invalid'})

        return f(*args, **kwargs)

    return decorated


@app.route('/sort/selection', methods=['POST'])
@token_required
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
@token_required
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
@token_required
def result():
    return convert.list_to_table(convert.text_to_list(db.read()))


@app.route('/sort/result/<id>', methods=["GET"])
@token_required
def result_by_id(id):
    return convert.list_to_table(convert.text_to_list(db.read_by_id(id)))


@app.route('/login')
def login():
    auth = request.authorization

    if(auth and auth.password == 'password'):
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Login Required')


if __name__ == "__main__":
    app.run(debug=True)
