import requests
import json

#search = "Water%20pipit"
#search = "forsen"
#search = "rebecca%20black"
#search = "pizza"
#search = "justin bieber"
#search = search.replace(" ", "%20")

#request = requests.get("http://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + search + "&format=json&prop=revisions&rvprop=content&rvsection=1")
#urmom = (request.text).replace('<span class=\\"searchmatch\\">' , '')
#urmom = urmom.replace('</span>' , '')
#temp = (urmom.split('snippet":"')[1]).split('","timestamp":')[0]
#print(request.text)
#print(temp + "\n\n\n")

def wiki(in_search):
    try:
        search = in_search.replace(" ", "%20")
        request = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvprop=content&rvsection=0&titles=" +search).json()
        request_text = json.dumps(request)
        print(request_text + "\n\n\n")
        if "#REDIRECT" in  request_text:
            print("1")
            try:
                search = ((request_text).split("#REDIRECT [[")[1]).split("]]")[0]
            except:
                search = ((request_text).split("#REDIRECT[[")[1]).split("]]")[0]
            search = search.replace(" ", "%20")
            request = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvprop=content&rvsection=0&titles=" +search).json()
        print("2")
        page_id = ((json.dumps(request)).split('"pageid": ')[1]).split(', "ns":')[0]
        print("3")
        request_text = request['query']['pages'][page_id]['revisions'][0]['*']
        print(request_text + "\n\n\n")

        #temp2 = ((request_text).replace(']]' , ''))
        temp1 = request_text

        #note removal
        sepfinal_1 = temp1.split('-->')

        temp2 = ""

        for line in sepfinal_1:
            temp2 += line.split('<!--')[0]


        try:
            temp2 = temp2.split("\n\n'''" , 1)[1]
        except:
#            try:
            temp2 = temp2.split("'''" , 1)[1]
        #temp2 = temp2.split("\\n\\n")[0]
        temp2 = temp2.split("\n")[0]
        print(temp2)
        #temp2 = ((((temp2.replace('<ref name=' , '')).replace('\\', '')).replace('":0' , '')).replace('\\' , '')).replace('"/>','')
        temp2 = (temp2.replace('<ref name=\\":0\\"/>' , '')).replace('<ref name=\\":0\\" />' , '')
        nam = temp2.split('<ref')

        final1 = ""
        for strings in nam:
            try:
                final1 += strings.split('ref>')[1]
            except:
                try:
                    final1 += strings.split('/>')[1]
                except:
                    final1 += strings



        final1 = final1.replace("'''" , "")
        final1 = final1.replace("''" , "")

        print("after reference removal and ''' '' replace              "+final1 + "\n\n")


        if '{{IPA' in final1:
            sepfinal1 = final1.split('{{IPA')

            final2 = ""

            for line in sepfinal1:
                print(line + "\n\n")
                if line == sepfinal1[0]:
                    final2 += line
                else:
                    try:
                        final2 += line.split('}}' , 1)[1]
                    except:
                        final2 += line
        else:
            final2 = final1


        print("after pronounciation removal                   " + final2)

        sepfinal2 = final2.split('[[')



        final3 = ''

        for line in sepfinal2:
            print("7     " + line)
            sepsepfinal = line.split(']]')
            if line == sepfinal2[0]:
                final3 += line
            else:
                try:
                    final3 += ((sepsepfinal[0]).split('|')[1])
                    print("1")
                    print(((sepsepfinal[0]).split('|')[1]))
                #    print((line.split('|')[1]))
                    final3 += ((sepsepfinal[1]))
                    print("2")
                    print((sepsepfinal[1]))
                except:
                    final3 += line.replace(']]' , '')
                    print("3")
                    print(line.replace(']]' , ''))


        final3 = (((final3.replace('{{' , '')).replace('}}' , '')).replace('|' , ' ')).replace('\\' , '')
        final3 = final3.split('}]')[0]


        #note removal again, no reason to exist other than to not fuck up the sequence

        sepfinal3 = final3.split('-->')

        final4 = ""

        for line in sepfinal3:
            final4 += line.split('<!--')[0]



        print("\n\n")
        print(final4)
        print("\n\n")
        i = 0
        part = []
        part.append(final4)
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
        #print(final4)
        print(part[0])
        print("\n\n")
        return part
        #/w/api.php?action=query&format=json&list=search&srsearch=Craig%20Noone
    except:
        if in_search.endswith("#"):
            return "no info found for " +  in_search
        else:
            part = ["no info found for " +  in_search]
            return part

    #    return "no info found for " +  in_search
