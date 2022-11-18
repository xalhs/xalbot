import requests

#channel = "itmejp"

def uptime(channel):
    request = requests.get("https://beta.decapi.me/twitch/uptime/" + channel) #uptime
    return(request.text)
