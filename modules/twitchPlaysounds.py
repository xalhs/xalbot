import string
import os
from playsound import playsound
import requests
import json
import traceback
from modules.Settings import MY_AUTH, link

def twitchPlaysound(message):
    m = message.lower()
    if m.startswith("!playsound"):
        print(m)
        try:
            c = m.split(" ", 1)[1]
            if os.path.isfile("var/playsounds/" + c + ".mp3"):
                print("playing a sound")
                playsound("var/playsounds/" + c + ".mp3")
            if os.path.isfile("var/playsounds/" + c + ".wav"):
                print("playing a sound")
                playsound("var/playsounds/" + c + ".wav")
        except:
            print("no playsound found with that name")

def twitchPlaysoundWTD (message):
    m = message.lower()
    if m.startswith("!playsound"):
        print(m)
        try:
            c = m.split(" ", 1)[1]
            if os.path.isfile("var/SpecialPlaysounds/" + c + ".mp3"):
                print("playing a sound")
                playsound("var/SpecialPlaysounds/" + c + ".mp3")
            else:
                print("no playsound found with that name")
        except:
            print("no playsound found with that name")

def serverPlaysound(message):
    m = message.lower()
    if m.startswith("!playsound"):
        print(m)
        try:
            c = m.split(" ", 1)[1]
            if os.path.isfile("var/playsounds/" + c + ".mp3"):
                print("playing a sound")
                psound_type = ".mp3"
            if os.path.isfile("var/playsounds/" + c + ".wav"):
                print("playing a sound")
                psound_type = ".wav"
            body = json.dumps({"data": {"playsound": c , "type": psound_type}})
            request = requests.post(link + "/playsound", headers = { 'Authorization': MY_AUTH, "Content-Type": "application/json"} ,  data = body).json()
        except:
            traceback.print_exc()
            print("no playsound found with that name")

def serverPlaysoundWTD (message):
    m = message.lower()
    if m.startswith("!playsound"):
        print(m)
        try:
            c = m.split(" ", 1)[1]
            if os.path.isfile("var/SpecialPlaysounds/" + c + ".mp3"):
                print("playing a sound")
                psound_type = ".mp3"
            else:
                print("no playsound found with that name")
            body = json.dumps({"data": {"specialplaysound": c , "type": psound_type}})
            request = requests.post(link + "/specialplaysound", headers = { 'Authorization': MY_AUTH, "Content-Type": "application/json"} ,  data = body).json()
        except:
            traceback.print_exc()
            print("no playsound found with that name")
    else:
        try:
            c = message.lower()
            if os.path.isfile("var/SpecialPlaysounds/" + c + "WAYTOODANK.mp3"):
                print("playing a sound")
                psound_type = ".mp3"
                #playsound("var/SpecialPlaysounds/" + c + "WAYTOODANK.mp3")
            else:
                print("no playsound found with that name")
            body = json.dumps({"data": {"specialplaysound": c + "WAYTOODANK" , "type": psound_type}})
            request = requests.post(link + "/specialplaysound", headers = { 'Authorization': MY_AUTH, "Content-Type": "application/json"} ,  data = body).json()
        except:
            print("no playsound found with that name")
