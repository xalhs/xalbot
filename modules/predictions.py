import requests
import json
from modules.Settings import CHANNEL, CLIENT_ID, OAUTH, BROADCASTER_ID

client_id = CLIENT_ID
OAuth = OAUTH
broadcaster_id = BROADCASTER_ID
channel = CHANNEL
url = "https://api.twitch.tv/helix/predictions"

def create_prediction(argument_list):
    title = argument_list[0]
    outcome1 = argument_list[1]
    outcome2 = argument_list[2]
    try:
        window = int(argument_list[3].replace(" ",""))
    except:
        window = 60

    outcomes = [{"title" : outcome1} , {"title" : outcome2}]
    body = json.dumps({"broadcaster_id" : broadcaster_id  , "title" : title , "outcomes" : outcomes , "prediction_window" : window} )
    request = requests.post(url , headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH , "Content-Type": "application/json"} , data = body).json()
    try:
        return str("error: " + request['status']) + " " + request['message']
    except:
        return "Prediction created"

def end_prediction(text):
    request = requests.get(url + '?broadcaster_id=' + broadcaster_id, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
    id = request["data"][0]['id']
    status = request["data"][0]['status']
    outcome1_id = request["data"][0]['outcomes'][0]["id"]
    outcome2_id = request["data"][0]['outcomes'][1]["id"]
    winning_outcome_id = ""
    if status == "ACTIVE" or "LOCKED":
        if text.lower() == "outcome 1":
            new_status = "RESOLVED"
            winning_outcome_id = outcome1_id


        if text.lower() == "outcome 2":
            new_status = "RESOLVED"
            winning_outcome_id = outcome2_id

        if text.upper() == "LOCK":
            if status == "LOCKED":
                return " Prediction is already locked"
            new_status = "LOCKED"
        if text.upper() == "CANCEL":
            new_status = "CANCELED"
        body = json.dumps({"broadcaster_id" : broadcaster_id  , "id": id, "status": new_status, "winning_outcome_id": winning_outcome_id})
        request2 = requests.patch(url , headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH , "Content-Type": "application/json"} , data = body).json()
        try:
            return str(request2['status']) + " " +  request2['message']
        except:
            return "Prediction " + request2['data'][0]['status']
    else:
        return " No active prediction found"
