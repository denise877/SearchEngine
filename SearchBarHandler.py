from tkinter import *
import HtmlHandler
from SearchResultHandler import *
from nltk.corpus import stopwords

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SearchEngine"]
mycol = mydb["Posting"]
stop_words = set(stopwords.words('english'))

def showSearchBar () :
    root = Tk()
    root.title("Search")
    entry = Entry(root)
    entry.grid(row=0, column=0, padx=20, sticky=W)

    def show ():
        query_text = entry.get().strip().lower()
        if query_text != None and query_text != "":
            handleQuery(query_text)

    Button(root, text="Go", command=show).grid(row=1, column=0)
    root.mainloop()

def handleQuery (query:str) :
    splitted = query.lower().split()
    query_list = list()
    for w in splitted:
        if len(w) > 2 and w not in stop_words and mycol.find_one({"index":w}) != None:
            query_list.append(w)
    if len(query_list) == 0 or query_list[0] == "":
        docList = list()
    elif len(query_list) == 1:
        docList = handleSingleQuery(query_list[0])
    else:
        docList = handleMultipleQuery(query_list)
    linkTitles = getTitleLinkFromDocId(docList)
    HtmlHandler.handleHtml(query,linkTitles)


showSearchBar()