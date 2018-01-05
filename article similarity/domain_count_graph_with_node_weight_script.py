#Take author count and create graph of references
#Directed graph

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import lxml
import gexf
import string
import networkx as nx
import math

import sys

sys.path.append('../gexf')
from gexf import Gexf, GexfImport


df = pd.read_csv('domain_path_count_65.csv', delimiter=',', index_col=0)
articles = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', index_col=0)

rows = list(df.index)
cols = list(df.columns.values)
num = len(rows)
urls = list(articles.index)


G=nx.Graph()

unreadable_names = {}
#add nodes
for r in rows:
	#print(r)
	matches = [x for x in urls if (r in x)]
	freq = 0
	for m in matches:
		c = articles.loc[m, "est_freq"]
		if math.isnan(c):
			c = 0
		freq = freq + c
	print int(freq)
	G.add_node(r, freq=int(freq))

#add edges
count = 0
count_r = 0
for r in rows:
	print("r" + str(count_r))
	for c in cols:
		if(not r==c):
			tot = df.loc[r, c] + df.loc[c, r]
			if(tot > 0):
				#each edge needs a unique 'name' - here it's just a count
				G.add_edge(r, c, weight=tot)
				count = count + 1
	count_r = count_r + 1

nx.write_gexf(G, "domain_count_graph_65.gexf")


