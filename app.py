from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import pandas as pd
import csv
from os import remove
import bcrypt

from math import e, floor
from sort_algo import selection_sort
from database import db,cursor
from setup import DB_NAME, TABLE_NAME, USER_TABLE_NAME, init_db

UPLOADED_DATA_PATH = "./"

app = Flask(__name__)

# CONFIG(S)
app.config['UPLOAD_FOLDER'] = UPLOADED_DATA_PATH
app.config['JWT_KEY'] = "this_key_is_not_secured_but_works"
print(UPLOADED_DATA_PATH)



# ROUTE(S)
@app.route('/init_db', methods=["POST"])
def init_database():
    global init_db
    init_db()
    return redirect(url_for('main'))

@app.route('/login', methods=["GET","POST"])
def login():
    global DB_NAME, USER_TABLE_NAME
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        cursor.execute("USE {}".format(DB_NAME))
        cursor.execute("SELECT * FROM {} WHERE email='{}'".format(USER_TABLE_NAME, email))
        user = cursor.fetchall()
        if len(user) != 1:
            return render_template("login.html")
        user = user[0]

        # CHECKING PASSWORD
        if bcrypt.checkpw(request.form["password"].encode(), user[1].encode()):
            print("Login berhasil. Halo {}!".format(user[0]))
            return render_template("index.html")

        return render_template("login.html")

@app.route('/signup', methods=["GET","POST"])
def signup():
    global db, DB_NAME, USER_TABLE_NAME
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        email = request.form["email"]
        hashed_password = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt(14)).decode()
        print("email:", email)
        print("hashed password:", hashed_password, "| type:", type(hashed_password))
        cursor.execute("USE {}".format(DB_NAME))
        cursor.execute("INSERT INTO {} (email, hashed_password) VALUES('{}','{}')".format(USER_TABLE_NAME,email, hashed_password))
        db.commit()
        return render_template("login.html")


@app.route('/', methods=["POST", "GET"])
def main():
    global cursor, DB_NAME, TABLE_NAME
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute("SELECT id FROM {}".format(TABLE_NAME))
    raw_list_id = cursor.fetchall()
    list_id = []
    for i in raw_list_id:
        list_id.append(i[0])
    print(list_id)
    return render_template("index.html", list_id=list_id)

@app.route('/sort/<algo>', methods = ["POST"])
def sort_upload(algo):
    global cursor
    print(request.form)
    print(request.args)

    if request.method == "POST":
        return upload_handler(algo)
    return redirect(url_for('main'))

@app.route('/sort/result', methods = ["GET"])
def get_result():
    global cursor, DB_NAME, TABLE_NAME
    result_id = -1
    print(request.args)
    try:
        result_id = request.args["id"]
    except:
        pass

    db_data = None

    try:
        cursor.execute("USE {}".format(DB_NAME))
        if result_id == -1:
            cursor.execute("SELECT * FROM {} ORDER BY {} DESC LIMIT 1".format(TABLE_NAME, 'id'))
            pass
        else:
            cursor.execute("SELECT * FROM {} where id={}".format(TABLE_NAME, result_id))
        db_data = cursor.fetchone()
    except:
        print("error occured")
    
    if db_data == None:
        return redirect(url_for('main'))
    
    sorted_data = []
    try:
        temp = db_data[3].split('\n')
        for i in range(len(temp)):
            temp[i] = temp[i].split(',')
            for j in range(len(temp[i])):
                try:
                    temp[i][j] = int(temp[i][j])
                except:
                    temp[i][j] = temp[i][j]
        sorted_data = temp
    except:
        pass

    sorted_data = pd.DataFrame(sorted_data)
    print(sorted_data)

    print(db_data)

    # print(result_id)
    # return redirect(url_for('main'))
    return render_template("result.html", sorted_data = sorted_data.to_html(index = True, header = False), id_data = db_data[0], exec_time_in_ms = db_data[4]*1000, algorithm=db_data[2])

@app.route('/reset_table/<table_name>', methods = ["POST"])
def reset_table(table_name):
    global db,cursor, DB_NAME
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute("TRUNCATE table {}".format(table_name))
    db.commit()
    return redirect(url_for('main'))

# Helper function(s)
def insertdb_sort(tanggal_waktu, algoritme, hasil_sorting, waktu_eksekusi):
    global db,cursor,DB_NAME, TABLE_NAME
    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute("INSERT INTO {} (tanggal_waktu, algoritme, hasil_sorting, waktu_eksekusi) VALUES('{}','{}','{}','{}')".format(TABLE_NAME,tanggal_waktu, algoritme, hasil_sorting, waktu_eksekusi))
    db.commit()

def upload_handler(algo):
    global cursor
    try:
        # UPLOADING FILE (TO SOLVE PATH ISSUE)
        f = request.files["csv_uploader"]
        f.save(UPLOADED_DATA_PATH+secure_filename(f.filename))

        # READING DATA
        data = []
        with open(app.config['UPLOAD_FOLDER']+secure_filename(f.filename), 'r') as csv_file:
            csv_var = csv.reader(csv_file)
            for row in csv_var:
                temp_list = []
                for num in row:
                    try:
                        temp_list.append(int(floor(float(num))))
                    except:
                        temp_list.append(num)
                data.append(temp_list)
        
        # VALIDATION
        if len(data) == 0:
            return redirect(url_for('main'))
        if (int(request.form["selected_column"]) < 0) or ((len(data[0]) - 1) <= int(request.form["selected_column"])):
            print("ERROR....................")
            return redirect(url_for('main'))

        # SORTING
        retval = []
        if algo == "selection":
            retval = selection_sort(data[1:], int(request.form["selected_column"]), True)
        elif algo == "bubble":
            retval = selection_sort(data[1:], int(request.form["selected_column"]), True)
        elif algo == "merge":
            retval = selection_sort(data[1:], int(request.form["selected_column"]), True)

        retval["sorted_matrix"].insert(0,data[0])
        
        data = pd.DataFrame(data)
        sorted_data = pd.DataFrame(retval["sorted_matrix"])
        print(retval["sorted_matrix"][1:6])
        # END SORTING

        # FORMAT RESULT TO CSV
        csv_out = sorted_data.to_csv(index=False, header=False)[:-1]
        print(len(csv_out))
        # END FORMAT..

        # INSERTING TO DATABASE
        if len(retval["sorted_matrix"]) > 0: # masukan valid
            insertdb_sort(retval["tanggal_waktu"], algo+" sort", csv_out, retval["delta_time"])

        # CLEANING UPLOADED FILE
        remove(UPLOADED_DATA_PATH+f.filename)
        
        # GETTING DATABASE ID
        cursor.execute("SELECT id FROM sort")
        id_data = int(cursor.fetchall()[-1][0])
        print("ID data:", id_data)

        

        # return redirect(url_for('main'))
        return render_template("result.html", sorted_data = sorted_data.to_html(index = True, header = False), id_data = id_data, exec_time_in_ms = retval["delta_time"]*1000, algorithm=algo+" sort")
    except:
        return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)