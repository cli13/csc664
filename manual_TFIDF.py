import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import re

ps = PorterStemmer()
#getting googlesheets to work on python
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Canra\Desktop\csc664\project_secret.json", scope)
client = gspread.authorize(credentials)
#opening spreadsheet called drug marketable and getting sheet1
ss = client.open('drug marketable')
ws = ss.worksheet('Sheet1')

tweets = ws.col_values(4)

#tokenize all tweets
tweets = [[word for word in tweet.lower().split()] for tweet in tweets]

#make a list for each tweet and in each tweet are words. The word in the list are stem and special characters such as hashtags are removed
bagOfWords = []
docOfWords = []
for tweet in tweets:
    for word in tweet:
        word = re.sub(r"[^a-zA-Z0-9]","",word)
        word = ps.stem(word)
        bagOfWords.append(word)
    docOfWords.append(bagOfWords)
    bagOfWords = []

trimmed = []
#remove items in list with empty
for bow in docOfWords:
    for w in bow:
        if w != '':
            bagOfWords.append(w)
    trimmed.append(bagOfWords)
    bagOfWords = []

#get a dictionary going
dictionary = set(trimmed[0]).union(set(trimmed[1]))
for bag in trimmed[2:]:
    dictionary = set(bag).union(set(dictionary))

print(len(dictionary))

def computeTF(wordDict, bagOfWords):
    '''calculating the tf score'''
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

def computeIDF(documents):
    ''' compute the idf for document'''
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf

#finding the the idf
docNumberofWords = []
for tweet in trimmed:
    numberOfWords = dict.fromkeys(dictionary, 0)
    for word in tweet:
        numberOfWords[word] += 1
    docNumberofWords.append(numberOfWords)
    numberOfWords = []

idf = computeIDF(docNumberofWords)

#calculating the tfidf
tfidfALL = []
numberOfWords = []
for tweet in trimmed:
    numberOfWords = dict.fromkeys(dictionary, 0)
    for word in tweet:
        numberOfWords[word] += 1
        bagOfWords.append(word)
    tf = computeTF(numberOfWords, bagOfWords)
    tfidf = computeTFIDF(tf, idf)
    tfidfALL.append(tfidf)
    numberOfWords = []
    bagOfWords = []

df = pd.DataFrame(tfidfALL)
df.to_csv(r'C:/Users/Canra/Desktop/csc664/manual.csv', index = False)

