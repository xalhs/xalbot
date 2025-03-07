import random
import os
import codecs
import shutil
import time
from modules.Settings import CHANNEL
import pandas as pd

def points(name):
    name = name.lower()
    df = pd.read_csv('var/points/points.csv'  , index_col = 0).T
    try:
        return df[name]['points']
    except:
        return None

def Roulette(name , amount):
    name = name.lower()
    df = pd.read_csv('var/points/points.csv'  , index_col = 0).T
    try:
        p = df[name]['points']
    except:
        return 0
    if p < amount and amount > 0 :
        return 0
    else:
        s = random.random()
        print("s= " + str(s))
        if s < 0.5:
            df[name]['points'] -= amount
            df = df.T
            df.to_csv('var/points/points.csv')

            f= codecs.open("var/Roulette/" + name + ".txt", "a+" , "utf-8")
            f.write((time.ctime(time.time())).split(" ", 1)[1]  + " roulette: -" + str(amount) +  "\r\n")
            f.close()
            return -1
        else:
            df[name]['points'] += amount
            df = df.T
            df.to_csv('var/points/points.csv')

            f= codecs.open("var/Roulette/" + name + ".txt", "a+" , "utf-8")
            f.write((time.ctime(time.time())).split(" ", 1)[1] + " roulette: +" + str(amount) +  "\r\n")
            f.close()
            return 1

def PointsIncrease(name, amount):
    name = name.lower()
    df = pd.read_csv('var/points/points.csv'  , index_col = 0).T
    df[name]['points'] += amount
    df = df.T
    df.to_csv('var/points/points.csv')


def PointsDecrease(name, amount):
    name = name.lower()
    df = pd.read_csv('var/points/points.csv'  , index_col = 0).T
    df[name]['points'] -= amount
    df = df.T
    df.to_csv('var/points/points.csv')

def rank(name):
    name = name.lower()
    df = pd.read_csv('var/points/points.csv'  , index_col = 0)
    df = df.sort_values('points' , ascending=False).T
    for i , user in enumerate(df):
        i += 1
        if user == name:
            return [i , df[name]['points']]



#def givePoints(user1, user2, amount):
