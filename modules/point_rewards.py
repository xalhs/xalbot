import requests
from modules.Settings import BROADCASTER_ID, CLIENT_ID, OAUTH
import json

url = 'https://api.twitch.tv/helix/channel_points/custom_rewards'
broadcaster_id = BROADCASTER_ID
client_id = CLIENT_ID

def CreateReward(params):
    name = params[0]
    cost = params[1]
    try:
         user_input = params[2].replace(" " , "")
    except:
         user_input = False

    try:
        if isinstance(cost, int):
            pass
        else:
            cost = int(cost.replace(" ",""))
    except:
        return("cost wasn't an integer")

    if user_input.lower() == "true":
        user_input = True
    elif user_input.lower() == "false" or user_input == False:
        user_input = False
    else:
        return "error determining whether user input is required"
    body = json.dumps({"title": name , "cost": cost , "is_user_input_required": user_input })
    request = requests.post(url + '?broadcaster_id=' + broadcaster_id , headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH , "Content-Type": "application/json" }, data = body).json()
    print(request)
    try:
        return str("error: " + request['status']) + " " + request['message']
    except:
        return "Reward created successfully"

def getRewardCode(reward):
    request = requests.get(url + '?broadcaster_id=' + broadcaster_id, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH , "Content-Type": "application/json"}).json()
    #print(request)
    for rewardnumber in request['data']:
        if rewardnumber['title'] == reward:
            return rewardnumber['id']

def UpdateRewardStatus(argument_list):
    reward_name = argument_list[0]
    id = argument_list[1]
    status = argument_list[2]
    reward_id = getRewardCode(reward_name)
    body = json.dumps({"status": status})
    request = requests.patch(url+'/redemptions' + '?broadcaster_id=' + broadcaster_id + '&reward_id=' + reward_id + '&id=' + id, headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH , "Content-Type": "application/json"}, data = body).json()
    print(request)


def getRedemptionid(user , message , reward_id):
    request = requests.get(url+'/redemptions' + '?broadcaster_id=' + broadcaster_id + '&reward_id=' + reward_id + '&status=UNFULFILLED', headers= {"client-id": client_id , 'Authorization': 'Bearer ' + OAUTH}).json()
    #print(request)
    for redemption in request['data']:
        if redemption['user_input'] == message and redemption['user_login'] == user:
            print(redemption['id'])
            return redemption['id']
