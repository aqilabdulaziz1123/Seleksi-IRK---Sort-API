from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import pandas as pd
import csv
from os import remove

from math import floor
from sort_algo import selection_sort
from database import db,cursor
from setup import DB_NAME, TABLE_NAME, init_db

UPLOADED_DATA_PATH = "./"

app = Flask(__name__)

# CONFIG(S)
app.config['UPLOAD_FOLDER'] = UPLOADED_DATA_PATH
print(UPLOADED_DATA_PATH)



# ROUTE(S)
@app.route('/init_db', methods=["POST"])
def init_database():
    global init_db
    init_db()
    return redirect(url_for('main'))

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

@app.route('/sort/selection', methods = ["POST"])
def sort_selection():
    global cursor
    print(request.form)
    print(request.args)

    try:
        if request.method == "POST":
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
                insertdb_sort(retval["tanggal_waktu"], "selection sort", csv_out, retval["delta_time"])

            # CLEANING UPLOADED FILE
            remove(UPLOADED_DATA_PATH+f.filename)
            
            # GETTING DATABASE ID
            cursor.execute("SELECT id FROM sort")
            id_data = int(cursor.fetchall()[-1][0])
            print("ID data:", id_data)

            

            # return redirect(url_for('main'))
            return render_template("result.html", sorted_data = sorted_data.to_html(index = True, header = False), id_data = id_data, exec_time_in_ms = retval["delta_time"]*1000)
    except:
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
    return render_template("result.html", sorted_data = sorted_data.to_html(index = True, header = False), id_data = db_data[0], exec_time_in_ms = db_data[4]*1000)

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

if __name__ == "__main__":
    app.run(debug=True)