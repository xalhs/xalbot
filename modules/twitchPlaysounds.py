import string
import os
from playsound import playsound

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
