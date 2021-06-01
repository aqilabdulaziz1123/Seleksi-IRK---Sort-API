# imports
from flask import Flask, request, make_response, jsonify

from werkzeug.datastructures import ImmutableMultiDict

from script.sort_algorithm import selection,insertion,bubble
from script.database import convertHTMLTable,insert,select

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# initializing Flask app
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "seleksiIRK"
jwt = JWTManager(app)
authorizedUser = {
	'test': 'pass',
	'user2': 'hello'
}

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
	username = request.args.get("username", None)
	password = request.args.get("password", None)
	if password != authorizedUser[username]:
		return jsonify({"msg": "Bad username or password"}), 401

	access_token = create_access_token(identity=username)
	return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/sort/selection', methods =['POST'])
@jwt_required()
def selection_sort():
	message = request.args.to_dict(flat=True)
	csvFile = request.files['file']
	
	current_user = get_jwt_identity()

	print(message)
	sortTable, execTime = selection(csvFile,int(message['id']),message['order'])

	print(execTime)
	insert("Selection Sort",sortTable,csvFile,execTime)

	return convertHTMLTable(sortTable)

@app.route('/sort/insertion', methods =['POST'])
@jwt_required()
def insertion_sort():
	message = request.args.to_dict(flat=True)
	csvFile = request.files['file']
	
	current_user = get_jwt_identity()

	print(message)
	sortTable, execTime = insertion(csvFile,int(message['id']),message['order'])

	print(execTime)
	insert("Insertion Sort",sortTable,csvFile,execTime)

	return convertHTMLTable(sortTable)

@app.route('/sort/bubble', methods =['POST'])
@jwt_required()
def bubble_sort():
	message = request.args.to_dict(flat=True)
	csvFile = request.files['file']

	current_user = get_jwt_identity()

	print(message)
	sortTable, execTime = bubble(csvFile,int(message['id']),message['order'])

	print(execTime)
	insert("Bubble Sort",sortTable,csvFile,execTime)

	return convertHTMLTable(sortTable)

@app.route('/sort/result', methods =['GET'])
@jwt_required()
def getTable():
	message = request.args.get('id')
	id = message if message != None else -1
	
	current_user = get_jwt_identity()
	
	return select(id)

if __name__ == "__main__":
	app.run(debug=True)