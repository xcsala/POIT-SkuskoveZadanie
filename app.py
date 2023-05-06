from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import math
import time
import json
import serial
import pymysql
import configparser as ConfigParser

from dataUtils import *

async_mode = None

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
dbFlag = False


def background_thread(args):
    ser=serial.Serial("/dev/tty.usbmodem11201", 9600)
    db = pymysql.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    count = 0
    flag = 0
    dataList = []
    btnV=""
    oldDigitalArduino = 1
    sensorFlag = True
    while True:
        read_ser=ser.readline()
        arduinoData = parseArduinoData(read_ser)
        if(int(arduinoData[1]) == 0 and oldDigitalArduino != int(arduinoData[1])):
            sensorFlag = not sensorFlag
        oldDigitalArduino = int(arduinoData[1])
        # print(sensorFlag)
        if args:
          A = dict(args).get('A')
          btnV = dict(args).get('btn_value')
          dbFlag = dict(args).get('dbFlag')
        #   print(dbFlag)
        else:
          A = 1
        
        if btnV == "start":
            if sensorFlag:
                flag = 1
            elif not sensorFlag:
                flag = 0
        elif btnV == "stop":
            flag = 0
        else:
            flag = 0
            
        if flag == 1:
            socketio.sleep(2)
            count += 1
            dataDict = {
                "t": time.time(),
                "x": count,
                "analog": arduinoData[0],
                "digital": arduinoData[1],
                "humidity": float(arduinoData[2]) * float(A),
                "temperature": float(arduinoData[3]) * float(A),
                "amplitude" : float(A)
            }
            print(dataDict)
                # "y": float(A) * prem}
            dataList.append(dataDict)
            json_object = json.dumps(dataDict, indent=4)
            # print(json_object)
            # if len(dataList) > 0:
            #     # print(str(dataList))
            #     print(str(dataList).replace("'", "\""))
            socketio.emit('data_response', {'data': json_object, 'count': count}, namespace='/test')
        else:
            if len(dataList) > 0:
                dataStr = str(dataList).replace("'", "\"")
                cursor = db.cursor()
                cursor.execute("INSERT INTO poit (data) VALUES (%s)", (dataStr))
                db.commit()
                dataList = []
                count = 0         
    db.close()
            


@app.route('/')
def index():
    return render_template('index.html',async_mode=socketio.async_mode)

@app.route('/db')
def db():
    db = pymysql.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM poit")
    data = cursor.fetchall()
    return str(data)

@app.route('/dbdata/<string:num>', methods=['GET', 'POST'])
def dbdata(num):
  db = pymysql.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute("SELECT * FROM poit WHERE id=%s", num)
  data = cursor.fetchone()
  return str(data)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})
    
@socketio.on('open', namespace='/test')
def test_open(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': "Opened", 'count': session['receive_count']})

@socketio.on('click_event', namespace='/test')
def db_message(message):
    session['btn_value'] = message['value']
 
@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['A'] = message['value']
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})
    
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
