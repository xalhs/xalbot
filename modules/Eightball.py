import random

def eightball():
    r1=["As I see it, yes","NaM ❗","PepeLaugh OH NO NO NO NO","idk kev eShrug","You got Jebaited","Don’t count on it","It is certain","It is decidedly so","Most likely","My reply is no"]
    r2=["My sources say no","Outlook good","Outlook not so good","Just get a house 4House","Signs point to yes","Very doubtful","Without a doubt","Yes","Yes, definitely","You may rely on it"]
    responses = r1 + r2
    rand =  random.randint(0,19)
    return responses[rand]
