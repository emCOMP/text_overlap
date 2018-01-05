#Take author count and create graph of references
#Directed graph

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import lxml
import gexf
import string

import sys

sys.path.append('../gexf')
from gexf import Gexf, GexfImport


df = pd.read_csv('domain_path_count.csv', delimiter=',', index_col=0)

rows = list(df.index)
cols = list(df.columns.values)
num = len(rows)


gexf = Gexf("emCOMP","Authors")
G=gexf.addGraph("undirected","static","Domain Counts")

unreadable_names = {}
#add nodes
for r in rows:
	print(r)
	G.addNode(r, r)

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
				G.addEdge(count, r, c, tot)
				count = count + 1
	count_r = count_r + 1

output_file=open("domain_count_graph.gexf","w")
gexf.write(output_file)


