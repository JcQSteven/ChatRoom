#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/27 12:55 PM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : main.py
# @Software: PyCharm
from flask import Flask,render_template,request,jsonify,send_from_directory
from flask_cors import *
from flask_socketio import SocketIO,emit,disconnect
import os


app=Flask(__name__)
CORS(app,resource=r'/*')
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'upload'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
basedir = os.path.abspath(os.path.dirname(__file__))
socketio = SocketIO(app)
user={}

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('client_event')
def client_msg(msg):
    decode_msg(msg)
    name=msg["name"]
    data=msg['data']
    if(name=="" or data==""):
        pass
    else:
        if(data=='showall'):
            totalName='、'.join(list(user.keys()))
            emit('res', {'name': 'System', 'data': '【当前在线人数 %d】%s' % (len(user),totalName)}, broadcast=True)
        else:
            emit('res',{'name':name,'data':data},broadcast=True)

@socketio.on('register_client')
def register(msg):
    decode_msg(msg)
    sid = request.sid
    name = msg["name"].strip()
    if(len(name)>5):
        name=name[0:5]
    if(user.get(name)==None and name!=""):
        user.update({name:sid})
    else:
        disconnect(sid)

@socketio.on('connect')
def test_connect():
    emit('res', {'name':'System','data': '有新人加入【当前在线人数 %d】'%(len(user)+1)}, broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    quit_client=""
    for name,sid in user.items():
        if sid==request.sid:
            emit('res', {'name': 'System', 'data': name+' 离开了【当前在线人数 %d】'%(len(user)-1)}, broadcast=True)
            del user[name]
            break
    print('%s disconnected'%quit_client)

@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f=request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(f)
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        (f.filename).replace('../','')  #过滤跨路径上传
        file_list=os.listdir(file_dir)
        if f.filename in file_list.index:#防止文件重复覆盖
            f.filename="重名文件"+f.filename
        f.save(os.path.join(file_dir, f.filename))  #保存文件到upload目录
        return jsonify({"errmsg": "success"})
    else:
        return jsonify({"errmsg": "fail"})

@app.route('/loadfile',methods=['POST'])
def api_loadfile():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    data = os.listdir(file_dir)
    data = ','.join(data)
    return jsonify({"data": data})

@app.route("/download/<path:filename>")
def downloader(filename):
    dirpath = os.path.join(app.root_path, 'upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载

def decode_msg(msg):
    for i in msg:
        msg[i]=msg[i].encode('latin-1').decode('utf-8')
    return msg

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
if __name__ == '__main__':
    socketio.run(app, host='192.168.10.14',debug=True)