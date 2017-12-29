#Take similarity matrix and create a gexf graph
#Undirected graph

import pandas as pd
import numpy as np
import lxml
import datetime
import gexf
from urlparse import urlparse

import sys

sys.path.append('../gexf')
from gexf import Gexf, GexfImport


df = pd.read_csv('article_similarity_filtered.csv', delimiter=',', index_col=0)
dates = pd.read_csv('master_articles-scraped_filtered_aritcles.csv', delimiter=',')

rows = list(df.index)
rows.remove('Article URL')
cols = list(df.columns.values)
num = len(rows)
cols.remove('Article URL.1')


gexf = Gexf("emCOMP","Article Similarity")
graph=gexf.addGraph("undirected","static","Article Similarity")

#add nodes
for r in rows:
	graph.addNode(r, dates.loc[r, "updated_domain"])

#add edges
count = 0
count_r = 0
for r in rows:
	print("r" + str(count_r))
	for c in cols:
		#can be adapted for directed graph
		if(df.loc[r, c] > .85):
			r_date = datetime.datetime.strptime(str(dates.loc[r, "first_ts"]), '%Y-%m-%d %H:%M:%S')
			c_date = datetime.datetime.strptime(str(dates.loc[c, "first_ts"]), '%Y-%m-%d %H:%M:%S')
			if(r < c):
				graph.addEdge(count, r, c, df.loc[r, c])
			else:
				graph.addEdge(count, c, r, df.loc[r, c])
			count = count + 1
	count_r = count_r + 1

output_file=open("edge_matrix.gexf","w")
gexf.write(output_file)


