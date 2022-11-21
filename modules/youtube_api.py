import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import re
import requests
import json
from urllib.parse import urlparse, parse_qs
from modules.Settings import MY_AUTH, link

devKey = "" #your dev key here

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
#link = "http://localhost:5001"

def main():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=devKey)

    print(youtube)
    request = youtube.search().list(
         part="snippet",
         maxResults=25,
         q="the forsen build song"
     )
    response = request.execute()

    print(response)

def search_song(query):
    ytlinks = [ "youtube." , ".youtube" , "youtu."]
    vid_id = ""
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=devKey)

    if  (any (x in query.lower() for x in ytlinks)):
        print("found potential vidid")
        vid_id = videoid_from_url(query)
    if vid_id == "":
        print("searching youtube")
        request = youtube.search().list(
             part="snippet",
             maxResults=25,
             q= query
         )
        response = request.execute()
        if response['items'] == []:
            return["error" , 404 , "could not find video"]
        print(response)
        vid_id = response['items'][0]['id']['videoId']

    print("vidid = " + vid_id)
    request2 = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id=vid_id
    )
    response2 = request2.execute()
    print(response2)
    if response2['items'] == []:
        return["error" , 405 , "invalid video id"]
    try:
        if response2['items'][0]['contentDetails']['contentRating']['ytRating'] == 'ytAgeRestricted':
            return["error" , 69 , "video is age restricted"]
    except:
        pass

    title = response2['items'][0]['snippet']['title']
    uploader = response2['items'][0]['snippet']['channelTitle']
    dur = dur_to_sec(response2['items'][0]['contentDetails']['duration'])

    return [title, uploader , dur , vid_id]

reg = r"""(?:http:|https:)*?\/\/(?:www\.|)(?:youtube\.com|m\.youtube\.com|youtu\.|youtube-nocookie\.com).*(?:v=|v%3D|v\/|(?:a|p)\/(?:a|u)\/\d.*\/|watch\?|vi(?:=|\/)|\/embed\/|oembed\?|be\/|e\/)([^&?%#\/\n]*)"""

def videoid_from_url(link1):
    try:
        url_data = urlparse(link1)
        query = parse_qs(url_data.query)
        video = query['v'][0]
        return video
    except:
        pass

    print(reg)
    m = re.findall(reg , link1)

    if m == []:
        return ""
    else:
        return m[0]

def request_song(query , user):

    info = search_song(query)
    if info[0] == "error":
        return [ 0 , info[1] , info[2]]
    info.insert(2 , user)
    body = json.dumps({"data": info})
    #request = requests.post("http://127.0.0.1:5000/sr", headers = {"Content-Type": "application/json"} ,  data = body)
    request = requests.post(link + "/sr", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} ,  data = body).json()

    try:
        return[0 , 420 , request['error']]
    except:
        class Song:
            def __init__(self):
                Song.dur = info[3]
                Song.name = info[0]
                Song.artist = info[1]
                Song.pos = request['data']
                Song.id = 1
        pos = request['data']
        return Song()

def voteskip(user , active_chatters):
    body = json.dumps({"data": {"user": user , "active_chatters": active_chatters}})
    request = requests.post(link + "/voteskip", headers = {"Content-Type": "application/json"  , 'Authorization': MY_AUTH} ,  data = body).json()
    return(request['data'])

def dur_to_sec(dur):
    dur_sec = 0
    dur_split = re.split('(\d+)',dur)

    for i , num in enumerate(dur_split):
        try:
            num = int(num)
        except:
            pass
        if isinstance(num, int):
            if dur_split[i+1] == "S":
                mult = 1
            elif dur_split[i+1] == "M" and any ("T" in element for element in dur_split[:i]):
                mult = 60
            elif dur_split[i+1] == "H":
                mult = 3600
            elif dur_split[i+1] == "D" or dur_split[i+1] == "DT":
                mult = 86400  # seconds in day
            elif dur_split[i+1] == "W" or dur_split[i+1] == "WT":
                mult = 86400*7
            elif (dur_split[i+1] == "M" and "T" in dur_split[i:]) or dur_split[i+1] == "MT":
                mult = 86400*30
            elif dur_split[i+1] == "Y" or dur_split[i+1] == "YT":
                mult = 86400*365
            dur_sec += num*mult

    return dur_sec

def instaskipsong():
    request = requests.post( link + "/hardskip", headers = {'Authorization': MY_AUTH,  "Content-Type": "application/json"} ).json()

