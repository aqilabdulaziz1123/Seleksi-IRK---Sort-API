import mysql.connector
from decouple import config
import array, csv, io

global mydb

def convertHTMLTable(input):
	html = "<table>\n"
	first = True
	for row in input:
		if first:
			html += "<thead>\n<tr>\n<td>" + "</td>\n<td>".join(map(str,row)) + "</td>\n</tr>\n</thead>\n"
			first = False
			html += "<tbody>\n"
			continue
		html += "<tr>\n<td>" + "</td>\n<td>".join(map(str,row)) + "</td>\n</tr>\n"

	return html + "</tbody>\n</table>"

def select(id):
    DBPASS = config('DB_PASS')
    DBNAME = config('DB_NAME')
    DBHOST = config('DB_HOST')
    DBUSER = config('DB_USER')

    mydb = mysql.connector.connect(
      host=DBHOST,
      user=DBUSER,
      password=DBPASS,
      database=DBNAME
    )
    mycursor = mydb.cursor()

    query = "SELECT hasil_sorting FROM sorts "

    if (int(id)<0):
        query += "ORDER BY time DESC"
    else:
        query += "WHERE id=" + str(id)
    query += " LIMIT 1"

    print(query)
    mycursor.execute(query)
    data = mycursor.fetchone()
    if data != None:
        data = data[0].replace('(',"").replace(')',"")
        table = data.split(';')
        for i in range(len(table)):
            table[i] = table[i].split(',')
        return convertHTMLTable(table)
    else:
        return {'Error':"Data doesn't exist!"}

def insert(algoritma,hasil,file,execTime):
    # database credentials
    DBPASS = config('DB_PASS')
    DBNAME = config('DB_NAME')
    DBHOST = config('DB_HOST')
    DBUSER = config('DB_USER')

    mydb = mysql.connector.connect(
      host=DBHOST,
      user=DBUSER,
      password=DBPASS,
      database=DBNAME
    )
    mycursor = mydb.cursor()

    temp = "("
    first = True
    for row in hasil:
        if first:
            first = False
        else :
            temp += ';'
        temp += "(" + ','.join(map(str,row)) +")"
    temp += ")"
    temp = "'" + temp.replace('\\',"\\\\").replace("'","\\'").replace('"','\\"') + "'"
    # print(test)

    query = "INSERT INTO sorts (algoritma,hasil_sorting,execution_time) VALUES ({0},{1},{2})".format('\''+algoritma+'\'',temp,execTime)
    values = "({0},{1},{2})".format('\''+algoritma+'\'',temp,execTime)
    # print(query)
    mycursor.execute(query)
    mydb.commit()

if __name__ == "__main__":
    # test = "\\x02\\23"
    # print(test.replace('\\',"\\\\").replace("'","\\'").replace('"','\\"'))
    print(select("2"))
