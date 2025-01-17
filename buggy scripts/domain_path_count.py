#Count number of times each articles
#is in a path with each other article
#outputs a large matrix where
#row is 'source', column is 'destination'

import pandas as pd
import numpy as np
import datetime
import math
import csv
from urlparse import urlparse

df = pd.read_csv('paths.csv', delimiter=',', header=None)

shape = df.shape
length = shape[1]
height = shape[0]
print shape
urls = np.empty(shape)
urls[:, :] = 0

#Getting the date from the paths.csv format (which is a bit weird)
def get_url(entry):
	if(isinstance(entry, basestring)):
		e = entry.split("datetime.")
		url = e[0]
		url = url[2:-2]
		return urlparse(url).netloc
	return None

#Apply url mask to every cell in paths
f = np.vectorize(get_url)
urls = f(df)
print urls
urls_flat = urls.flatten()
us = urls_flat.tolist()
#list of all unique urls
us = list(set(us))
size = len(us)

results = pd.DataFrame(index=us, columns=us)
results= results.fillna(0) 
print size

count=0
#for each path...
for r in range(height):
	print r
	#two pointers to count every pair in path
	for c1 in range(length-1):
		for c2 in range(c1, length):
			a = urls[r, c1]
			b = urls[r, c2]
			#ignore 'None' and empty cells
			if not ((a=='None' or b=='None') or (a=='' or b=='')):
				count = count+1
				results.loc[a, b] = results.loc[a, b] + 1
print count



results.to_csv('domain_path_count_2.csv', sep=',', index=us, columns=us)


