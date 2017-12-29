#Filters articles out of spreadsheet by:
#remove all urls from yahoo
#remove any url where another url exists where:
	#text 9s >.8 similar
	#they are from the same site
#Outputs a list of 'replacers' and 'replacees'
import pandas as pd
import numpy as np 
from urlparse import urlparse
import math

df = pd.read_csv('article_similarity_results_01.csv', delimiter=',', index_col=0)
df2 = pd.read_csv('master_articles_11_16 - new_articles.csv(1).csv', delimiter=',', index_col=0)

urls = list(df2.index)
drops = {}
blacklist = []
for url in urls:
	if "yahoo" in url:
		drops[url] = url
	else:
		location = df2.loc[url, "updated_domain"]
		if(not isinstance(location, basestring)):
			#get 'location' portion of url
			location = urlparse(url).netloc
		for url2 in urls:
			#Check if you're looking at the column header
			if url2 != "Article URL" and url != "Article URL" and url not in blacklist:
				#The matix is only half-filled, one entry will be 0
				if (location in url2) and (df.loc[url, url2] + df.loc[url2, url]) > .8:
					drops[url2] = url
					blacklist.append(url2)

drop_list = drops.keys()
print(drop_list)
for drop in drop_list:
	if(drop in df.index):
		df = df.drop(drop, axis=0)
		df = df.drop(drop, axis=1)

#Now we have a list we can use
df2 = pd.DataFrame(drops.items(), columns=["Replaced", "Replacer"])

df2.to_csv('filtered_url_list.csv', sep=',')
df.to_csv('article_similarity_filtered.csv', index=True, header=True, sep=',')