import os
import time
import jwt
import uuid
import re
from flask import Flask, request, session, jsonify, make_response
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from csv_processing import *
from sorting import *
from html_processing import *
from other_util import *

app = Flask(__name__)
app.config['DEBUG'] = True

load_dotenv()

# Set a secret key (private key) as an information used to decrypt or encrypt message
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Set up MySql database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = 'sorts'

mysql = MySQL(app)

# Authenticate user via JSON Web Token (JWT)
def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.args.get('token')
        # Return 401 if token is not passed
        if not token:
            return "<h1>401 Error</h1><p>Token is Missing!</p>", 401
  
        try:
            # Decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return "<h1>401 Error</h1><p>Token is Invalid!</p>", 401
        # Returns the current logged in users contex to the routes
        return  f(*args, **kwargs)
  
    return decorated

# A function to process csv input from the user to the sorted one and can be used flexibly in this program
def csv_processing(algoritma, token):
    # Initiate mysql connection & cursor
    conn = mysql.connection
    cursor = conn.cursor()

    # Start time of the algorithm
    start_time = time.time()

    # Save the csv file from the user to 'csv_inputs' folder
    try:
        f = request.files['csv_file']
        file_path = os.path.join('..', 'csv_inputs', secure_filename(f.filename))
        f.save(file_path)

    # Error handling if the user doesn't input any file
    except FileNotFoundError:
        w = algoritma.split()
        return f"""
        <p>Please Input the CSV File!</p>
        <a href='/sort/{w[0].lower()}?token={token}'>Back to {algoritma}</a>
        """

    # Get Column Number
    try:
        column_no = int(request.form.get('column_no'))
    
    # Error handling if the user doesn't input any column number
    except ValueError:
        w = algoritma.split()
        return f"""
        <p>Please Input the Column No.!</p>
        <a href='/sort/{w[0].lower()}?token={token}'>Back to {algoritma}</a>
        """

    # Get Sorting Orientation (Ascending or Descending)
    # try:
    orientation = request.form.get('orientation')
    # except ValueError:
    #     w = algoritma.split()
    #     print(w[0].lower())
    #     return f"""
    #     <p>Please Input the Sorting Orientation (ASC/DESC)!</p>
    #     <a href='/sort/{w[0].lower()}'>Back to {algoritma}</a>
    #     """

    # Preprocess the csv file
    clean_strip(file_path)
    preprocessed_data = data_preprocess(file_path)

    # Get the column names
    column_name = preprocessed_data[0][column_no-1]

    # Get list of row for the specified column
    list_of_row = preprocessed_data[column_no]

    # Start sorting algorithm
    sorted_list = []
    # Select which sort that the user wants to use
    if algoritma == 'Selection Sort':
        sorted_list = selection_sort(list_of_row, orientation)
    elif algoritma == 'Bubble Sort':
        sorted_list = bubble_sort(list_of_row, orientation)
    elif algoritma == 'Merge Sort':
        sorted_list = merge_sort(list_of_row, orientation)
    
    # Change the specified column of data that the user changes
    preprocessed_data[column_no] = sorted_list

    # Change the sorted_list to comma separated value
    csv_result = list_to_csv(preprocessed_data)

    # Change the csv file into binary (blob) to be saved into the database
    csv_binary = str_to_bin(csv_result)

    # Get the execution time (Time now - Start time)
    execution_time = "{:.4f}".format(time.time() - start_time)

    # Insert the sorting result into table 'sorts'
    insertion = f"""
    INSERT INTO sorts (tanggal_waktu, algoritma, sorting_result, execution_time)
    VALUES(%s, %s, %s, %s)
    """
    cursor.execute(insertion, (datetime.now(), algoritma, csv_binary, execution_time))
    conn.commit()

    # Get the sorting result's ID from the database
    selection = """
    SELECT id
    FROM sorts
    ORDER BY id DESC
    LIMIT 1
    """
    cursor.execute(selection)
    sorting_id = cursor.fetchall()[0][0]

    # Close the cursor
    cursor.close()

    # Return the HTML Table of the sorted column, along with the sorting result's ID and execution time
    table = list_to_table(col_to_row(preprocessed_data))
    return f"""
    <p>THE SORTING RESULT HAS BEEN INSERTED INTO THE DATABASE</p>
    <p>Sorted Column : {column_name}</p>
    {table}
    <p>Execution Time : {execution_time} second(s)</p>
    <p>ID : {sorting_id}</p>
    <a href='/mainpage?token={token}'>Back to Main Menu</a>
    """

# Homepage
# Contains login and signup button
@app.route('/')
def home_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset='utf-8'>
            <title>Sorting API Homepage</title>
        </head>
        <body>
            <h1>Sorting API</h1>
            <h5>by : Daffa Ananda Pratama Resyaly -- 13519107</h5>
            <a href='/login'>Login</a><br>
            <a href='/signup'>Signup</a>
        </body>
    </html>
    """

# Mainpage for user
# Contains the sorting algorithm choices and result viewer
@app.route('/mainpage')
@authenticate
def mainpage():
    token = str(request.get_json)
    cleaned_token = re.search('\?token=(.*)\'', token).group(1)
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset='utf-8'>
            <title>Sorting API Mainpage</title>
        </head>
        <body>
            <h1>Sorting API</h1>
            <h5>by : Daffa Ananda Pratama Resyaly -- 13519107</h5>
            <a href='/sort/selection?token={cleaned_token}'>Selection Sort</a>
            <a href='/sort/bubble?token={cleaned_token}'>Bubble Sort</a>
            <a href='/sort/merge?token={cleaned_token}'>Merge Sort</a><br><br>
            <a href='/sort/result?token={cleaned_token}'>Sorting Result</a>
        </body>
    </html>
    """

