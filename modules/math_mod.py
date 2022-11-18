import requests
import json

def math(expression):
    body = json.dumps({"expr": expression})
    request = requests.post("http://api.mathjs.org/v4/" , headers = {"content-type": "application/json"} , data = body ).json()
    print(request)
    if request["error"] == None:
        return(request["result"])
    else:
        return(request["error"])

nam ="3^2 + 4^2"
body = json.dumps({"expr": nam})
request = requests.post("http://api.mathjs.org/v4/" , headers = {"content-type": "application/json"} , data = body ).json()
print(request["result"])
