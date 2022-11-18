import codecs
import string

def addcommand(command, action):
    f= codecs.open("var/Resources/commands.txt","a+" , "utf-8")
    f.write("\r\n")
    f.write("\r\n")
    f.write(command + "\r\n")
    f.write(action)
    f.close()

def commands(message):
#    print(" dis da command broda")
    f = codecs.open("var/Resources/commands.txt","r+" , "utf-8")
#    list = list(f)
    statement = False
    for file_line in f:
#        print(file_line.rstrip("\n"))
        if statement == True:
#           sendMessage(s, file_line)
            f.close()
            return file_line
        if message == file_line.rstrip("\r\n"):
           statement = True
    f.close()
