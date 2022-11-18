import requests
import json

def chatters(CHANNEL):
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
