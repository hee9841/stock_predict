from pandas_datareader import data
from datetime import datetime, timedelta
import pandas as pd

class  StockdataToCSV:
    def __init__(self, stockCode):
        self.stockCode = stockCode
        end_date = datetime.today()
        self.start_date = end_date + timedelta(days=-1850)

    def SaveToCSV(self):
        toCSV = data.get_data_yahoo(self.stockCode, self.start_date)
        toCSV.to_csv('../dataset/'+ self.stockCode+'.csv')