def currentsong():
    request = requests.get(link + "/queue" , headers = {'Authorization': MY_AUTH} ).json()['data']
    if request == []:
        return('songrequest client is not on right now, check back later')
    if request[0] == []:
        if( (not request[4]) and request[5] > 0 ):
            return("current song is : " + request[3])
        return("the queue is empty, check top left if song is playing from playlist :)")

    if request[1] != 1:
        if(( not request[4]) and request[5] > 0 ):
            return("current song is : " + request[3])
        return("no song is playing on sr right now, check top left if song is playing from playlist :)" )

    total_dur = request[0][0]['length']
    elapsed_dur = request[2]
    min, secs = divmod(total_dur, 60)
    hours, min = divmod(min, 60)
    hou = ""
    if hours != 0:
        hou =  str(round(hours)) + " hours, "
    if min != 0:
        hou = hou +  str(round(min)) + " minutes and "
    hou += str(round(secs)) + " seconds"
    min2, secs2 = divmod(elapsed_dur, 60)
    hours2, min2 = divmod(min2, 60)
    hou2 = ""
    if hours != 0:
        hou2 =  str(round(hours2)) + " hours, "
    if min2 != 0:
        hou2 = hou2 +  str(round(min2)) + " minutes and "

    hou2 +=  str(round(secs2)) + " seconds"
    return("the song " + request[0][0]['title'] + " from " + request[0][0]['uploader'] + " requested by " + request[0][0]['user'] + " is playing right now, we are currently "  + hou2 + " out of " + hou + " through. Link: https://www.youtube.com/watch?v=" + request[0][0]['videoID'] + " MegaLUL 👉  🔗" )

def currentqueue():
    request = requests.get(link + "/queue" , headers = {'Authorization': MY_AUTH}).json()['data']
    if request == []:
        return('songrequest client is not on right now, check back later')
    if request[0] == []:
        return("the queue is empty")

    total_dur = 0
    num = 0
    for item in request[0]:
        num += 1
        total_dur += item['length']

    total_dur -= request[2]
    bonus = ""
    if request[1] != 1:
        bonus = "songrequest is paused for the moment but "

    min, secs = divmod(total_dur, 60)
    hours, min = divmod(min, 60)
    hou = ""
    if hours != 0:
        hou =  str(round(hours)) + " hours, "
    if min != 0:
        hou = hou +  str(round(min)) + " minutes and "

    return(bonus + "the current queue has " + str(num) + " songs and is "+ hou + str(round(secs)) +  " seconds long")

def when(user):
    request = requests.get(link + "/queue" , headers = {'Authorization': MY_AUTH}).json()['data']
    if request == []:
        return('songrequest client is not on right now, check back later')
    if request[0] == []:
        return("the queue is empty")

    if request[1] != 1:
        return("songrequest is paused for the moment so idk when your song will play eShrug")

    if request[0][0]['user'] == user:
        return("your song is currently playing Pepega")

    total_dur = 0
    total_dur -= request[2]
    num = -1
    for item in request[0]:
        num += 1
        total_dur += item['length']
        min, secs = divmod(total_dur, 60)
        hours, min = divmod(min, 60)
        hou = ""
        if hours != 0:
            hou =  str(round(hours)) + " hours, "
        if min != 0:
            hou = hou +  str(round(min)) + " minutes and "
        if item['user'] == user:

            return("your song is in position " + str(num) + " and will play in approximately "+ hou  + str(round(secs)) + " seconds time")

    return("you have no songs in the queue Pepega")

def wrongsong(user):
    request = requests.get(link + "/queue" , headers = {'Authorization': MY_AUTH}).json()['data']
    if request == []:
        return('songrequest client is not on right now, check back later')
    if request[0] == []:
        return("the queue is empty")

    for item in reversed(request[0]):
        if item['user'] == user:
            body = json.dumps({"data": item['videoID']})
            request2 = requests.post(link + "/skip", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} ,  data = body).json()
            if request2['data'] == 'success':
                return(" removed " + item['title'] + " from queue")
            elif request2['data'] == "couldn't find":
                return("weird error, couldn't find song @xalhs :tf: 🤜 🔔 ")
            else:
                return("unknown error, @xalhs :tf: 🤜 🔔 ")

        #    remove song with video-id = 'videoID'

    return("you have no songs in the queue Pepega")

def volume(mag):
    thingy = {"volume": mag}
    body = json.dumps({"data": thingy})
    request = requests.post(link + "/setvolume", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} ,  data = body).json()
    #response??

def playvideo():
    print('playing')
    request = requests.post( link + "/play", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} ).json()

def pausevideo():
    print('pausing')
    request = requests.post( link + "/pause", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} ).json()

def playliston():
    print('playlist on')
    request = requests.post( link + "/playliston", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} )

def playlistoff():
    print('playlist off')
    request = requests.post( link + "/playlistoff", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} )

def loadplaylist(playlist_name):
    print('loading playlist: ' + playlist_name)
    body = json.dumps({"data": playlist_name})
    request = requests.post( link + "/loadplaylist", headers = {"Content-Type": "application/json" , 'Authorization': MY_AUTH} ,  data = body).json()

if __name__ == "__main__":


        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=devKey)

        request = youtube.search().list(
             part="snippet",
             maxResults=25,
             q="the forsen build song Lefty Mc"

         )

        response = request.execute()
        vid_id = response['items'][0]['id']['videoId']

        request2 = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=vid_id
    )
        response2 = request2.execute()
        print(response2)
        title = response2['items'][0]['snippet']['title']
        uploader = response2['items'][0]['snippet']['channelTitle']
        dur = response2['items'][0]['contentDetails']['duration']
    #main()
