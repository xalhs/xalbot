import requests
from modules.Settings import CLIENT_ID, BROADCASTER_ID
client_id = CLIENT_ID
broadcaster_id_str = BROADCASTER_ID

def shoutout(channel):
    if channel.startswith("@"):
        channel = channel.strip("@")
    request = requests.get("https://api.twitch.tv/kraken/users?login=" + channel, headers={"client-id": client_id ,"Accept": "application/vnd.twitchtv.v5+json" ,"Content-Type": "application/json" , "broadcaster-id" : broadcaster_id_str})


    print(request.text)

    id = ((request.text).split('id":"')[1]).split('"')[0]
    print(id)
    request2 = requests.get("https://api.twitch.tv/kraken/channels/" + id, headers={"client-id": client_id  ,"Accept": "application/vnd.twitchtv.v5+json" ,"Content-Type": "application/json" , "broadcaster-id" : broadcaster_id_str})

    print(request2.text)
    print(channel.lower())
    part1 = (request2.text).split('","_id":"' + id + '","name":"' + channel.lower() + '","created_at":"')[0]
    part2 = (request2.text).split('","_id":"' + id + '","name":"' + channel.lower() + '","created_at":"')[1]

    print(part1)
    name = (part1.rsplit('"display_name":"' , 1)[1]).split('","game":')[0]
    game = (part1.rsplit('","game":"' , 1)[1]).split('","language"')[0]
    url = (part2.split('"url":"')[1]).split('","')[0]

    print("go and follow " + name + " at " + url + " they were last seen streaming " + game)
    return("go and follow " + name + " at " + url + " they were last seen streaming " + game)
    #f = open("GeneralFolder/shoutouttest/text.txt", "w+")
    #for channels in sep:
    #    print("1")
    #    print(channels + "\n\r" +"\r\n")
    #    f.write(channels + "\n\r" +"\r\n")


    #    f.close()
    #unsep = (request.text).split(channel)
    #list = ""
    #for line in unsep:
    #    unsep2 = line.split('"')[0]
    #
    #    print(channel + unsep2)
