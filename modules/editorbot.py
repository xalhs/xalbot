import requests
import json
from modules.Settings import CHANNEL, CLIENT_ID, OAUTH, BROADCASTER_ID

client_id = CLIENT_ID
OAuth = OAUTH
broadcaster_id = BROADCASTER_ID
channel = CHANNEL

def titlechange(title):

    body = json.dumps({"title": title})
    request2 = requests.patch('https://api.twitch.tv/helix/channels?broadcaster_id=' + broadcaster_id, headers = {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH, "Accept": "application/vnd.twitchtv.v5+json" ,"Content-Type": "application/json"}, data = body)

    request3 = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + broadcaster_id, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
    new_title= request3['data'][0]['title']

    try:
        if new_title == title:
            return 'changed title to "' + new_title + '"'
        elif request2.status_code == 400:
            return 'error 400: Missing Query Parameter'
        elif request2.status_code == 500:
            return 'error 500: Internal Server Error; Failed to update channel'
        elif 'error' in request2.json():
            return 'error ' + str(request2.json()['status']) + ", " + request2.json()['error'] + "; " + request2.json()['message']
        else:
            return 'something went wrong with titlechange command'
    except:
        print("UNKNOWN ERROR WITH TITLECHANGE")


def gamechange(game):

    if game.lower() == "none":
        game_id = 0
        body = json.dumps({"game_id": game_id})
        request2 = requests.patch('https://api.twitch.tv/helix/channels?broadcaster_id=' + broadcaster_id, headers = {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH, "Accept": "application/vnd.twitchtv.v5+json" ,"Content-Type": "application/json"}, data = body)
        if request2.status_code == 204:
            return "incognito mode activated EZY"
        else:
            return "something went wrong with the titlechange command"

    request0 = requests.get('https://api.twitch.tv/helix/games?name=' + game, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
    if request0['data'] == []:
        request1 = requests.get('https://api.twitch.tv/helix/search/categories?query=' + game, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
        if request1['data'] == None:
            return "couldn't find game"
        else:
            game_id = request1['data'][0]['id']
    else:
        game_id = request0['data'][0]['id']

    body = json.dumps({"game_id": game_id})
    request2 = requests.patch('https://api.twitch.tv/helix/channels?broadcaster_id=' + broadcaster_id, headers = {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH, "Accept": "application/vnd.twitchtv.v5+json" ,"Content-Type": "application/json"}, data = body)

    try:
        if request2.status_code == 204:
            request3 = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + broadcaster_id, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
            new_game= request3['data'][0]['game_name']
            return "updated game to " + new_game
        elif request2.status_code == 400:
            return 'error 400: Missing Query Parameter'
        elif request2.status_code == 500:
            return 'error 500: Internal Server Error; Failed to update channel'
        elif 'error' in request2.json():
            return 'error ' + str(request2.json()['status']) + ", " + request2.json()['error'] + "; " + request2.json()['message']
        else:
            return 'something went wrong with gamechange command'
    except:
        print("UNKNOWN ERROR WITH GAMECHANGE")