# Login page and method
@app.route('/login')
def login_page():
    return log_page()

@app.route('/login', methods=['POST'])
def login():
    conn = mysql.connection
    cursor = conn.cursor()

    # Creates dictionary of form data
    auth = request.form

    could_not_verify_message = """
    <p>Could not verify</p>
    <a href='/login'>Go to Login Page</a><br>
    <a href='/'>Go to Homepage</a>
    """
  
    if not auth or not auth.get('username') or not auth.get('password'):
        # Returns 401 if any username or / and password is missing
        return make_response(
            could_not_verify_message,
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )

    check_username = f"""
    SELECT *
    FROM user
    WHERE username='{auth.get('username')}'
    """
    user = cursor.execute(check_username)
  
    if not user:
        # Returns 401 if user does not exist
        return make_response(
            could_not_verify_message,
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
    
    fetched = cursor.fetchall()[0]
    public_id = fetched[1]
    username = fetched[3]
    password = fetched[4]
    cursor.close()
  
    if check_password_hash(password, auth.get('password')):
        # Generates the JWT Token
        token = jwt.encode({
            'public_id': public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])

        session['logged_in'] = True
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

    # Returns 403 if password is wrong
    return make_response(
        could_not_verify_message,
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

# Signup page and method
@app.route('/signup')
def signup_page():
    return sign_page()

@app.route('/signup', methods=['POST'])
def signup():
    conn = mysql.connection
    cursor = conn.cursor()
    # Creates a dictionary of the form data
    data = request.form
  
    # Gets name, username and password
    name, username = data.get('name'), data.get('username')
    password = data.get('password')
  
    # Checking for existing user
    select_user = f"""
    SELECT *
    FROM user
    WHERE username='{username}'
    """
    user = cursor.execute(select_user)
    if not user:
        # Database ORM object
        insert_user = f"""
        INSERT INTO user (public_id, name, username, password)
        VALUES ('{str(uuid.uuid4())}', '{name}', '{username}', '{generate_password_hash(password)}')
        """
        # insert user
        cursor.execute(insert_user)
        conn.commit()
        cursor.close()

        successful_message = """
        <p>Successfully registered.</p><br>
        <a href='/login'>Go to Login Page</a><br>
        <a href='/'>Go to Homepage</a>
        """
  
        return make_response(successful_message, 201)
    else:
        # Returns 202 if user already exists
        already_exist_message = """
        <p>User already exists. Please Log in.</p>
        <a href='/login'>Go to Login Page</a><br>
        <a href='/'>Go to Homepage</a>
        """
        return make_response(already_exist_message, 202)

# Sorting algorithm page and method based on the url that user goes to
@app.route('/sort/<algorithm>')
@authenticate
def algorithm_page(algorithm):
    token = str(request.get_json)
    cleaned_token = re.search('\?token=(.*)\'', token).group(1)
    return sorting_page(algorithm.capitalize(), cleaned_token)

@app.route('/sort/<algorithm>', methods=['POST'])
@authenticate
def algorithm_process(algorithm):
    token = str(request.get_json)
    cleaned_token = re.search('\?token=(.*)\'', token).group(1)
    return csv_processing(f'{algorithm.capitalize()} Sort', cleaned_token)

# Result of the sorting    
@app.route('/sort/result', methods=['GET'])
@authenticate
def result():
    conn = mysql.connection
    cursor = conn.cursor()
    token = str(request.get_json)
    cleaned_token = re.search('\?token=(.*)\'', token).group(1)

    # Get results if ID is present
    if 'id' in request.args:
        id = request.args['id']

        # Search ID in the database
        selection = f"""
        SELECT *
        FROM sorts
        WHERE id={id}
        """
        cursor.execute(selection)
        result = cursor.fetchall()
        cursor.close()

        # If the data of that ID is found, return that data
        if result:
            results = result[0]
            splitted_binary = split_string(results[3], 8)
            csv_string = bin_to_str(splitted_binary)
            csv_list = col_to_row(csv_to_list(csv_string))
            table = list_to_table(csv_list)
            return f"""<p>ID : {results[0]}</p>
            <p>Date, Time : {results[1].strftime('%d %B %Y, %X')} WIB</p>
            <p>Algorithm : {results[2]}</p>
            <p>Sorting Result : {results[3]}</p>
            {table}
            <p>Execution Time : {results[4]} second(s)</p>
            <a href='/mainpage?token={cleaned_token}'>Back to Main Menu</a>
            """
        
        # If the data of that ID isn't found, return error message
        else:
            return f"<p>No Data Found with ID {id} in the Database!</p><a href='/mainpage?token={cleaned_token}'>Back to Main Menu</a>"
    
    # Get result if ID is not present
    else:
        selection = """
        SELECT *
        FROM sorts
        ORDER BY id DESC
        LIMIT 1
        """
        cursor.execute(selection)
        result = cursor.fetchall()
        cursor.close()

        # If there's any data in the database, return the last data
        if result:
            results = result[0]
            splitted_binary = split_string(results[3], 8)
            csv_string = bin_to_str(splitted_binary)
            csv_list = col_to_row(csv_to_list(csv_string))
            table = list_to_table(csv_list)
            return f"""<p>ID : {results[0]}</p>
            <p>Date, Time : {results[1].strftime('%d %B %Y, %X')} WIB</p>
            <p>Algorithm : {results[2]}</p>
            <p>Sorting Result : </p>
            {table}
            <p>Execution Time : {results[4]} second(s)</p>
            <a href='/mainpage?token={cleaned_token}'>Back to Main Menu</a>
            """
        
        # If no data is found in the database, return error message
        else:
            return f"<p>No Data Found in the Database!</p><a href='/mainpage?token={cleaned_token}'>Back to Main Menu</a>"

if __name__ == '__main__':
    app.run()
