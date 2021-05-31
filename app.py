# imports
from flask import Flask, request, make_response
from werkzeug.datastructures import ImmutableMultiDict
from script.sort_algorithm import selection,insertion,bubble
from script.database import convertHTMLTable,insert,select
import json

# initializing Flask app
app = Flask(__name__)

@app.route('/sort/selection', methods =['POST'])
def selection_sort():
	message = request.args.to_dict(flat=True)
	csvFile = request.files['file']
	
	print(message)
	sortTable, execTime = selection(csvFile,int(message['id']),message['order'])

	print(execTime)
	insert("Selection Sort",sortTable,csvFile,execTime)

	return convertHTMLTable(sortTable)

@app.route('/sort/insertion', methods =['POST'])
def insertion_sort():
	message = request.args.to_dict(flat=True)
	csvFile = request.files['file']
	
	print(message)
	sortTable, execTime = insertion(csvFile,int(message['id']),message['order'])

	print(execTime)
	insert("Insertion Sort",sortTable,csvFile,execTime)

	return convertHTMLTable(sortTable)

@app.route('/sort/bubble', methods =['POST'])
def bubble_sort():
	message = request.args.to_dict(flat=True)
	csvFile = request.files['file']
	
	print(message)
	sortTable, execTime = bubble(csvFile,int(message['id']),message['order'])

	print(execTime)
	insert("Bubble Sort",sortTable,csvFile,execTime)

	return convertHTMLTable(sortTable)

@app.route('/sort/result', methods =['GET'])
def getTable():
	message = request.args.get('id')
	id = message if message != None else -1
	
	return select(id)

if __name__ == "__main__":
	app.run()