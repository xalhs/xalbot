import requests
import re
from modules.Settings import CHANNEL
from modules.DownloadImage import DownloadImage
import os
import shutil


def showFFZ():
    names = ""
    request = requests.get(f"https://api.frankerfacez.com/v1/room/{CHANNEL}")
    #print(request.text)
    almostraw = (request.text).split('"name":"')
    n = 0
    for i in almostraw:
        prelist = i.split('","offset')[0]
        n += 1
        if (n % 2 == 0):
            pass
        #    print(prelist + "\n\r")
            names +=  prelist + " "
    return names

def ReloadFFZ():
    if os.path.isdir("emote2"):
        shutil.rmtree("emote2")

    os.makedirs("emote2")
    request = requests.get(f"https://api.frankerfacez.com/v1/room/{CHANNEL}")
    print(request.text)
#    print(request.status_code)
    almostraw = (request.text).split('"name":"')
    size = 3   # select 1 2 or 3 for size of emotes
    n = 0
    for i in almostraw:
        prelist = i.split('","offset')[0]
        n += 1
        if (n % 2 == 0):
            pass
#            print(prelist + "\n\r")
            name = prelist
        elif ( n != 1):
            url1 = "https://" + ((prelist.split('"1":"//'))[1]).split('","2":"')[0]
            url2 = "https://" + ((prelist.split('"2":"//'))[1]).split('","4":"')[0]
            url3 = "https://" + ((prelist.split('"4":"//'))[1]).split('"},"width":')[0]
            if ( size == 1):
                DownloadImage(url1,name)
            elif ( size == 2):
                DownloadImage(url2,name)
            else:
                DownloadImage(url3,name)
    nu = str(int((n-1)/2))
    print("number of emotes: " + nu)
