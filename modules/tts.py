import pyttsx3
import modules.globals as globals
import requests
import json
import time
from modules.Settings import MY_AUTH, link

def tts(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(message)
    engine.runAndWait()
    engine.stop()
    globals.ttsEND = True

def Pointstts(message , pttsQueue):
    while (globals.ttsEND == False) or (globals.pttsPosition != pttsQueue):
        pass
    globals.ttsEND = False
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(message)
    engine.runAndWait()
    engine.stop()
    globals.pttsPosition += 1
    globals.ttsEND = True

def servertts(message):
    filename = str(time.time_ns())
    file_type =".mp3"
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.save_to_file(message ,"D:/Users/XALHS/pyth/var/tts/" +  filename +  file_type )
    engine.runAndWait()
    engine.stop()
    body = json.dumps({"data": {"tts_filename": filename , "type": file_type}})
    request = requests.post(link + "/tts", headers = { 'Authorization': MY_AUTH, "Content-Type": "application/json"} ,  data = body).json()
    globals.ttsEND = True

def serverPointstts(message , pttsQueue):
    while (globals.ttsEND == False) or (globals.pttsPosition != pttsQueue):
        pass
    globals.ttsEND = False
    filename = str(time.time_ns())
    file_type =".mp3"
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.save_to_file(message ,"D:/Users/XALHS/pyth/var/tts/" +  filename +  file_type )
    engine.runAndWait()
    engine.stop()
    body = json.dumps({"data": {"tts_filename": filename , "type": file_type}})
    request = requests.post(link + "/tts", headers = { 'Authorization': MY_AUTH,"Content-Type": "application/json"} ,  data = body).json()
    globals.pttsPosition += 1
    globals.ttsEND = True

#def changettsVolume(volume):
#    engine = pyttsx3.init()
#    engine.setProperty('volume',volume)
#    engine.stop()
#
#def actualttsvolume():
#    engine = pyttsx3.init()
#    k = engine.getProperty('volume')
#    engine.stop()
#    return k
