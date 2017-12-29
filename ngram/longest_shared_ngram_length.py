import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
import numpy as np
from difflib import SequenceMatcher
import distance
import datetime

df = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',')

texts = df.loc[:, ["Text", "Article URL"]]
texts = texts.dropna(axis=0, how="any")
text = texts["Text"]

num = len(text)
text_test = list(text[0:num])

results_matrix_lengths = np.zeros((len(text_test), len(text_test)))
results_matrix_strings = np.empty((len(text_test), len(text_test)), dtype=str)
print(type(results_matrix_strings))

for i in range(0, num):
	print(i)
        for j in range(i+1, num):
        	substrings = distance.lcsubstrings(text_test[i], text_test[j], False)
        	if(j%500 == 0):
        		print(datetime.datetime.now())
        	if(len(substrings) > 0):
        		s = list(substrings)
        		if(len(s[0]) > 100):
        			print(s[0])
        			print(type(len(s[0])))
        			results_matrix_lengths[i, j] = len(s[0])
        			l = ""
        			for string in s:
        				l = l + "\n" + str(string)
        			results_matrix_strings[i, j] = l
df = pd.DataFrame(results_matrix_lengths, index=texts.loc[0:num-1,"Article URL"], columns=texts.loc[0:num-1,"Article URL"])
df.to_csv('longest_ngram_results_lengths_01.csv', index=True, header=True, sep=',')
df = pd.DataFrame(results_matrix_strings, index=texts.loc[0:num-1,"Article URL"], columns=texts.loc[0:num-1,"Article URL"])
df.to_csv('longest_ngram_results_strings_01.csv', index=True, header=True, sep=',')

