What everyfile means
====================
dataset.csv - the data that was fetch on twitter. That was occupied in the googlesheets. I exported it as a csv file
project_secret.json - the secret information to access googlesheet api
manual_TFIDF.py - the python ode used to calculate tfidf manually
sklearn.py - the python code use to calculate tfidf using sklearn's TfidfVectorizer
top15mean.csv - the output of the top 15 most meaningful words of the entire dataset from both the manual code and sklearn's code
sklearn.csv - the tfidf for each word for each tweet from sklearn's TfidfVecorizer
manual.csv - the tfidf for each word for each tweet from our manual tfidf calculations
manual(test_data).csv - the output matrix for testing manual_TFIDF.py to make sure everything works (only contains the output of three tweets)

