import Mydb


class UserCategory:
    def __init__(self, userName):
        self.userName = userName

    def bringNameList(self):
        allNameList=[]
        try:
            myStockDB = Mydb.Mydb('info_data')
            myStockDB.db_execute("select * from stock_code;")
            sql = "select * from stock_code;"
            myStockDB.db_execute(sql)
            allNameList = myStockDB.db_fetch()
            myStockDB.db_close()
        except:
            print("e")
        return allNameList

    def bringUserStockData(self):
        sql = ("select * from user_stock where user_id = '" + self.userName + "';")
        userStockData=[]
        try:
            myStockDB = Mydb.Mydb('info_data')
            myStockDB.db_execute(sql)
            userStockData = myStockDB.db_fetch()
            myStockDB.db_close()
        except:
            print("e")
        return userStockData
