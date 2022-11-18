import time
import random
import codecs

def pasta():
    n = 0
    f = codecs.open("var/Resources/pastas.txt","r+" , "utf-8")
#    l = 1
    for line in f:
    #    print(l)

        if line.strip() == '':
            n = n + 1
#            print( "line = " + str(l))
#        l = l + 1
    print("n =" + str(n))
    f.seek(0)
    r = random.randint(1,n)
    paste = ""
#    l = 1
    for line in f:
        if r == n + 1:
#            print("reddit")
            paste = paste + line
#        print("l =" + str(l))
        if line.strip() == '':
            r = r + 1
#            print("r = " + str(r))

#        l = l + 1
    f.close()
    return paste

def addpasta(message):
    Failure = False
    f = codecs.open("var/Resources/pastas.txt","r+" , "utf-8")
    for line in f:
        if line == message:
            Failure = True
    f.close()
    if Failure == False:
        f = codecs.open("var/Resources/pastas.txt","a+" , "utf-8")
        f.write("\r\n")
        f.write("\r\n")
        f.write(message)
        f.close()
        return 1
    if Failure == True:
        return 0
