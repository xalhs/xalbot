import socket
from modules.Settings import HOST, PORT, PASS, IDENT, CHANNEL

def openSocket(sender = "default"  , new_ident = IDENT, new_pass = PASS ):


    if sender == "custom":
        final_pass = new_pass
        final_ident = new_ident
    else:
        final_pass = PASS
        final_ident = IDENT

    s = socket.socket()
    s.connect((HOST,PORT))
    a1 = "PASS " + final_pass + "\r\n"
    s.sendall(a1.encode("utf-8"))
    a2 = "NICK " + final_ident + "\r\n"
    s.sendall(a2.encode("utf-8"))
    a3 = "JOIN #" + CHANNEL + "\r\n"
    s.sendall(a3.encode("utf-8"))
    print("socket connected")
    return s

def sendMessage(s, message):
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message #PRIVMSG #xalhs :Hello
        a4 = messageTemp + "\r\n"
        s.sendall(a4.encode("utf-8"))
        print("Sent: " + messageTemp)
