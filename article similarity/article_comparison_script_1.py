#Script to go through articles and create a matrix of 'similarity'
#similarity is determined by the cosine difference of tf-idf

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
import numpy as np

df = pd.read_csv('scraped_articles_01.csv', delimiter=',')


texts = df.loc[:, ["Text", "Article URL"]]
texts = texts.dropna(axis=0, how="any")
text = texts["Text"]

num = len(text)

text_test = text[1:num]

tfidf_vectorizer = TfidfVectorizer(decode_error="ignore")
tfidf_matrix = tfidf_vectorizer.fit_transform(text_test)

results_matrix = np.zeros((len(text_test), len(text_test)))
print len(text_test)
print len(texts.loc[:, "Article URL"])
print text_test.shape
print texts.shape

for i in range(0, len(text_test)):
        for j in range(i+1, len(text_test)):
                results_matrix[i,j] = cosine_similarity(tfidf_matrix[i, :], tfidf_matrix[j, :])

df = pd.DataFrame(results_matrix, index=texts.loc[0:len(text_test),"Article URL"], columns=texts.loc[0:len(text_test),"Article URL"])
df.to_csv('results_01.csv', index=True, header=True, sep=',')
total = (results_matrix > .9).sum()
print total
