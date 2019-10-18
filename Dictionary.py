import pymongo
import json
from bs4 import BeautifulSoup
import re

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SearchEngine"]
mycol = mydb["Dictionary"]

def loadDictionary():
    #with open("/Users/ZP/Desktop/WEBPAGES_RAW/bookkeeping.json",'r',encoding='utf-8') as indexFile:
    with open("C:\\Users\\rdfzz\\Desktop\\WEBPAGES_RAW\\bookkeeping.json",'r',encoding='utf-8') as indexFile:
        d = json.load(indexFile)
    indexFile.close()
    count = 1
    for k in d.keys():
        soup = BeautifulSoup(open("C:\\Users\\rdfzz\\Desktop\\WEBPAGES_RAW\\"+k, 'r', encoding='utf-8'), "lxml")
        #soup = BeautifulSoup(open("/Users/ZP/Desktop/WEBPAGES_RAW/"+k, 'r', encoding='utf-8'), "lxml")
        for s in soup('script'):
            s.extract()
        # get doc title
        if soup.title != None and soup.title.string != None:
            title = soup.title.string
        else:
            title = d[k]
        # get doc length
        text = soup.get_text()
        words = re.split("[^a-zA-Z0-9]", text)
        mycol.insert_one({"docId":k , "title":title, "link":d[k], "length":len(words)})
        count += 1
        print(k + "\t" + str(count))

def showDictionary():
    for i in mycol.find():
        print(i)

loadDictionary()
showDictionary() 
