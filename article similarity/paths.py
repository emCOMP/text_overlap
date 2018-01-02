#Creates a graph of articles with similarity >.85
#Finds connected components - these are all one article being shared around
#Sorts the nodes in each connected component by date (earliest first)
#Ouputs these urls, with the most-copied articles first

#Ouput style:
	#Each row is a component (1 article that is copied)
	#Each cell is a different iteration of that article
	#Iterations are ordered by date, earliest to the left
	#Only articles that have at least 2 iterations are shown

import pandas as pd
import numpy as np
import datetime
import networkx as nx
import math
import csv

import sys

sys.path.append('../gexf')
from gexf import Gexf, GexfImport


df = pd.read_csv('article_similarity_filtered.csv', delimiter=',', index_col=0)
dates = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', index_col=0)

rows = list(df.index)
rows.remove('Article URL')
r2 = list(dates.index)
num = len(rows)

urls = list()

G = nx.DiGraph()
#Add nodes
for r in rows:
	if(r in r2 and not (str(dates.loc[r, "first_ts"])) == 'nan'):
		r_date = str(dates.loc[r, "first_ts"])
		G.add_node(r, date=r_date)
		urls.append(r)
urls2 = urls[:]
#Add edges
for r in urls:
	for c in urls2:
		if(df.loc[r, c] > .85):
			r_date = datetime.datetime.strptime(str(dates.loc[r, "first_ts"]), '%Y-%m-%d %H:%M:%S')
			c_date = datetime.datetime.strptime(str(dates.loc[c, "first_ts"]), '%Y-%m-%d %H:%M:%S')
			if(r_date < c_date):
				G.add_edge(r, c, similarity=df.loc[r, c])
			else:
				G.add_edge(c, r, similarity=df.loc[r, c])

with open("paths.csv", 'w') as f: 
	writer = csv.writer(f)
	#get components and sort
	for comp in sorted(nx.weakly_connected_components(G)):
		#write all copied articles to a csv
		if not len(comp) <= 1:
			print(comp)
			s = list()
			#sort as a list of tuples
			for node in comp:
				s.append((node, datetime.datetime.strptime(str(dates.loc[node, "first_ts"]), '%Y-%m-%d %H:%M:%S')))
			s = sorted(s, key=lambda x: x[1])
			writer.writerow(s)


