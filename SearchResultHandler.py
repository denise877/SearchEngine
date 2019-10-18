import pymongo
import math
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import numpy as np

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SearchEngine"]
mycol = mydb["Posting"]
mydict = mydb["Dictionary"]

def handleMultipleQuery (alist:list) -> list:
    query_length = len(alist)
    rank_dict = dict()
    query_dict = defaultdict(int)

    # document-term matrix
    pos = 0
    for w in alist:
        query_dict[w] += 1
        terminfo = mycol.find_one({"index":w})
        if terminfo != None:
            for doc in terminfo["docList"]:
                if doc[0] not in rank_dict.keys():
                    rank_dict[doc[0]] = np.zeros(query_length)
                rank_dict[doc[0]][pos] = (1 + math.log10(doc[1])) * terminfo["idf"]
        pos += 1
    # normalization
    for k in rank_dict.keys():
        agg = np.sqrt(sum(rank_dict[k]**2))
        rank_dict[k] = rank_dict[k] / agg
    # query normalization
    query_weight = []
    for w in alist:
        query_weight.append((1 + math.log10(query_dict[w])) * mycol.find_one({"index":w})["idf"])
    query_weight = np.array(query_weight)
    query_weight = query_weight / np.sqrt(sum(query_weight**2))
    # dot product
    for k in rank_dict.keys():
        rank_dict[k] = np.dot(rank_dict[k], query_weight)
    '''
    for w in alist:
        terminfo = mycol.find_one({"index":w})
        for doc in terminfo["docList"]:
            rank_dict[doc[0]] += (1 + math.log10(doc[1])) * terminfo["idf"]
    '''
    count = 0
    result = list()
    for k,v in sorted(rank_dict.items(), key=lambda d: -d[1]):
        result.append(k)
        count += 1
        if count >= 20:
            break
    return result

def handleSingleQuery (astr:str) -> list:
    terminfo = mycol.find_one({"index":astr})
    result = list()
    count = 0
    if terminfo is None:
        return result
    for doc in terminfo["docList"]:
        result.append(doc[0])
        count += 1
        if count >= 20:
            break
    return result

def getTitleLinkFromDocId (idList:list) -> list:
    result = list()
    for id in idList:
        info = mydict.find_one({"docId":id})
        result.append((info["link"],info["title"]))
    return result