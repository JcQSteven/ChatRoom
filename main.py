#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 12:55 PM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : main.py
# @Software: PyCharm
from flask import Flask,render_template,request
from flask_socketio import SocketIO,emit,disconnect
app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
user={}

@app.route('/')
def index():
    return render_template('test.html')


@socketio.on('client_event')
def client_msg(msg):
    name=msg["name"].strip()
    data=msg['data']
    print(name+data)
    if(name=="" or data==""):
        pass
    else:
        emit('res',{'name':name,'data':data},broadcast=True)

@socketio.on('register_client')
def register(msg):
    sid = request.sid
    name = msg["name"].strip()
    if(user.get(name)==None and name!=""):
        user.update({name:sid})
    else:
        disconnect(sid)

@socketio.on('connect')
def test_connect():
    emit('res', {'name':'System','data': 'New person join in'}, broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    quit_client=""
    for name,sid in user.items():
        if sid==request.sid:
            emit('res', {'name': 'System', 'data': name+' leave '}, broadcast=True)
            del user[name]
            break

    print('%s disconnected'%quit_client)

if __name__ == '__main__':
    socketio.run(app, host='192.168.10.14',debug=True)