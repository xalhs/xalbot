import pyttsx3
import modules.globals as globals

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
