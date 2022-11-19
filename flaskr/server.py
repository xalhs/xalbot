import os
#import db
from flask import Flask, render_template, jsonify

from flask import url_for
from flask import request, send_from_directory

# <script type="text/javascript" {{ url_for('static', filename='app.js')}}></script>
#from db import get_db
from flask_socketio import SocketIO

from flask_socketio import send, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
import json

from threading import Event
import threading
import time
import asyncio
from math import ceil

import pandas as pd
import random
MY_AUTH = "" #add some random string here
#init_db()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/' , methods=['GET', 'POST'])
    def hello2():
    #    videoID = ""
    #    videoID = remove_song()
        if request.method == 'POST':
            print("POSTED")
            list1 = database_to_list()
            return(list1)

        list1 = database_to_list()
        print(list1)
        return render_template('server_template.html', data= [list1])

    @app.route('/sr' , methods=['GET', 'POST'])
    def sr2():
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("POSTED")
            nam = add_song(request.json['data'])
            if nam == "error":
                return json.dumps({"error": "song already in queue"})
            print("requested")
            print(request.json)
            return json.dumps({"data": nam})

    @app.route('/skip' , methods=['GET', 'POST'])
    def skip():
        #if request.method == 'GET':
        #    remove_song()
        #    return("success")
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            list1 = database_to_list()
            for i, item in enumerate(list1):
                if item['videoID'] == request.json['data']:
                    if i == 0:
                        socketio.emit('skip' , ("foo" , "bar") )
                        return json.dumps({"data": "success"})
                    else:
                        socketio.emit('removesong' , (i , item['videoID']) )
                        remove_song(i)
                        return json.dumps({"data": "success"})
            return json.dumps({"data": "couldn't find"})

    @app.route('/hardskip' , methods=['GET', 'POST'])
    def hardskip():
        if request.method == 'GET' and request.headers['Authorization'] == MY_AUTH:
            socketio.emit('skip' , ("foo" , "bar") )#, namespace='/' )
            return("success")
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            socketio.emit('skip' , ("foo" , "bar") )#, namespace='/' )
            return json.dumps({"succ" : "ess"})

    @app.route('/hello' , methods=['GET', 'POST'])
    def hello():
        if request.method == 'POST':# and request.headers['Authorization'] == MY_AUTH:
            print("Postad")
            videoID = remove_song()
            skippers = []
            list1 = database_to_list()
            return jsonify({"data": [list1 , videoID]})

    @app.route('/queue' , methods=['GET', 'POST'])
    def queue():
        if request.headers['Authorization'] == MY_AUTH:
    #    if(socket.rooms.indexOf("room1") == 0):  ADD A WAY TO SEE IF CLIENT IS CONNECTED
    #        return(jsonify({"data" : []}))

            global ev
            global result
            global notdone
            ev = threading.Event()
            result = {"toto" : "tata"}
        #thread2= threading.Thread(target = emit_it_LUL , args = (ack,))
        #thread2.start()
            socketio.start_background_task(target=emit_it_LUL)
            notdone = True
            pause_until_done()
            return jsonify(result)
            try:
                pass


            except:
                print("987765")
                return result



    @app.route('/play' , methods=['GET', 'POST'])
    def playsong():
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("play")
            socketio.emit('play'  , ("foo") , to= "room1" )
            return json.dumps({"data": "success"})


    @app.route('/pause' , methods=['GET', 'POST'])
    def pausesong():
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("pausing")
            socketio.emit('pause'  , ("foo")  , to= "room1" )
            return json.dumps({"data": "success"})

    @app.route('/setvolume' , methods=['GET', 'POST'])
    def setvolume():
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("voluming")
            vol = request.json['data']['volume']
            socketio.emit('volume'  , (vol)  , to= "room1" )
            return json.dumps({"data": "success"})

        # socketio.emit('volume'  , ("foo")  , to= "room1" )
        # return json.dumps({"data": "success"})

    @app.route('/voteskip' , methods=['GET', 'POST'])
    def voteskip():
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("voteskipping")
            user = request.json['data']['user']
            if user in skippers:
                return json.dumps({"data": user + ", you already voted to skip the song"})

            skippers.append(user)
            first_song = sr.query.first()
        #    list1 = database_to_list()
            active_chatters = request.json['data']['active_chatters']
    #        v_need = list1[0]['votes_needed']
    #        v_got = list1[0]['votes_needed']
            first_song.votes_gotten += 1
            if first_song.votes_needed  == None:
                first_song.votes_needed = ceil((active_chatters+1)/2)

            if first_song.votes_gotten == first_song.votes_needed:
                socketio.emit('greetings' , ("foo" , "bar") )
                return json.dumps({"data": "skipped song: " + first_song.title })
            else:
                db.session.commit()
                return json.dumps({"data": str(first_song.votes_gotten) + " out of  " + str(first_song.votes_needed) + " votes needed to skip the current song"})

    @app.route('/playsound' , methods=['GET', 'POST'])
    def playsound():
        print(request.headers)
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("PLAYSOUND POSTED")
            socketio.emit('playsound'  ,( (request.json['data']['playsound']) , (request.json['data']['type'])) , to= "room1" )
            print(request.json)
            return json.dumps({"data": "success"})
        # else:
        #     socketio.emit('playsound'  , ("Allo" , ".mp3")  , to= "room1" )
        #     print("yourdad")
        #     return("yourdad")
    @app.route('/specialplaysound' , methods=['GET', 'POST'])
    def specialplaysound():
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("PLAYSOUND POSTED")
            socketio.emit('specialplaysound'  ,( (request.json['data']['specialplaysound']) , (request.json['data']['type'])) , to= "room1" )
            print(request.json)
            return json.dumps({"data": "success"})
        # else:
        #     socketio.emit('specialplaysound'  , ("AlloWAYTOODANK" , ".mp3")  , to= "room1" )
        #     print("yourdad")
        #     return("yourdad")
    @app.route('/tts' , methods=['GET', 'POST'])
    def tts():
        if request.method == 'POST' and request.headers['Authorization'] == MY_AUTH:
            print("TTS POSTED")
            socketio.emit('tts'  ,( (request.json['data']['tts_filename']) , (request.json['data']['type'])) , to= "room1" )
            print(request.json)
            return json.dumps({"data": "success"})
        # else:
        #     socketio.emit('tts'  , ("test" , ".mp3")  , to= "room1" )
        #     print("yourfather")
        #     return("yourfather")
    @app.route('/playsounds/<path:filename>')
    def download_file_simple(filename):   #change filename to your location
        print("sending from dir " + 'D:/Users/XALHS/pyth/var/playsounds/' + filename)
        return send_from_directory('D:/Users/XALHS/pyth/var/playsounds/' , filename)
    @app.route('/specialplaysounds/<path:filename>')
    def download_file_special(filename):
        print("sending from dir " + 'D:/Users/XALHS/pyth/var/specialplaysounds/' + filename)
        return send_from_directory('D:/Users/XALHS/pyth/var/specialplaysounds/' , filename)
    @app.route('/tts/<path:filename>')
    def download_tts_simple(filename):
        print("sending from dir " + 'D:/Users/XALHS/pyth/var/tts/' + filename)
        return send_from_directory('D:/Users/XALHS/pyth/var/tts/' , filename)
    @app.route('/Resources/music/<path:filename>')
    def download_music(filename):
        print("sending from dir " + 'D:/Users/XALHS/pyth/var/Resources/music/' + filename)
        return send_from_directory('D:/Users/XALHS/pyth/var/Resources/music/' , filename)

    return app

