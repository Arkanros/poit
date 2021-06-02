from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect  
import time
import random
import time
import random
import math
import serial # pre arduino connection
import MySQLdb    
import configparser as ConfigParser

async_mode = None

config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')
print(myhost)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 
ser = serial.Serial('/dev/ttyS1', 9600)
ser.flushInput()
stop = 1

    
def background_thread(args):
    
    stop = dict(args).get('stop')
    count = 0    
    dataList = []     
    A = [] 
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb) 
      
    while True:
        
          stop = dict(args).get('stop')
          if stop:
            
            A = ser.readline().decode('ascii')
          
            btnV = dict(args).get('btn_value')
         
            if len(A)>0:
                print("4a")
                fuj = str(A).replace("'", "\"")
                cursor = db.cursor()
                cursor.execute("SELECT MAX(id) FROM Test")
                maxid = cursor.fetchone()
                cursor.execute("INSERT INTO Test (id, hodnoty) VALUES (%s, %s)", (maxid[0] + 1, fuj))
                db.commit()
               
                dataCounter = 0
                
                f = open("demofile2.txt", "a")
                f.write(fuj)
                f.write("\n")
                f.close()
           
                dataList = []
                
                socketio.emit('my_response',
                                {'data': A, 'count': 0},
                          namespace='/test')  
                 #db.close()
         
@app.route('/', methods=['GET', 'POST'])                                    
def gauge():                                                                
    return render_template('index.html', async_mode=socketio.async_mode)    

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
       
@app.route('/graphlive', methods=['GET', 'POST'])
def graphlive():
    return render_template('graphlive.html', async_mode=socketio.async_mode)
      
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
    
@socketio.on('open_request', namespace='/test')
def test_connect():
    print("connected")
    global thread
    with thread_lock:
        if thread is None:
            print("abcde")
            session["stop"]=1
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
        
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('Stop_request', namespace='/test')
def Stop_connect():
    print("Zastavene")
    
    session["stop"]=0
    print("stop connect:",session["stop"])
    emit('my_response', {'data': 'Zastavujem...', 'count': 0})
    
@socketio.on('Start_request', namespace='/test')
def Start_connect():
    print("Spustam...")
    
    session["stop"]=1
    print("stop connect:",session["stop"])
    emit('my_response', {'data': 'Spustam...', 'count': 0})

@app.route('/dbdata/<string>', methods=['GET', 'POST'])
@socketio.on('Vypis1_request', namespace='/test')
def Vypis1_connect():
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute("SELECT hodnoty FROM Test")
  vyp = cursor.fetchall()

  
  emit('my_response', {'data': str(vyp), 'count': 0})
 
@app.route('/read/<string>')  
@socketio.on('Vypis2_request', namespace='/test')
def readfile():
    fo = open("demofile2.txt","r")
    rows = fo.readlines()
    emit('my_response', {'data': rows, 'count': 0})
    return rows
 
 
 
@socketio.on('my_event1', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    print(message,"event")
    print(message['value'])
    temp = message['value']    
    print(str(temp).encode('utf-8'))    
    ser.write(str(temp).encode('utf-8'))
    
@socketio.on('click_event', namespace='/test')
def db_message(message):   
    session['btn_value'] = message['value']    

@socketio.on('slider_event', namespace='/test')
def slider_message(message):  
    print (message['value'] )  
    session['slider_value'] = message['value']
    

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
