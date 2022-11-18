import string
from modules.Settings import CHANNEL #could be done better prob

class Message_properties():

    def __init__(self , ch):
        self.ch = ch
#        super(Message_properties).__init__(args)

    @staticmethod
    def User(self):
        separete = (self).split(";emote", 1)[0]
        user = separete.split("display-name=" , 1)[1]
#        separate = line.split(":", 2) old getuser commands
#        user = separate[1].split("!", 1)[0]
        return user
    @classmethod
    def Message(self):
        txt = (self.ch).split("PRIVMSG #" + CHANNEL + " :" , 1)[1]
        message = txt.rstrip("\r")
#       txt = line.split(":", 2)[2]  old getmessage command
#        message = txt.rstrip("\r")
        return message
    @classmethod
    def twitch_emotes(self):
        temp = (self.ch).split("PRIVMSG")[0]
        temp2 = temp.split("display-name=")[1]
        #temp3 = temp2.split(";")[1]
        temp4 = temp2.split("emotes=")[1]
        temp5 = temp4.split(";flags")[0]
        first = temp5.split("/")
        emotes = ""
        for second in first:
            third = second.split(":")[0]
            count = second.count(",") + 1
            emotes = emotes + " " + third + " " + str(count) + " times"
            return emotes
