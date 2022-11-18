import requests
#term = "simp"
import traceback

def urban(term):
    try:
        request = requests.get("http://api.urbandictionary.com/v0/define?term=" + term).json()
        print(request)

        definition = request['list'][0]['word']
        #(((request.text).split('"permalink":"http://')[1]).split('.urbanup.')[0]).replace("-" , " ")
        #print("nam")
        nam = request['list'][0]['definition']
    ##    nam = (nam.replace('\\n', ' ')).replace('\\r' , ' ')
        #.split('\\n')[0]).split('\\r')[0])

        #print(nam)
        rem1 = nam.split('[')

        con1 = ""
        for things in rem1:
            con1 += things

        rem2 = con1.split(']')

        con2 = ""
        for things in rem2:
            print(things)
            con2 += things

        almost_final = con2

        print( definition + ": " + almost_final )
        final = definition + ": " + almost_final
        final = final.replace('\r' , ' ').replace('\n' , " ")
    #    final = final.replace("\\" , "")
        i = 0
        part = []
        part.append(final)
        while len(part[i]) > 500:
            lendif = len(part[i]) - 500
            temp = part[i]
            part[i] = temp[: -(lendif + 3)]
            #part[i+1] = part[i].rsplit(" " , 1 )[1]
            part.append(part[i].rsplit(" " , 1 )[1])
            part[i] = part[i].rsplit(" " , 1 )[0]
            part[i] = part[i] + "..."
            part[i+1] += temp[-(lendif + 3):]
            i+= 1
        return part
    except:
        traceback.print_exc()
        part = ["no info found for " +  term]
        return part
    #    return "no info found for " +  term
