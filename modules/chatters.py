import requests
import json
from modules.Settings import CHANNEL, CLIENT_ID, OAUTH, BROADCASTER_ID
client_id = CLIENT_ID
OAuth = OAUTH
broadcaster_id = BROADCASTER_ID
channel = CHANNEL

def chatters_old(CHANNEL):
    request = requests.get("https://tmi.twitch.tv/group/user/" + CHANNEL + "/chatters").json()

    chatters = ["xalhs"]

    mods = request['chatters']['moderators']
    vips = request['chatters']['vips']
    staff = request['chatters']['staff']
    admins = request['chatters']['admins']
    gmods = request['chatters']['global_mods']
    viewers = request['chatters']['viewers']

    chatters += mods + vips + staff + admins + gmods + viewers

    return chatters

def chatters():
    chatters = {}
    request = requests.get('https://api.twitch.tv/helix/chat/chatters?broadcaster_id=' + broadcaster_id + '&moderator_id=' + broadcaster_id + '&first=1000', headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
    for chatter in request['data']:
        chatters[chatter['user_login']] = chatter['user_id']
    while request['pagination'] != {}:
        cursor = request3['pagination']['cursor']
        request = requests.get('https://api.twitch.tv/helix/chat/chatters?broadcaster_id=' + broadcaster_id + '&moderator_id=' + broadcaster_id + '&first=1000&after=' + cursor, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
        for chatter in request['data']:
            chatters[chatter['user_login']] = chatter['user_id']
    return chatters
