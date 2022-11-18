import requests
import time
from modules.Settings import CLIENT_ID, BROADCASTER_ID, OAUTH


client_id = CLIENT_ID
broadcaster_id_str = BROADCASTER_ID
Oauth = OAUTH

def Clip():

    clip_request = requests.post("https://api.twitch.tv/helix/clips?broadcaster_id=" + broadcaster_id_str, headers={"client-id": client_id , "Authorization": "Bearer " + Oauth ,"Accept": "application/vnd.twitchtv.v5+json" ,"Content-Type": "application/json" , "broadcaster-id" : broadcaster_id_str})
    print(clip_request.text)
    clip_id = ((clip_request.text).split('"id":"')[1]).split('"')[0]

    print("clip id = " + clip_id)
    time.sleep(20)
    request4 = requests.get("https://api.twitch.tv/helix/clips?id=" + clip_id , headers={"client-id": client_id})
    print(request4.text)
    #open clip in some kind of window
