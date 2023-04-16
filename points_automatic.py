from modules.chatters import chatters
from modules.Settings import CHANNEL
import time
import os
import codecs
import shutil
import pandas as pd


amount = 50

T = True
while ( T == True):
    list = chatters()
    df = pd.read_csv('var/points/points.csv'  , index_col = 0).T
    for name in list:
        if name in df:
            df[name]['points'] += amount
            df[name]['watchtime'] += 5
        else:
            df[name] = [amount , 5]
        print(name)
        print(df[name]['points'])

    df = df.T
    df.to_csv('var/points/points.csv')
#    copyfile ("logsRECORDER.txt" , "copyRECORDER.txt")

    time.sleep(300)
