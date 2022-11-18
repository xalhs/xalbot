import requests
#from modules.Settings import CLIENT_ID, BROADCASTER_ID
#clint_id = CLIENT_ID
#request2 = requests.get("https://api.twitch.tv/kraken/channels/" + id, headers={"client-id": client_id ,"Accept": "application/vnd.twitchtv.v5+json" ,"Content-Type": "application/json" , "broadcaster-id" : BROADCASTER_ID})

#channel = "xalhs"

def followage (user , channel):
    if user == channel:
        return("a user cannot follow themself")
    request = requests.get("https://api.2g.be/twitch/followage/" + channel + "/" + user +"?format=mwdhms")
    return(request.text)
