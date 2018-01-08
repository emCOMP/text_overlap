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


df = pd.read_csv('domain_path_count_2.csv', delimiter=',', index_col=0)
counts = pd.read_csv('total_domain_counts_White_Helmets_unshortened-2.txt', delimiter='\t', index_col=0, header=None)

rows = list(df.index)
cols = list(df.columns.values)
num = len(rows)
urls = list(counts.index)


G=nx.Graph()

unreadable_names = {}
#add nodes
for r in rows:
	freq = 0
	if r.startswith("www."):
		r = r[4:]
	if not r in urls:
		print r
	else:
		if "russia" in r:
			print "r " + r
			print counts.loc[r, :].values[0]
		c = counts.loc[r, :].values[0]
	G.add_node(r, freq=int(c))

#add edges
count = 0
count_r = 0
for r in rows:
	print("r" + str(count_r))
	for c in cols:
		if(not r==c):
			tot = df.loc[r, c] - df.loc[c, r]
			if not (df.loc[r, c] == 0  and df.loc[c, r]==0):
				#each edge needs a unique 'name' - here it's just a count
				G.add_edge(r, c, weight=tot)
				count = count + 1
	count_r = count_r + 1

nx.write_gexf(G, "domain_count_graph_2.gexf")


