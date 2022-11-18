import string
from modules.Socket import sendMessage
def joinRoom(s , mode = "not silent"):
  readbuffer = ""
  Loading = True
  while Loading:
      print("begin loading")
      byterecv=s.recv(1024)
      stringrecv= byterecv.decode("utf-8")
      readbuffer = readbuffer + stringrecv
      temp = str.split(readbuffer, "\n")
      readbuffer = temp.pop()
      print("printing lines")

      for line in temp:
          print(line)
          Loading = loadingComplete(line, Loading)
          print(Loading)
      messageTemp = "CAP REQ :twitch.tv/tags" #PRIVMSG #xalhs :Hello
      messageTemp2 = "CAP REQ :twitch.tv/commands"
  a4 = messageTemp + "\r\n"
  a5 = messageTemp2 + "\r\n"
  s.sendall(a4.encode("utf-8"))
  print("Sent: " + messageTemp)
  s.sendall(a5.encode("utf-8"))
  print("Sent: " + messageTemp2)
  if mode != "silent":
      sendMessage(s, "dot")


def loadingComplete(line, Loading):
        if("End of /NAMES list" in line):
            return False
        else:
            return Loading