def pause_until_done():
    global notdone
    while notdone:
        print("cycle")
        socketio.sleep(0.1)


def ack(data):
    print(data)
    global result
    global ev
    global notdone

    result = {'data': data}
    notdone = False
    #ev.set()

def emit_it_LUL():
    print("nam")
    socketio.emit('status2'  , ("foo") , to= "room1" , callback = ack)
    print("nam2")
    #ev.set()


class StupidError(Exception):
    pass

app = create_app()
app.config['SECRET_KEY'] = 'secret!'


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db = SQLAlchemy(app)
socketio = SocketIO(app )#, async_mode="threading")
  # id INTEGER PRIMARY KEY AUTOINCREMENT,
  # title TEXT NOT NULL,
  # uploader TEXT NOT NULL,
  # requester TEXT NOT NULL,
  # length INTEGER NOT NULL,
  # video_id TEXT NOT NULL UNIQUE,
  # created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

import datetime
class sr(db.Model):
    id = db.Column(db.Integer, primary_key = True , autoincrement = True)
    # title = db.Column(db.String(100))
    # uploader = db.Column(db.String(40) , nullable=False)
    # requester = db.Column(db.String(40) , nullable=False)
    title = db.Column(db.Text)
    uploader = db.Column(db.Text , nullable=False )
    requester = db.Column(db.Text , nullable=False)
    length = db.Column(db.Integer , nullable=False)
    video_id = db.Column(db.Text , unique=True, nullable=False)
    created = db.Column(db.TIMESTAMP , nullable=False , default=datetime.datetime.utcnow )
    votes_gotten = db.Column(db.Integer , nullable = True , default = 0 )
    votes_needed = db.Column(db.Integer , nullable = True)
    #skippers = db.Column()
    #return value

