from PIL import Image
import requests
from io import BytesIO
from modules.Settings import CHANNEL

def showBTTV():
    request = requests.get(f"https://api.betterttv.net/2/channels/{CHANNEL}")
    #print(request.text)
    almostraw = (request.text).split('code":"')
    names = ""
    n = 0
    for i in almostraw:
        n += 1
        prelist = i.split('","imageType')[0]
        #print(prelist + "\r\n")
        if n != 1:
            names += prelist + " "
    return names
