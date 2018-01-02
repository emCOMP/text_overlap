#Create a matrix of counts for how many times author x refers to author y in an article
#Creates authors_counts.csv
import pandas as pd
import numpy as np


df = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', index_col=0)
author_references = pd.read_csv('authors_results_01.csv', delimiter=',', index_col=0)


texts = df.loc[:, ["Text", "Authors"]]

texts = texts.dropna(subset=["Text"])
authors = texts["Authors"]

rows = list(df.index)
rows.remove('Article URL')
cols = list(df.columns.values)

set_of_auths = set()

#Blacklist of authors, these authors are not useful and are very common
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
blacklist = ["Getty", "Image", "Email", "News", "Published"]

#Make a list of all authors from the authors column
for a in authors:
		a = a.replace("[", "")
		a = a.replace("]", "")
		a = a.replace("'", "")
		auths_pre = a.split(',')
		auths_pre = [x.strip() for x in auths_pre]
		#conditios to be useful
		auths = [x for x in auths_pre if( x not in months and x not in blacklist and len(x) > 3)]
		set_of_auths.update(auths)

list_of_auths = list(set_of_auths)
size = len(list_of_auths)
results_matrix = np.zeros((size, size))


#add counts
for r in rows:
	a = df.loc[r, "Authors"]
	a = a.replace("[", "")
	a = a.replace("]", "")
	a = a.replace("'", "")
	auths_pre = a.split(',')
	auths_pre = [x.strip() for x in auths_pre]
	#conditions to be useful
	auths = [x for x in auths_pre if( x not in months and x not in blacklist and len(x) > 3)]
	if(r in author_references.index):
		print(r)
		references = author_references.loc[r, '0']
		refs_pre = a.split(',')
		refs_pre = [x.strip() for x in refs_pre]
		#conditions to be useful
		refs = [x for x in refs_pre if( x not in months and x not in blacklist and len(x) > 3)]
		for a in auths:
			for r in refs:
				a_index = list_of_auths.index(a)
				r_index = list_of_auths.index(r)
				print(results_matrix[a_index, r_index])
				print(a_index)
				print(r_index)
				results_matrix[a_index, r_index] = results_matrix[a_index, r_index] + 1

#export			
df = pd.DataFrame(results_matrix, index=list_of_auths, columns=list_of_auths)
df.to_csv('authors_counts.csv', index=True, header=True, sep=',')


