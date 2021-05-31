# imports
from flask import Flask, request, make_response
import mysql.connector
from decouple import config
import json

# initializing Flask app
app = Flask(__name__)

# database credentials
DBPASS = config('DB_PASS')
DBNAME = config('DB_NAME')
DBHOST = config('DB_HOST')
DBUSER = config('DB_USER')

# mydb = mysql.connector.connect(
#   host=DBHOST,
#   user=DBUSER,
#   password=DBPASS,
#   database=DBNAME
# )

# mycursor = mydb.cursor()

@app.route('/sort/selection', methods =['POST'])
def sort():
	message = request.get_json(force=True)
	csvFile = message['file']
	idColumn = message['id']
	order = message['order']
	
	return order

app.run(debug=True)