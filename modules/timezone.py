import requests
import json

def germany_time():
    request = requests.get("http://worldtimeapi.org/api/timezone/Europe/Berlin").json()

    print(request['datetime'])

    time = request['datetime'].split("T" , 1)[1]
    time = time.split(".")[0]

    print(time)
    return time


def timezone(zone):
    word = zone.lower()
    request_0 = requests.get("http://worldtimeapi.org/api/timezone").json()
    for element in request_0:
        if element.lower().endswith("/" + word):
            request = requests.get("http://worldtimeapi.org/api/timezone/" + element).json()
            print(element)
            print(request['datetime'])

            time = request['datetime'].split("T" , 1)[1]
            time = time.split(".")[0]
            return("time in " + zone + " is " + time)
        elif ("/" + zone + "/").lower() in ("/" + element).lower():
            return("request a more specific location in " + zone)



        print (element)
    return("couldn't find location " + zone)

#print(request)

#    time = request['datetime'].split("T" , 1)[1]
#    time = time.split(".")[0]

#    print(time)
