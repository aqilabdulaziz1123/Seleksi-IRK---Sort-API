import mysql.connector
from database import cursor


DB_NAME = "sort_api"
TABLE_NAME = "sort"
USER_TABLE_NAME = "user"

table_query_sort = (
    "create table `{}`(".format(TABLE_NAME)+
    " `id` int auto_increment not null primary key,"
    " `tanggal_waktu` datetime not null,"
    " `algoritme` varchar(30),"
    " `hasil_sorting` varchar(10000),"
    " `waktu_eksekusi` float)"
)
table_query_user = (
    "create table `{}`(".format(USER_TABLE_NAME)+
    " `email` varchar(64) unique not null primary key,"
    " `hashed_password` varchar(64) not null)"
)
def create_db():
    try:
        cursor.execute("drop database {}".format(DB_NAME))
    except:
        pass
    cursor.execute("create database if not exists {} default character set 'utf8'".format(DB_NAME))

    print(DB_NAME, "created!")

def create_table(query, table_name):
    cursor.execute("USE {}".format(DB_NAME))
    try:
        cursor.execute("drop table {}".format(table_name))
    except:
        print("table can't be dropped!")
    cursor.execute(query)
    print("table created")

def init_db():
    create_db()
    create_table(table_query_sort, TABLE_NAME)
    create_table(table_query_user, USER_TABLE_NAME)


if __name__ == "__main__":
    init_db()