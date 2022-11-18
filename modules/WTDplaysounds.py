from pydub import AudioSegment
from pydub.playback import play
import os
from playsound import playsound

def WTD(psound):
    c = psound
    try:
        if os.path.isfile("var/playsounds/" + c + ".mp3"):
            playsoundfile = "var/playsounds/" + c + ".mp3"
            audio = AudioSegment.from_mp3("var/playsounds/" + c + ".mp3")
        if os.path.isfile("var/playsounds/" + c + ".wav"):
            playsoundfile = "var/playsounds/" + c + ".wav"
            audio = AudioSegment.from_wav("var/playsounds/" + c + ".wav")
    except:
        print("no playsound found with that name")
        return

    silence = AudioSegment.silent(duration=116)
    final = AudioSegment.silent(duration=0)
    final += audio
    print(len(audio))
    for i in range(16):
        result = AudioSegment.silent(duration=0)
        for j in range(4):
            result = audio.overlay(result)
            audio = silence + audio
            print(len(result))
        audio = result
        final += AudioSegment.silent(duration=3000) + result
    #return
    final.export("var/SpecialPlaysounds/" + c +"WAYTOODANK.mp3", format="mp3")
    playsound("var/SpecialPlaysounds/" + c +"WAYTOODANK.mp3")
