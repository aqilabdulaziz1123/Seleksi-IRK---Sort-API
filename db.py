import mysql.connector as mysql


class Database:
    @staticmethod
    def init_connection():
        return mysql.connect(
            host="localhost",
            user="root",
            password="",
        )

    @staticmethod
    def create_connection():
        return mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="sort_api"
        )

    @staticmethod
    def init():
        mydb = Database.init_connection()
        cursor = mydb.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS sort_api")
        cursor.execute("USE sort_api")
        cursor.execute("CREATE TABLE IF NOT EXISTS sorts (id INT AUTO_INCREMENT PRIMARY KEY, waktu TIMESTAMP DEFAULT current_timestamp(), algoritma VARCHAR(100), hasil BLOB, execution_time DOUBLE)")
        mydb.commit()

    @staticmethod
    def create(algoritma, hasil, execution_time):
        mydb = Database.create_connection()
        cursor = mydb.cursor()
        query = (
            "INSERT INTO sorts (algoritma, hasil, execution_time) VALUES (%s, %s, %s)")
        data = (algoritma, hasil, execution_time)
        cursor.execute(query, data)
        mydb.commit()

    @staticmethod
    def read():
        mydb = Database.create_connection()
        cursor = mydb.cursor()
        query = "SELECT * FROM sorts ORDER BY ID DESC LIMIT 1"
        cursor.execute(query)
        (_, _, _, res, _) = cursor.fetchone()
        return res

    @staticmethod
    def read_by_id(id):
        mydb = Database.create_connection()
        cursor = mydb.cursor()
        query = "SELECT * FROM sorts WHERE id = " + id
        cursor.execute(query)
        (_, _, _, res, _) = cursor.fetchone()
        return res
