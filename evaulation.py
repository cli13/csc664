import gspread
from oauth2client.service_account import ServiceAccountCredentials
#used to debug
import pprint
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# def top_mean_feats(Xtr, features, min_tfidf=0.1, top_n=25):
#     ''' Return the top n features that on average are most important amongst documents in rows'''
#     D = Xtr.toarray()

#     D[D < min_tfidf] = 0
#     tfidf_means = np.mean(D, axis=0)
#     return top_tfidf_feats(tfidf_means, features, top_n)

# def top_tfidf_feats(row, features, top_n=25):
#     ''' Get top n tfidf values in row and return them with their corresponding feature names.'''
#     topn_ids = np.argsort(row)[::-1][:top_n]
#     top_feats = [(features[i], row[i]) for i in topn_ids]
#     df = pd.DataFrame(top_feats)
#     df.columns = ['feature', 'tfidf']
#     return df

# def iter_pd(df):
#     for val in df.columns:
#         yield val
#     for row in df.to_numpy():
#         for val in row:
#             if pd.isna(val):
#                 yield ""
#             else:
#                 yield val

# def pandas_to_sheets(pandas_df, sheet):
    # '''Updates all values in a googlesheet to match a pandas dataframe'''
    # (row, col) = pandas_df.shape
    # cells = sheet.range("A1:{}".format(gspread.utils.rowcol_to_a1(row + 1, col)))
    # for cell, val in zip(cells, iter_pd(pandas_df)):
    #     cell.value = val
    # sheet.update_cells(cells)

#getting googlesheets to work on python
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Canra\Desktop\csc664\project_secret.json', scope)
client = gspread.authorize(credentials)
#opening spreadsheet called drug marketable and getting sheet1
ss = client.open('drug marketable')
ws = ss.worksheet('Sheet1')

pp = pprint.PrettyPrinter()

#column 4 is where tweets is located
tweets = ws.col_values(4)

#creates tfidf
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(tweets)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
denselist = dense.tolist()

###output = ss.worksheet('test')
###demo = vectorizer.fit_transform([tweets[53]])
###pandas_to_sheets(top_tfidf_feats(demo, vectorizer.get_feature_names(), 10), output)

#create a dataframe and sent that data to sklearn.csv
df = pd.DataFrame(denselist, columns=feature_names)
df.to_csv(r'C:/Users/Canra/Desktop/csc664/sklearn.csv', index = False, encoding='utf-8')
#get the top 25 most meaningful word from the entire doc
#top_mean_feats(vectors, feature_names).to_csv(r'C:/Users/Canra/Desktop/csc664/top_mean.csv', index = False, encoding='utf-8')







    
    
