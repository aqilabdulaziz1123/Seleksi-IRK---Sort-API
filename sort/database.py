from sort import cursor, conn

def add_to_database(tanggal, algoritma, hasil, duration):
    # conn = connection()
    # cursor = conn.cursor()
    sql = "INSERT INTO SORTS.SORTS (tanggal, algoritma, hasil, duration) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, (tanggal,algoritma,hasil,duration))
    print("Record inserted")
    conn.commit()

def get_latest_id():
    # conn = connection()
    # cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM SORTS")
    return cursor.fetchone()[0]

def get_data(id):
    # conn = connection()
    # cursor = conn.cursor()
    sql = "SELECT hasil FROM SORTS WHERE id=%s"
    cursor.execute(sql, (id,))
    return cursor.fetchone()[0]