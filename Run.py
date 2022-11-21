import string
from modules.Settings import CHANNEL, IDENT ################
from modules.ReadOLD import getUser, getMessage, getEmotes, getStatus, getBStatus, getPointRewards
from modules.Socket import openSocket, sendMessage
from modules.Initialize import joinRoom
from modules.twitchPlaysounds import twitchPlaysound, twitchPlaysoundWTD, serverPlaysound, serverPlaysoundWTD
from modules.twitchEmotes import twitchEmotes
from modules.FFZ import ReloadFFZ, showFFZ
from modules.BTTV import showBTTV
#from modules.CleverbotSingleChat import chat
from modules.points import points, Roulette, PointsIncrease, PointsDecrease, rank
from modules.pasta import pasta, addpasta
from modules.commands import addcommand, commands
from modules.tts import tts, Pointstts, servertts, serverPointstts  #, changettsVolume, actualttsvolume
from modules.shoutout import shoutout
from modules.editorbot import titlechange, gamechange
#from modules.ReadCLASS import Message_properties
from modules.Clips import Clip
from modules.Eightball import eightball
from modules.nightbotSongRequest import songrequest, skipsong, currentsong
from modules.timer import timer
from modules.followage import followage
from modules.outoutsmartingstrings import baseletter
from modules.urban import urban
from modules.wiki import wiki
#from modules.twitter import twitter
from modules.uptime import uptime
from modules.math_mod import math
from modules.unmod import unmod

from modules.predictions import create_prediction, end_prediction
from modules.WTDplaysounds import WTD
from modules.point_rewards import CreateReward, getRewardCode, UpdateRewardStatus, getRedemptionid

from modules.youtube_api import request_song, currentqueue, currentsong, when, instaskipsong, playvideo, pausevideo, volume, wrongsong, voteskip, playliston, playlistoff, loadplaylist

import pandas as pd

import codecs
import threading
import multiprocessing
import modules.globals as globals
import os
import pyttsx3
import random

import sys
import importlib
import traceback
import queue

CDTTS = False
permWTD = False

def cooldownTTS():
    global CDTTS
    CDTTS = False

def allowWTD():
    global permWTD
    permWTD = False

#ReloadFFZ()
s = openSocket()
joinRoom(s)
readbuffer = ""
playsounds = True

globals.initialize()
ttsAllowed = True
ttsPrice = 10
pttsQueue = 0
leaderboardnames = [ "a", "a", "a", "a", "a" ]
leaderboard = [ -1, -1, -1, -1, -1]
enableWeebs = True
#maxdur = 190
maxdur= 600
#ttsVolume = 1
 #class TTS:
#     def __init__(self, price, volume, on):
#         self.price = price
#         self.volume = volume
#         self.on = on

CDweebslist = queue.Queue(maxsize=1000)
#def CDweebs():
#    CDweebslist.get()

#CDweebstime = 60

active_chatters = queue.Queue(maxsize = 1000)
def remove_active_chatter():
    active_chatters.get()

active_chatter_CD = 600


