"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db

import pymysql

import Mydb
import stockData
import UserCategory  # 사용자 주식 정보 가져오기

import numpy as np


app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# log-In
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        passw = request.form['password']
        tableName = 'user_info'
        sql = ("select user_id from user_info where user_id = '" +
               username + "' and pw = '" + passw + "';")
        try:
            loginDB = Mydb.Mydb('info_data')
            loginDB.db_execute(sql)
            checkUser = loginDB.db_fetch()
            loginDB.db_close()
            if checkUser:
                isAlert = 0
                session['logged_in'] = username
                return redirect(url_for('home'))
            else:
                isAlert = 1
                # session['logged_in'] = False
                return render_template('login.html', isAlert=isAlert)
        except:
            isAlert = 2
            return render_template('login.html', isAlert=isAlert)


# Log-OUt
@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = None
    return redirect(url_for('home'))


# UserStockPage
@app.route("/userStock", methods=['GET', 'POST'])
def userStock():
    PuserStockList = []  # 구매한 주식 정보 리스트
    PStockNamesList = []  # 구매한 주식 이름 리스트
    myData = UserCategory.UserCategory(session['logged_in'])
    allNameList = myData.bringNameList()
    userStockData = myData.bringUserStockData()
    if userStockData:
        for data in userStockData:
            if data[2] == 'P':
                PuserStockList.append(data)
        for data in PuserStockList:
            for name in allNameList:
                if name[0] == data[1]:
                    PStockNamesList.append(name[1])

    if request.method == 'GET':
        return render_template('userStock.html', PuserStockList=PuserStockList, PStockNamesList=PStockNamesList)
        # 사용자가 저장한 주식 카테로그가 'P'이면 사용자 주식 정보, 주식이름 전달
        # if PStockNamesList:
        #     return render_template('userStock.html', PuserStockList=PuserStockList, PStockNamesList=PStockNamesList)
        # else:
        #     return render_template('userStock.html')
    # POST 방식이면
    else:
        selectedStock = request.form.get('selectedStock')
        if selectedStock:
            for name in allNameList:
                if name[1] == selectedStock:
                    selectedStockCode = name[0]
            predictStock = stockData.stockData(selectedStockCode)
            # 차트 이미지로 저장
            predictStock.drawChart()
            # 종가 예측
            predictPrice = predictStock.pradiction()
            nowPrice = predictStock.ClosePrice()
            for data in PuserStockList:
                if data[1] == selectedStockCode:
                    prchasePrice = data[4]  # 매수단가
                    prchaseNum = data[5]
            # 수익률(%) = ((현재 주식가격 / 매입한 주식 가격)-1)*100
            preProfitRatio = np.round(
                (((predictPrice / prchasePrice) - 1) * 100), 2)
            nowProfitRatio = np.round((((nowPrice / prchasePrice) - 1) * 100), 2)
            strnowProfitRatio = str(nowProfitRatio)
            strnowProfitRatio = strnowProfitRatio[1:-1]
            return render_template('userStock.html', nowPrice=int(nowPrice),
                                   preProfitRatio=preProfitRatio, predictPrice=predictPrice,
                                   nowProfitRatio=strnowProfitRatio, PuserStockList=PuserStockList,
                                   PStockNamesList=PStockNamesList, selectedStockCode=selectedStockCode)
        else:
            return render_template('userStock.html', PuserStockList=PuserStockList, PStockNamesList=PStockNamesList)

# UserStockPage


@app.route("/favoriteStock", methods=['GET', 'POST'])
def favoriteStock():
    FavorStockList = []  # 구매할 주식 정보 리스트
    FStockNamesList = []  # 구매할 주식 이름 리스트
    myData = UserCategory.UserCategory(session['logged_in'])
    allNameList = myData.bringNameList()
    userStockData = myData.bringUserStockData()
    if userStockData:
        for data in userStockData:
            if data[2] == 'F':
                FavorStockList.append(data)
        for data in FavorStockList:
            for name in allNameList:
                if name[0] == data[1]:
                    FStockNamesList.append(name[1])

    if request.method == 'GET':
        return render_template('favoriteStock.html', FavorStockList=FavorStockList, FStockNamesList=FStockNamesList)
        # 사용자가 저장한 주식 카테로그가 'F'이면 사용자 주식 정보, 주식이름 전달
        # if FStockNamesList:
        #     return render_template('favoriteStock.html', FavorStockList=FavorStockList, FStockNamesList=FStockNamesList)
        # else:
        #     return render_template('favoriteStock.html')
    # POST 방식이면
    else:
        selectedStock = request.form.get('selectedStock')
        for name in allNameList:
            if name[1] == selectedStock:
                selectedStockCode = name[0]
        predictStock = stockData.stockData(selectedStockCode)
        # 차트 이미지로 저장
        predictStock.drawChart()
        # 종가 예측
        predictPrice = predictStock.pradiction()
        nowPrice = predictStock.ClosePrice()
        return render_template('favoriteStock.html', selectedStockCode=selectedStockCode, nowPrice=int(nowPrice), predictPrice=predictPrice, FavorStockList=FavorStockList, FStockNamesList=FStockNamesList)


if __name__ == '__main__':

    app.secret_key = "a03mfk$d"
    app.run(debug=True)
