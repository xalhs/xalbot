from modules.chatters import chatters
from modules.Settings import CHANNEL
from modules.uptime import uptime
import time
import os
import codecs
import shutil
import pandas as pd


amount = 50

T = True
while ( T == True):
    uptimemessage = uptime(CHANNEL)
    if not "offline" in uptimemessage:
        list = chatters()
        df = pd.read_csv('var/points/points.csv'  , index_col = 0).T
        for name in list:
            if name in df:
                df[name]['points'] = int( df[name]['points'] +  amount)
                df[name]['watchtime'] = int(df[name]['watchtime']  +5)
            else:
                df[name] = [amount , 5 , list[name]]
            print(name)
            print(df[name]['points'])

        df = df.T
        df.to_csv('var/points/points.csv')
    #    copyfile ("logsRECORDER.txt" , "copyRECORDER.txt")
    print("new loop")
    time.sleep(300)
