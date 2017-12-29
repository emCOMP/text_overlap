import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
from nltk.util import ngrams
import datetime

df = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', encoding='latin1')

texts = df.loc[:, ["Text", "Article URL"]]
texts = texts.dropna(axis=0, how="any")
text = texts["Text"]

num = len(text)
print(num)
print(len(texts.loc[0:2000,"Article URL"]))
text_test = list(text[0:num])

i_grams = np.empty((num, 5), dtype=object)
i = 0
for t in text_test:
        i_grams[i, 0] = list(ngrams(t.split(), 200))
        i_grams[i, 1] = list(ngrams(t.split(), 150))
        i_grams[i, 2] = list(ngrams(t.split(), 100))
        i_grams[i, 3] = list(ngrams(t.split(), 50))
        i_grams[i, 4] = list(ngrams(t.split(), 20))
        print(i)
        i = i+1

print(i_grams)
results_matrix_lengths = np.empty((num, num), dtype=object)

for i in range(0, 20):
        print(i)
       	for j in range(i+1, num):
            string = "counts:("
            for k in range(0, 4):
                a = i_grams[i][k]
                b = i_grams[j][k]
                b = set(tuple(t) for t in b)
                a = set(tuple(t) for t in a)
                for x in a.intersection(b):
                    print(len(x))
                    print k
                    '''
                if(k == 0):
                        results_matrix_lengths_200[i][j] = len(a.intersection(b))
                elif (k==1):
                        results_matrix_lengths_150[i][j] = len(a.intersection(b))
                elif(k==2):
                        results_matrix_lengths_100[i][j] = len(a.intersection(b))
                elif(k==3):
                        results_matrix_lengths_50[i][j] = len(a.intersection(b))
                elif(k==4):
                        results_matrix_lengths_20[i][j] = len(a.intersection(b))
                        '''

df1 = pd.DataFrame(results_matrix_lengths_200, index=texts.loc[0:2000,"Article URL"], columns=texts.loc[0:2000,"Article URL"])
df2 = pd.DataFrame(results_matrix_lengths_150, index=texts.loc[0:2000,"Article URL"], columns=texts.loc[0:2000,"Article URL"])
df3 = pd.DataFrame(results_matrix_lengths_100, index=texts.loc[0:2000,"Article URL"], columns=texts.loc[0:2000,"Article URL"])
df4 = pd.DataFrame(results_matrix_lengths_50, index=texts.loc[0:2000,"Article URL"], columns=texts.loc[0:2000,"Article URL"])
df5 = pd.DataFrame(results_matrix_lengths_20, index=texts.loc[0:2000,"Article URL"], columns=texts.loc[0:2000,"Article URL"])
'''
df1.to_csv('ngram_category_count_200.csv', index=True, header=True, sep=',')
df2.to_csv('ngram_category_count_150.csv', index=True, header=True, sep=',')
df3.to_csv('ngram_category_count_100.csv', index=True, header=True, sep=',')
df4.to_csv('ngram_category_count_50.csv', index=True, header=True, sep=',')
df5.to_csv('ngram_category_count_20.csv', index=True, header=True, sep=',')
'''


