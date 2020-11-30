import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from IPython.display import display
from mplfinance.original_flavor import candlestick2_ohlc

import pandas as pd
import numpy as np
import tensorflow as tf
from datetime import datetime

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Dropout, Activation

import StockdataToCSV


class stockData:
    def __init__(self, stockCode):
        self.stockCode = stockCode
        toCSV = StockdataToCSV.StockdataToCSV(self.stockCode)
        toCSV.SaveToCSV()
        self.dataset = pd.read_csv('../dataset/'+ self.stockCode+'.csv', sep=',')
        self.dataset = self.dataset.dropna()

    def drawChart(self):
        df = self.dataset
        #이동 평균선을 그리기 위해 n일간의 값의 산술평균
        df['MA5'] = df['Close'].rolling(5).mean()
        df['MA10'] = df['Close'].rolling(10).mean()
        df['MA20'] = df['Close'].rolling(20).mean()

        df = df[-30:]
        #인덱스 설정
        dateindex = df.Date.astype('str')

        df = df[['Open', 'High', 'Low', 'Close', 'Volume','MA5', 'MA10', 'MA20']]

        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)

        ax.plot(dateindex, df['MA5'], label='MA5', linewidth=0.7)
        ax.plot(dateindex, df['MA10'], label='MA10', linewidth=0.7)
        ax.plot(dateindex, df['MA20'], label='MA20', linewidth=0.7)

        # x축을 60도로 회전
        plt.xticks(rotation=60)
        # X축 티커 숫자 30개로 제한
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

        ax.set_title(self.stockCode, fontsize=22)
        ax.set_ylabel("Price")
        # ax.set_xlabel('Date')

        # 차트 저장

        candlestick2_ohlc(ax, df['Open'], df['High'], df['Low'],
                          df['Close'], width=0.5, colorup='r', colordown='b')
        fig1 = plt.gcf()
        ax.legend()
        plt.grid()
        plt.savefig("./static/img/" + self.stockCode + '.png', dpi=300)

    # 종가 예측 함수
    def pradiction(self):
        df = self.dataset[['Close']]
        df = np.array(df)
        new_windows = df[-10:]

        # 데이터 정규화
        standardized_data = []

        for p in new_windows:
            tandardized_window = ((p - np.mean(new_windows)) / (np.std(new_windows)))
            standardized_data.append(tandardized_window)

        #데이터 모양 변화
        windows = np.array(standardized_data)
        x = windows
        x = np.reshape(x,(1,x.shape[0], x.shape[1]))

        model = tf.keras.models.load_model('./model/' + self.stockCode + '.h5')
        temp = model.predict(x)
        result = (temp * np.std(new_windows)) + np.mean(new_windows)
        price = result[0][0]
        return price

    #현재 종가
    def ClosePrice(self):
        df = self.dataset[['Close']]
        df = np.array(df)
        Price = df[-1]
        return Price
