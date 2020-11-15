# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

import pandas as pd
import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense,LSTM,Dropout, Activation
import datetime

#플라스크 객체를 app에 할당
app = Flask(__name__)

#데이터 불러오기
dataset = pd.read_csv('../dataset/005930.KS.csv', sep=',')
data = dataset.dropna()

df=data[['Close']]
df=np.array(df)

#예측을 위한 윈도우 생성
new_windows = df[-10:]


#윈도우 정규화
standardized_data=[]

for p in new_windows:
    tandardized_window = ((p - np.mean(new_windows)) / (np.std(new_windows)))
    standardized_data.append(tandardized_window)


#데이터 모양 변화
windows = np.array(standardized_data)

x = windows
x = np.reshape(x,(1,x.shape[0], x.shape[1]))


#app객체를 이용해 라우팅 경로를 설정해줌
#해당 라우팅 경로로 요청이 올 때 실행할 함수를 바로 밑에 작성
@app.route("/", methods=["GET", 'POST'])

def model():
    if request.method == 'GET':
        return render_template('mainPage.html') #html파일 넘겨줌
    if request.method == 'POST':
        model = tf.keras.models.load_model('./model/test5_model.h5')
        temp = model.predict(x)
        result = (temp * np.std(new_windows)) + np.mean(new_windows)
        price = result[0][0]
        return render_template('prediction.html', price=price)

if __name__ == '__main__':
    app.run(debug=True)
