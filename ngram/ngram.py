import pandas as pd
import nltk
nltk.download('punkt')
from nltk.util import ngrams
import numpy as np
import datetime

df = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', encoding='latin1')

texts = df.loc[:, ["Text", "Article URL"]]
texts = texts.dropna(axis=0, how="any")
text = texts["Text"]

num = 10
print(num)
print(len(texts.loc[0:2000,"Article URL"]))
text_test = list(text[0:num])

i_grams = np.empty((5, num), dtype=object)
i = 0
for t in text_test:
        i_grams[0, i] = list(ngrams(t.split(), 200))
        i_grams[1, i] = list(ngrams(t.split(), 150))
        i_grams[2, i] = list(ngrams(t.split(), 100))
        i_grams[3, i] = list(ngrams(t.split(), 50))
        i_grams[4, i] = list(ngrams(t.split(), 20))
        print(i)
        i = i+1
df = pd.DataFrame(i_grams, index=[200, 150, 100, 50, 20], columns=texts.loc[0:11,"Article URL"])
print(df)
df.to_csv('ngram_results.csv', index=True, header=True, sep=',')