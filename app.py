# imports
from flask import Flask, request, make_response
from werkzeug.datastructures import ImmutableMultiDict
from script.selection_sort import selection
from script.database import convertHTMLTable,insert,select
import json

# initializing Flask app
app = Flask(__name__)

@app.route('/sort/selection', methods =['POST'])
def sort():
	message = request.args.to_dict(flat=True)
	csvFile = request.files['file']
	
	print(message)
	sortTable, execTime = selection(csvFile,int(message['id']),message['order'])

	print(execTime)
	insert("Selection Sort",sortTable,csvFile,execTime)

	return convertHTMLTable(sortTable)

@app.route('/sort/result', methods =['GET'])
def getTable():
	message = request.args.to_dict(flat=True)
	id = message['id'] if message['id'] != None else -1
	
	return select(id)

if __name__ == "__main__":
	app.run()