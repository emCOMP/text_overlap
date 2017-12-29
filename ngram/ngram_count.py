import pandas as pd
import nltk
nltk.download('punkt')
from nltk.util import ngrams
import numpy as np
import datetime

df = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', encoding='latin1')

i_grams = pd.read_csv('ngram_results.csv', delimiter=',', encoding='latin1', header=0, index_col=0)

texts = df.loc[:, ["Text", "Article URL"]]
num = 10

results_matrix_lengths = np.empty((num, num), dtype=object)

for i in range(0, num):
        print(i)
        for j in range(i+1, num):
                string = "counts:("
                for k in range(0, 4):
                        a = i_grams.iloc[k][i]
                        b = i_grams.iloc[k][j]
                        a = set(tuple(i) for i in a)

                        string = string + str(len(a.intersection(b))) + "; "
                results_matrix_lengths[i][j] = string + ")"
                print(string)
                print(results_matrix_lengths[i][j])

df = pd.DataFrame(results_matrix_lengths, index=texts.loc[0:num-1,"Article URL"], columns=texts.loc[0:num-1,"Article URL"])
df.to_csv('ngram_category_count.csv', index=True, header=True, sep=',')


