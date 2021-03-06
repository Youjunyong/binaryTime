from . import api
from flask import jsonify, request, Blueprint, session, redirect ,flash
from models import db , MyUser , SaveTime , LoadTime
import requests


@api.route('/plustime' , methods=["GET", "POST"])
def plustime():
    if request.method == "POST":
        timeType = request.form['timeType']
        time = request.form['Time']
        
        userEmail = session.get('userEmail', None)
        save = SaveTime
        save.saveTime(userEmail , time, timeType)
        if 'Start' in timeType :
            return jsonify({'result':'success','msg':'Plustime 시작'})
        elif 'End' in timeType :
            return jsonify({'result':'success','msg':'Plustime 끝'})


@api.route('/minustime' , methods=["GET", "POST"])
def minustime():
    if request.method == "POST":
        timeType = request.form['timeType']
        time = request.form['Time']
        userEmail = session.get('userEmail', None)
        save = SaveTime
        save.saveTime(userEmail , time, timeType)
        if 'Start' in timeType :
            return jsonify({'result':'success','msg':'MinusTime 시작'})
        elif 'End' in timeType :
            return jsonify({'result':'success','msg':'MinusTime 끝'})

@api.route('/chart' , methods = ["GET", "POST"])
def chart():
    userEmail = session.get('userEmail', None)
    loadtime = LoadTime
    if request.method == 'GET':
        dateList = loadtime.chartList(userEmail)
        return jsonify({'result': 'success','msg':'list 연결되었습니다!' , 'dateList' : dateList })

    elif request.method == 'POST':
        date = request.form['date']
        month , day= date.split("-")
        # day = loadtime.NumDateToStr(date)[0]
        # month = loadtime.NumDateToStr(date)[1]
        # a = loadtime.loadDay(userEmail, month , day)
        a = loadtime.loadDay(userEmail, month , day)
        
        return jsonify({'result': 'success','msg':'GET!!' , 'timeInfo' : a})

    
@api.route('/timelist' , methods = ["GET", "POST", "DEL"])
def timelist():
    userEmail = session.get('userEmail', None)
    loadtime = LoadTime

    if request.method == 'GET':
        todayMonth = loadtime.todaysDate()[1]
        todayDay = loadtime.todaysDate()[0]
        timeList = []
        timeList.extend(list(db.plus.find({"$and" : [{'userEmail':userEmail},{'day':todayDay},{'month':todayMonth}]},{'_id' : 0})))
        timeList.extend(db.minus.find({"$and" : [{'userEmail':userEmail},{'day':todayDay},{'month':todayMonth}]}, {'_id' : 0}))
        timeList.sort(key=lambda x:x['startTime'])
        status = loadtime.NowStatus(userEmail)
        startTime = 0

        if len(status) != 1:
            startTime = status[1]
        return jsonify({'result': 'success','msg':'list 연결되었습니다!' , 'timeList' : timeList ,'status' : status[0] ,'startTime' : startTime})

    elif request.method == 'POST':
        article = request.form['article']
        time = request.form['time']
        timeType = request.form['timeType']
        if timeType == 'blueList':
            timeType = '+ Start'
        else:
            timeType = '- Start'
        startTime, endTime = time.split(' ~ ')
        SaveTime.saveArticle(userEmail ,timeType, article, startTime ,endTime)
        return jsonify({'result': 'success','msg':'입력완료' })

    elif request.method == "DEL":
        time = request.form['time']
        timeType = request.form['timeType']
        if timeType == 'blueList':
            timeType = '+ Start'
        else:
            timeType = '- Start'
        startTime, endTime = time.split(' ~ ')
        LoadTime.DelList(userEmail ,timeType, startTime ,endTime)
        return jsonify({'result': 'success','msg':'삭제완료' })

