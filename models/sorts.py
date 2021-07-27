from mysql.connector import connect

class database:
    def __init__(self):
        try:
            self.db = connect(host='localhost',
                              database='sortdb',
                              user='root',
                              password='taisanta')
        except Exception as e:
            print(e)
    
    def postSort(self, **params):
        try:
            print(params["algorithm"])
            cursor = self.db.cursor()
            post_query ='''insert into sorts (algorithm, result, exec_time) values ('{0}', '{1}', {2})'''.format(
                params["algorithm"], params["result"], params["exec_time"]
            )
            print(post_query)
            cursor.execute(post_query)
            self.db.commit()
            return "Insert Success"
        except Exception as e:
            print(e)
    
    def getSort(self, id=None):
        try:  
            cursor = self.db.cursor()
            if(id is None):
                query ='''select * from sorts order by date_time desc limit 1;'''
            else:
                query ='''select * from sorts where id = {0};'''.format(id)
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(e)