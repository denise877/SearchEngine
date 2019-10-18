import re
from collections import defaultdict
from html.parser import HTMLParser
import json
import pymongo
import math
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

fileCount = 0
stopwords = set(stopwords.words("english"))
indexDict = defaultdict(list)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SearchEngine2"]
mycol = mydb["Posting2"]

class MyHtmlParser(HTMLParser):
    currentTag = None
    allData = list()

    def handle_starttag(self, tag, attrs):
        self.currentTag = tag

    def handle_data(self, data:str):
        if self.currentTag not in set(["script","style"]):
            text = data.strip()
            if text is not '' :
                self.allData.append(text)

def postDatabase(freqTable:dict,fileId:str):
    for token in freqTable.keys():
        dbEntry = mycol.find_one({"name":token})
        if dbEntry is None:
            mycol.insert_one({"name":token, "files":[(fileId,freqTable[token])]})
        else:
            curData:list = dbEntry["files"]
            curData.append((fileId,freqTable[token]))
            mycol.update_one({"name":token}, {"$set":{"files":curData}})

def tokenize (dataList:list, fileId:str):
    #global indexDict
    wordCount = 0
    dict = defaultdict(float)
    for line in dataList:
        wlist = re.findall(r'[A-Za-z0-9\']+',line)
        for word in wlist:
            if len(word) > 2 and word not in stopwords:
                dict[word.lower()] += 1
                wordCount += 1
    #for i in dict :
        #dict[i] /= wordCount # calc tf here
        #indexDict[i].append((fileId,dict[i]))
    return dict
    #for w, t in sorted(dict.items(), key=lambda d: (-d[1],d[0])) :
        #print(w,"\t",t)

#iFile = "/Users/ZP/Desktop/WEBPAGES_RAW/0/2"
def parseFile (fileId:str):
    global fileCount
    dir = fileId.split("/")
    #iFile = "/Users/ZP/Desktop/WEBPAGES_RAW/" + dir[0] + "/" + dir[1]
    iFile = "C:\\Users\\rdfzz\\Desktop\\WEBPAGES_RAW\\" + dir[0] + "\\" + dir[1]
    with open(iFile,'r',encoding='utf-8') as iFile:
        parser = MyHtmlParser()
        parser.feed(iFile.read())
        tokenResult = tokenize(parser.allData,fileId)
        for key in tokenResult.keys():
            indexDict[key].append((fileId,tokenResult[key]))
            #indexDict[key] = ListNode((fileId,tokenResult[key]),indexDict[key])
        #postDatabase(tokenResult,fileId)
    iFile.close()
    print(fileId," job complete.\tTotal ",fileCount)
    fileCount += 1

def parseFile2 (fileId:str):
    global fileCount
    dir = fileId.split("/")
    #iFile = "/Users/ZP/Desktop/WEBPAGES_RAW/" + dir[0] + "/" + dir[1]
    iFile = "C:\\Users\\rdfzz\\Desktop\\WEBPAGES_RAW\\" + dir[0] + "\\" + dir[1]
    soup = BeautifulSoup(open(iFile,'r',encoding='utf-8'), "lxml")
    text = soup.get_text()
    for i in range(10):
        for j in soup.find_all("title"):
            text += " " + j.text
    for i in range(5):
        for j in soup.find_all("h1"):
            text += " " + j.text
        for j in soup.find_all("h2"):
            text += " " + j.text
        for j in soup.find_all("h3"):
            text += " " + j.text
        for j in soup.find_all("h4"):
            text += " " + j.text
        for j in soup.find_all("h5"):
            text += " " + j.text
        for j in soup.find_all("h6"):
            text += " " + j.text
    for j in soup.find_all("b"):
        text += " " + j.text
    for j in soup.find_all("li"):
        text += " " + j.text
    tokenResult = tokenize(text,fileId)
    for key in tokenResult.keys():
        indexDict[key].append((fileId,tokenResult[key]))
    print(fileId," job complete.\tTotal ",fileCount)
    fileCount += 1
        
def main ():
    mycol.delete_many({})
    allFiles = list()
    #with open("/Users/ZP/Desktop/WEBPAGES_RAW/bookkeeping.json") as iFile:
    with open("C:\\Users\\rdfzz\\Desktop\\WEBPAGES_RAW\\bookkeeping.json") as iFile:
        load_dict = json.load(iFile)
        for k in load_dict.keys():
            allFiles.append(k)
    iFile.close()

    #count = 0
    for fileId in allFiles:
        #if (count < 100):
        parseFile2(fileId)
        #count += 1

    #for i in indexDict.items():
        #print(i)
    count = 0
    for k,v in indexDict.items():
        #df = len(v)
        #v = sorted(v, key=lambda x:x[1], reverse=True)
        #alist = list()
        #while v != None and v.value != None:
            #alist.append(v.value)
            #v.head = v.next
        mycol.insert_one({"index":k, "docList":sorted(v, key=lambda x:x[1], reverse=True), "idf":math.log10(37497/len(v))})
        if count % 1000 == 0:
            print("Inserting term: ",count)
        count += 1

    for i in mycol.find():
        print(i)
    #mycol.delete_many({})

if __name__ == '__main__':
    #en_stops = set(stopwords.words('english'))
    main()
