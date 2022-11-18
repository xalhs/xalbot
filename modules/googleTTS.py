from gtts import gTTS
import os
from playsound import playsound
import time

#text = "O M E G A L U L O M E G A L U L O M E G A L U L O M E G A L U L O M E G A L U L O M E G A L U L O M E G A L U L O M E G A L U L O M E G A L U L "

def tts(text):
    language = 'en'
    os.remove("text.mp3")
    print("0")
    time.sleep(5)
    speech = gTTS(text = text, lang = language, slow = False)
    print("1")
    speech.save("text.mp3")
    print("2")
    playsound("text.mp3")
    print("3")
    time.sleep(5)
    print("4")
