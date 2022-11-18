from modules.Settings import BROADCASTER_PASS, BROADCASTER_IDENT

from modules.Socket import openSocket, sendMessage
from modules.Initialize import joinRoom

import time

id = BROADCASTER_IDENT
b_pass = BROADCASTER_PASS

def unmod(name):
    s = openSocket("custom" , id , b_pass )
    joinRoom(s , "silent")
    sendMessage(s, "/unmod " + name)
    sendMessage(s , name + " you have 60 seconds to bet before you get modded again")
    time.sleep(60)
    sendMessage(s , "/unban " + name)
    time.sleep(0.3)
    sendMessage(s , "/mod " + name)
