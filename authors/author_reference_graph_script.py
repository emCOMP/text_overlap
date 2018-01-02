#NOTE: THIS IS NOT A WORKING SCRIPT - I GAVE UP DEBUGGING IT
# PLEASE SEE author_reference_graph_script_2.py

#Take author count and create graph of references
#Directed graph

# coding: utf-8

import pandas as pd
import numpy as np
import lxml
import networkx as nx
import matplotlib.pyplot as plt

import sys


df = pd.read_csv('authors_counts.csv', delimiter=',', index_col=0)

rows = list(df.index)
cols = list(df.columns.values)
num = len(rows)


G = nx.DiGraph()
#add nodes
for r in rows:
	G.add_node(r)
nx.draw(G)
#add edges
count = 0
count_r = 0
for r in rows:
	print("r" + str(count_r))
	for c in cols:
		#can be adapted for directed graph
		if(not r==c):
			G.add_edge(r, c, weight=df.loc[r, c])
			count = count + 1
	count_r = count_r + 1

nx.draw(G)
plt.draw()

#nx.write_gexf(G, "author_reference_graph.gexf")


