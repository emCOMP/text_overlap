#Fro the list of authors for each article, see how many other articles mention the author
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
import numpy as np
from difflib import SequenceMatcher

df = pd.read_csv('scraped_filtered_articles.csv', delimiter=',')

texts = df.loc[:, ["Text", "Article URL", "Authors"]]
texts = texts.dropna(subset=["Text", "Article URL"])
text = texts["Text"]
authors = texts["Authors"]
urls = texts["Article URL"]
set_of_auths = set()

num = len(text)
text_test = text[0:num]

results_matrix = np.empty((len(text_test), 1), dtype=object)

#Blacklist of authors, these authors are not useful and are very common
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
blacklist = ["Getty", "Image", "Email", "News", "Published"]

#Make a list of all authors from the authors column
for i in range(0, len(authors)):
	if(i in authors):
		a = authors[i]
		a = a.replace("[", "")
		a = a.replace("]", "")
		a = a.replace("'", "")
		auths_pre = a.split(',')
		auths_pre = [x.strip() for x in auths_pre]
		#conditions to be useful
		auths = [x for x in auths_pre if( x not in months and x not in blacklist and len(x) > 3)]
		set_of_auths.update(auths)

#print(set_of_auths)

#make a list of authors in each text
for i in range(0, len(text_test)):
	if(i in text_test):
		text = text_test[i]
		a = ""
		for j in set_of_auths:
			if (j in text and not (j in authors[i])):
				a = a + j + ", "
		results_matrix[i][0] = a    

df = pd.DataFrame(results_matrix, index=urls)
df.to_csv('authors_results_01.csv', index=True, header=True, sep=',')


