import string
import os
from PIL import Image

def twitchEmotes(message):
    m = message
    print(m)
    m = message.split(" ")
    for e in m:
#        print("printing e" + e)
        try:
            if  e + ".png" in os.listdir("emote2"):
                im = Image.open("emote2/" + e + ".png")
                im.show()
            elif e + ".PNG" in os.listdir("emote2"):
                im = Image.open("emote2/" + e + ".png")
                im.show()

        #    if os.path.isfile("emote2/" + e + ".png"):
        #        im = Image.open("emote2/" + e + ".png")
        #        im.show()

        except:
            print("no emote found with that name")