id_list = []
user_list = []
#Deathcount = 0
while True:

    try:
        byterecv=s.recv(2048)
      #  print(byterecv)
        if "PRIVMSG" in str(byterecv):
            if ((str(byterecv).split("PRIVMSG ")[1]).split(" :")[1]).startswith("\\x01ACTION"):
                #byterecv = bytes((codecs.decode((str(byterecv)).replace("\\x01ACTION" , "/me" , 1) , 'unicode-escape').split("b'" , 1)[1]).rsplit("\x01\r\n" , 1)[0] + "\r\n" ,  encoding="ascii")
                #print(50*"#")
                stringrecv = "PRIVMSG" + "meflag=True" + byterecv.decode("utf-8")
            else:
                stringrecv= "PRIVMSG" +  byterecv.decode("utf-8")
        else:
            stringrecv= byterecv.decode("utf-8")


        readbuffer = readbuffer + stringrecv
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()
    except:
        print(byterecv)
        raise YourMomError("forsenHead")

    for line in temp:
          try:
              print(line)
              if "PING :tmi.twitch.tv" in line:
                  bytepong = line.replace("PING","PONG")
                  bytepong = bytepong + "\r\n"
                  print(bytepong)
                  s.sendall(bytepong.encode("utf-8"))
              elif (line.rstrip("\r") == ":tmi.twitch.tv CAP * ACK :twitch.tv/tags"):
                  print("found the tmi line \r\n")
              elif (line.rstrip("\r").startswith(":tmi.twitch.tv CAP * ACK :twitch.tv/commands")):
                  print("found the command line \r\n")
              elif ("display-name="+ IDENT).lower() in line.lower():
                  print("botline \r\n")
              elif line.startswith("PRIVMSG"):
                  line = line.split("PRIVMSG" , 1)[1]
    #              line = Message_properties(line)
            #      user = Message_properties.User(line)
            #      message = line.Message()
            #      emotes = line.TwitchEmotes()
                  user = getUser(line)
                  message = getMessage(line)
                  emotes = getEmotes(line)
                  mod = getStatus(line)
                  pointRewards = getPointRewards(line)
                  [pointRewards,reward_id] = getPointRewards(line)
                  if pointRewards != 0:
                      print("reward redeemed " + str(pointRewards) )
                      try:
                          id_of_redemption = getRedemptionid(user , message , reward_id)
                      except:
                          id_of_redemption = "yourmom"
    #              print("points rewards is " + str(pointRewards))
                  print(user + " typed :" + message)
                  print("typed emotes: " + emotes)
                  if message.startswith("!"):                       #!commands
                    try:
                        sendMessage(s, commands(message))
                    except:
                        pass
                  if (message.lower()).startswith("!addcommand ") and mod == True:
                      addcommand(message.split(" " , 2)[1], message.split(" " , 2)[2])
                  if message.lower() == "!pasta":
                      sendMessage(s, pasta())
                  if (message.lower()).startswith("!addpasta ") and mod == True:
                      k = addpasta(message.split(" ", 1)[1])
                      if k == 1:
                          sendMessage(s, "Pasta added")
                      if k == 0:
                          sendMessage(s, "Pasta already exists")
        #          print("ttsEND is " + str(global.ttsEND))
                  if message.lower() == "!ttson" and mod == True:
                      ttsAllowed = True
                      sendMessage(s, "points for !tts is now on")
                  if message.lower() == "!ttsoff" and mod == True:
                      ttsAllowed = False
                      sendMessage(s, "points for !tts is now off")

    #              if (message.lower()).startswith("!changettsvolume") and mod == True:
    #                 try:
    #                      ttsVolume = float(message.split(" ")[1])
    #                      if ttsVolume <= 1 and ttsVolume >= 0:
    #                          changettsVolume(ttsVolume)
    #                          sendMessage(s, "tts volume changed to " + str(ttsVolume))
    #                      else:
    #                          sendMessage(s, "Please give a value between 0 and 1")
    #                 except:
    #                     sendMessage(s, "something failed with the changettsvolume command please check to see if you typed the command correctly")
    #              if message.lower() == "!ttsvolume":
    #                  sendMessage(s, user + " the current tts volume is " + str(ttsVolume))
    #              if message.lower() == "!actualttsvolume":
    #                sendMessage(s , str(actualttsvolume()))
                  if (message.lower()).startswith("!changettsprice ") and mod == True:
                      try:
                          if int(message.split(" ")[1]) >= 0:
                              ttsPrice = int(message.split(" ")[1])
                              sendMessage(s, "changed tts price to " + message.split(" ")[1])
                          else:
                              sendMessage(s, "give a positive value you Pepega")
                      except:
                          sendMessage(s, "could not recognize the value, type a positive integer Pepega")
                  if (message.lower()) == "!ttsprice":
                      sendMessage(s, "current tts price is " + str(ttsPrice))
                  if (message.lower()).startswith("!tts "):
                      if (points(user) > ttsPrice  and CDTTS == False) and (globals.ttsEND == True and ttsAllowed == True):
                          PointsDecrease(user, ttsPrice)
                          ttsProcess = threading.Thread(target = servertts, args = (message.split(" " , 1)[1],))
                          globals.ttsEND = False
                          ttsProcess.start()
                          timerTTS = threading.Timer(10.0, cooldownTTS)
                          timerTTS.start()
                          CDTTS = True
                      elif (ttsAllowed == False):
                          sendMessage(s, "tts is currently off")
                      elif (CDTTS == True):
                          sendMessage(s , user + " tts is on cooldown right now")
                      elif (globals.ttsEND == False):
                          sendMessage(s, user + " wait for the previous tts message to end")
                      else:
                          sendMessage(s, user + " you don't have enough points to request tts")
                  if (message.lower().startswith("!create_reward") and mod == True):
                      reward_params = message.split(" " , 1)[1]
                      reward_params = reward_params.split("|")
                      sendMessage(s, "/me @" + user + " " + CreateReward(reward_params))
                  if (pointRewards == 1):
                      ttsProcess = threading.Thread(target = serverPointstts, args = (message, pttsQueue,))
                      ttsProcess.start()
                      pttsQueue += 1
                  if (pointRewards == 2):
                     song = request_song(message , user)
                     try:
                         if (song[0] == 0):
                             sendMessage(s, user + ", " + song[2])
                     except:
                         duration = int(song.dur)
                         title = song.name
                         id = song.id
                         id_list.append(id)
                         user_list.append(user)
                         if duration > maxdur:
                             timerSR = threading.Timer(maxdur + 0.0 + globals.timer , skipsong , args = (title, ))
                             timerSR.start()
                         if globals.timerrunning == False:
                             if duration > maxdur:
                                 print("nam111")
                                 timerProcess = threading.Thread(target = timer, args = (maxdur, ))
                                 timerProcess.start()
                             else:
                                 print("ordie")
                                 timerProcess = threading.Thread(target = timer, args = (duration, ))
                                 timerProcess.start()
                         elif duration > maxdur:
                             globals.timer += maxdur
                         else:
                             globals.timer += duration
                         sendMessage(s, user + " your video " + song.name + " by " + song.artist + " has been added to the queue in position " +  str(song.pos))


                  if (pointRewards == 3):
                      waytoodank = "!playsound hey guys hows it going kripparrian here waytoodank"
                      PlaysoundProcess = threading.Thread(target = serverPlaysoundWTD, args = (waytoodank,))
                      PlaysoundProcess.start()
                  if (pointRewards == 5):
                      psound = message
                      #psound = message.split(" " , 1)[1]
                      if os.path.isfile("var/playsounds/" + psound + ".mp3") or os.path.isfile("var/playsounds/" + psound + ".wav"):
                          if os.path.isfile("var/SpecialPlaysounds/" + message+ "WAYTOODANK.mp3"):
                              sendMessage(s, "/me @" + user + " playsound is already WAYTOODANK ified, refunding your points")
                              UpdateRewardStatus(["WAYTOODANKIFY" , id_of_redemption , "CANCELED"])
                          else:
                              WTDProcess = threading.Thread(target = WTD, args = (message,))
                              WTDProcess.start()
                        #  UpdateRewardStatus(["WAYTOODANKIFY" , id_of_redemption , "FULFILLED"])
                      else:
                          sendMessage(s, "/me @" + user + " couldn't find the playsound, refunding your points")
                          UpdateRewardStatus(["WAYTOODANKIFY" , id_of_redemption , "CANCELED"])
                  if (pointRewards == 6):
                      if os.path.isfile("var/SpecialPlaysounds/" + message+ "WAYTOODANK.mp3"):
                          PlaysoundProcess = threading.Thread(target = serverPlaysoundWTD, args = (message,))
                          PlaysoundProcess.start()
                          #UpdateRewardStatus(["Play Special Playsound" , id_of_redemption , "FULFILLED"])
                      else:
                          sendMessage(s, "/me @" + user + " couldn't find the playsound, refunding your points")
                          UpdateRewardStatus(["Play Special Playsound" , id_of_redemption , "CANCELED"])



                  if (message.lower().startswith("!changemaxdur")) and mod == True:
                      try:
                          maxdur = int(message.split(" " , 1 )[1])
                          sendMessage(s, "max video duration changed to " + str(maxdur))
                      except:
                          sendMessage(s, "could not change max duration to that value")
                ##########################
                  if (message.lower()).startswith("!points") :
                      if message.lower() == "!points":
                          sendMessage(s, user + " you have " + str(points(user)) + " points")
                      elif points(message.split(" ")[1]) == None:
                          sendMessage(s, 'could not find user "' +  message.split(" ")[1] + '"')
                      else:
                          sendMessage(s, 'user "' + message.split(" ")[1] + '" has ' + str(points(message.split(" ")[1])) + " points" )

                  if (message.lower()).startswith("!roulette "):
                      amount = (message.lower()).split("!roulette ")[1]
                      if amount.endswith("%"):
                          try:
                              perc = float(amount.split("%")[0])
                              amount = round(points(user)*perc*0.01)
                          except:
                              pass
                      if amount == "all":
                          amount = points(user)
                      print("amount = " + str(amount))
                      try:
                          amount = int(amount)
                      except:
                          pass
                      if isinstance( amount, int):
                          if (amount > 0):
                               outcome = Roulette(user, amount)
                               if outcome == -1:
                                   sendMessage(s, user + " you lost " + str(amount) +  " points in roulette and now have " + str(points(user)) + " points forsenSWA" )
                               if outcome == 1:
                                   sendMessage(s, user + " you won " + str(amount) +  " points in roulette and now have " + str(points(user)) + " points forsenPls" )
                               if outcome == 0:
                                   sendMessage(s, user + " you don't have that many points to roulette" )
                          if (amount == 0):
                              sendMessage(s, user + " you can't roulette 0 points")
                  if (message.lower()).startswith("!give "):
                      amount = (message.lower()).split(" ")[2]
                      receiver = (message.lower()).split(" ")[1]
                      if amount.endswith("%"):
                          try:
                              perc = float(amount.split("%")[0])
                              amount = round(points(user)*perc*0.01)
                          except:
                              pass
                      if amount == "all":
                          amount = points(user)
                    #  print("amount = " + str(amount))
                      try:
                          amount = int(amount)
                      except:
                          pass
                      if isinstance( amount, int):
                          if points(message.split(" ")[1]) != None:
                              if (amount > 0):
                                   PointsDecrease(user, amount)
                                   PointsIncrease(receiver, amount)
                                   sendMessage(s, user + " gave " + receiver + " " + str(amount) + " points")
                              if (amount == 0):
                                  sendMessage(s, user + " you can't give 0 points")
                          else:
                              sendMessage(s, "couldn not find user " + receiver)
                  if (message.lower()) == "!leaderboard":
                      df = pd.read_csv('var/points/points.csv'  , index_col = 0)
                      df = df.sort_values('points' , ascending=False).T
                      snd = "leaderboards are: "
                      for i , name in enumerate(df):
                            if i < 5:
                                snd += str(i+1) + ". " + name + " with " + str(df[name]['points']) + " points, "
                                print(name + " " + str(df[name]['points']))
                      snd = snd[:-2] + "."
                      sendMessage(s , snd)

                  if (message.lower()) == "!rank":
                      print(user)
                      rank2 = rank(user)
                      sendMessage(s, user + " you are rank " + str(rank2[0]) + " with " + str(rank2[1]) + " points." )

                    ######################################
                  if (message.lower()).startswith("!8ball "):
                       sendMessage(s, user + " " + eightball())
                  if (message.lower()).startswith("!clip") and mod == True:
                      ClipProcess = threading.Thread(target = Clip)
                      ClipProcess.start()
                  if ((message.lower()) == "!playsoundson") and mod == True:
                      playsounds = True
                      sendMessage(s, "playsounds are now on")
                  if ((message.lower()) == "!playsoundsoff") and mod == True:
                      playsounds = False
                      sendMessage(s, "playsounds are now off")
                  if ((message.lower()) == "!playliston" or (message.lower()) == "!playlist on") and user == "xalhs":
                      playliston()
                      sendMessage(s, "playlist is now on")
                  if ((message.lower()) == "!playlistoff" or (message.lower()) == "!playlist off") and user == "xalhs":
                      playlistoff()
                      sendMessage(s, "playlist is now off")
                  if (message.lower()).startswith("!loadplaylist ") and user == "xalhs":
                      loadplaylist(message.split(" " , 1)[1])
                  if (message.lower()) == "!ffz":
                      sendMessage(s, "available FFZ emotes: " + showFFZ())
                  if (message.lower()) == "!bttv":
                      sendMessage(s, "available BTTV emotes: " + showBTTV())
                  if ((message.lower()) == "!allow waytoodank" and getBStatus(line) == True) or (pointRewards == 4):
                      sendMessage(s, "WAYTOODANK will be allowed for 10 seconds")
                      permWTD = True
                      timerWTD = threading.Timer(10.0 , allowWTD)
                      timerWTD.start()
                  if (message.lower()) == "!playsound " and permWTD == True:
                      PlaysoundProcess = threading.Thread(target = serverPlaysoundWTD, args = (message,))
                      PlaysoundProcess.start()
                  if playsounds == True:
                     PlaysoundProcess = threading.Thread(target = serverPlaysound, args = (message,))
                     # twitchPlaysound(message)
                     PlaysoundProcess.start()
                  if (message.lower() == "!enable weebs"):
                      enableWeebs = True
                      sendMessage(s, "contacting pajlada...")
                  if (message.lower() == "!disable weebs"):
                      enableWeebs = False
                  weebs = ["ayaya", "weeb", "weebs", "anime", "weaboo", "weaboos", "nemzanana"]
                  if (any (x in baseletter(message).lower() for x in weebs)) and enableWeebs == True:
                      sendMessage(s, "/me WEEBSDETECTED WEEBS OUT")
                  if (message.lower()).startswith("!so ") and mod == True:
                      try:
                          sendMessage(s , shoutout((message.lower()).split("!so ")[1]))
                      except:
                          sendMessage(s , "something went wrong with the shoutout command")
                  if (message.lower()).startswith("!title ") and getBStatus(line) == True:
                      try:
                          sendMessage(s , titlechange(message.split(" " , 1)[1]))
                      except:
                          sendMessage(s, "something went wrong with titlechange command")
                  if (message.lower()).startswith("!game ") and getBStatus(line) == True:
                      try:
                          sendMessage(s , gamechange(message.split(" " , 1)[1]))
                      except:
                          sendMessage(s, "something went wrong with gamechange command")
                  if (message.lower()) == "!emojitest":
                      sendMessage(s, " <3 🍓🍑🍊🍋🍍NaM 🍐🍏🐬🐳NaM 🍆🐙🌷🐷🍓🍑🍊🍋🍍NaM  ♥   ")
                  if (message.lower().startswith("!followage")):
                      try:
                          follow_params = message.split(" ")
                          sendMessage(s, followage(follow_params[1],follow_params[2]))
                      except:
                          try:
                              follow_params = message.split(" ")
                              sendMessage(s, followage(follow_params[1], CHANNEL))
                          except:
                              sendMessage(s , followage(user , CHANNEL))
                  if (message.lower().startswith("!urban ")):
                      urban_array = urban(message.split(" ",1)[1])
                      for parts in urban_array:
                          sendMessage(s , parts)
                      #sendMessage(s, urban(message.split(" ",1)[1]))
                  if (message.lower().startswith("!wiki ")):
                      wiki_array = wiki(message.split(" ",1)[1])
                      for parts in wiki_array:
                          sendMessage(s , parts)
                #      sendMessage(s , wiki(message.split(" ",1)[1]))
                  if (message.lower().startswith("!w ")) and (user == "xalhs"): #and (user == "NainsArrival"):
                      sendMessage(s, "/w " + user + " " +  message.split(" " , 1)[1] + "\r\n")

                #  if (message.lower().startswith("!twitter ")) and (mod == True or user == "xalhs"):
                #      sendMessage(s, twitter(message.split(" ", 1)[1]))
                  if (message.lower()) == "!drop":
                      sendMessage(s, "/me " + user + " your drop is ready check your notifications")

                  if (message.lower()).startswith("!uptime"):
                       try:
                           uptimechannel =  message.split(" " , 1)[1]
                       except:
                           uptimechannel = CHANNEL
                       uptimemessage = uptime(uptimechannel)
                       if "offline" in uptimemessage:
                           sendMessage(s,"/me " + uptimemessage)
                       else:
                           sendMessage(s,"/me " + uptimechannel + " has been live for " + uptimemessage)
                  if (message.lower() == "!currentsong" or message.lower() == "!song"  ):
                      sendMessage(s , "/me " + user + ", " + currentsong())

                  if (message.lower() == "!q" or message.lower() == "!queue" ):
                      sendMessage(s , "/me " + user + ", " + currentqueue())
                  if (message.lower() == "!when"):
                      sendMessage(s , "/me " + user + ", " + when(user))
                  if (message.lower() == "!skip") and (mod == True or vip):
                      instaskipsong()
                  if (message.lower() == "!play") and (mod == True or vip):
                      playvideo()
                  if (message.lower() == "!pause") and (mod == True or vip):
                      pausevideo()
                  if (message.lower()).startswith("!volume") and (mod or vip):
                      newvol = message.split(" " , 1)[1]
                      try:
                          newvolint = int(newvol)
                          volume(newvolint)
                          sendMessage(s , "/me " + user + " changed volume to " + str(newvolint))
                      except:
                          sendMessage(s , "/me " + user + ", please provide a valid value for the volume")
                  if (message.lower()) == "!wrongsong":
                      sendMessage(s , "/me " + user + "," + wrongsong(user))
                  if user not in list(active_chatters.queue):
                      active_chatters.put(user)
                      active_chatter_Process = threading.Timer(remove_active_chatter , active_chatter_CD)
                      active_chatter_Process.start()
                  if (message.lower()) == "!voteskip":
                      sendMessage(s, "/me " + voteskip(user , active_chatters.qsize()))

                  if (message.lower()).startswith("!math"):
                      if message.startswith("!math help"):
                          sendMessage(s, "/me @" + user + ' use !math to calculate mathematical expressions, for example "!math 3^2 + 4^2" ')

                      else:
                          sendMessage(s , "/me @" +user + " " + math(message.split("!math " , 1)[1]) )

                  if message.lower() == "!unmod":
                      if mod ==True:

                          if getBStatus(line) == True:
                              sendMessage(s , "You can't unmod yourself FailFish you are the streamer")
                          else:
                              UnmodProcess = threading.Thread(target = unmod, args = (user,))
                              UnmodProcess.start()
                      else:
                          sendMessage(s , "You are not a mod idiot, you can't get unmodded FailFish")

                  if message.lower().startswith("!create_prediction") and mod == True:
                      sendMessage(s , "/me " + create_prediction((message.split("!create_prediction ")[1]).split("|")))

                  if message.lower().startswith("!end_prediction") and mod == True:
                      sendMessage(s , "/me " + end_prediction(message.split("!end_prediction ")[1]))





              else:
                  print("#"*10 + " LINE IS NOT MESSAGE " + "#"*100)
                  print(line)


          except:
              print("!"*50 + "EXCEPTION")
              traceback.print_exc()
              pass
            #  basss = "nam"
            #  print(bass.split(" "))
             # sendMessage(s, line)



                #  weebs = ["weeb", "weebs", "anime", "weaboo", "weaboos", "nemzanana" , "nam"]
                 # if (any (x in baseletter(message).lower() for x in weebs)) and user not in list(CDweebslist.queue):
                #      CDweebslist.put(user)
                #      CDweebsProcess = threading.Timer(CDweebstime , CDweebs)
                #      CDweebsProcess.start()
                #      print("1")
            #      twitchEmotes(message)
            #      if "@xalbot9000" in message:
            #          CBT = message.split("@xalbot9000")
            #          userinput = ""
            #          for l in CBT:
            #              userinput = userinput + l
            #          chat(s, user, userinput)
            #      if " cd " in message:
            #        sendMessage(s, "/me forsenCD Clap")
