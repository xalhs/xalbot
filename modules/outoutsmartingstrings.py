import os

def baseletter(string):
    for filename in os.listdir("var/LetterReplacement"):
        file = open("var/LetterReplacement/" + filename , encoding = "utf16")
        for line in file:
            if line.rstrip("\n") in string:
                string = string.replace(line.rstrip("\n") , filename.replace(".txt" , ""))
    return string