def list_to_string(list1):
    temp = "list1 = list1 + ["
    for item in list1:
        temp += """
        + '{title: """ + item['title'] + """, uploader: """ + item['uploader'] + """, user:""" + item['user'] + """, length: """ + str(item['length']) + """},'
        """
    temp += "]"
    return temp


def add_song(list1):
    data = make_entry(list1[0], list1[1], list1[2], list1[3] , list1[4])
    list2 = database_to_list()
    for x in list2:
        if x['videoID'] == list1[4]:
            return ("error")

    socketio.emit('add' , data)

    esar = sr(title = list1[0] , uploader = list1[1] , requester = list1[2] , length = list1[3] , video_id = list1[4])
    db.session.add(esar)
    db.session.commit()

    esar1 = sr.query.all()

    print("added song prolly")
    return len(esar1)

def remove_song(N = 0):
    print(N)
    esar = sr.query.all()[N]
    db.session.delete(esar)
    db.session.commit()
    return(esar.video_id)
    #print( videoID[0]['video_id'])

def del_all():
    db = get_db()
    videoID = db.execute('DELETE FROM sr').fetchall()

def database_to_list():
    esar = sr.query.all()
    list1 = []
    for item in esar:
        list1.append(make_entry(item.title , item.uploader , item.requester,  item.length , item.video_id ))

    return(list1)

def generating_fake_list():
    list1 = []
    list1.append(make_entry("THE♂TIME♂WIZARD♂" , "DJ FGT" , "xalhs" , 178 , "aC48Cm1eWLY"))
    list1.append(make_entry("your mom song" , "DJ FGT" , "xalhs" , 177 , "vQHM2Q9OMa0"))
    list1.append(make_entry("Don't Doubt" , "DJ FGT" , "xalhs" , 226 , "CRCvq-l_unE"))

    return list1

def make_entry(title, artist ,user ,length , videoID):
    return {"title" : title , "uploader": artist , "user": user , "length": length , "videoID": videoID}

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(1111)
    send(str(username) + ' has entered the room: ' + room , to=room)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == '__main__':

    skippers = []
    #socketio.run(app = app , host = "localhost" , port = 5000 )
    socketio.run(app = app , host = "0.0.0.0" , port = 5001 )
