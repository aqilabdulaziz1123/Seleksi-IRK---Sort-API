import mysql.connector
from database import cursor


DB_NAME = "sort_api"
TABLE_NAME = "sort"

table_query_sort = (
    "create table `{}`(".format(TABLE_NAME)+
    " `id` int auto_increment not null primary key,"
    " `tanggal_waktu` datetime not null,"
    " `algoritme` varchar(30),"
    " `hasil_sorting` varchar(10000),"
    " `waktu_eksekusi` float)"
)
def create_db():
    cursor.execute("create database if not exists {} default character set 'utf8'".format(DB_NAME))

    print(DB_NAME, "created!")

def create_table(query):
    cursor.execute("USE {}".format(DB_NAME))
    try:
        cursor.execute("drop table sort")
    except:
        print("table can't be dropped!")
    cursor.execute(query)
    print("table created")

def init_db():
    create_db()
    create_table(table_query_sort)


if __name__ == "__main__":
    init_db()