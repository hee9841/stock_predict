import pymysql
class Mydb:
    # conn = None
    # curs = None

    def __init__(self, dname):
        self.dname = dname
        self.conn = pymysql.connect(host='localhost', user='root', password='hee7716', db = self.dname, charset='utf8',)
        self.curs = self.conn.cursor()

    def db_execute(self, query):
        self.query = query
        self.curs.execute(self.query)

    def db_commit(self):
        self.conn.commit()

    def db_fetch(self):
        rows = self.curs.fetchall()
        return rows

    def db_close(self):
        self.conn.close()
