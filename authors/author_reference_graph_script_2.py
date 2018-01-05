#Take author count and create graph of references
#Directed graph

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import lxml
import gexf
import unicodedata
import string

import sys

sys.path.append('../gexf')
from gexf import Gexf, GexfImport

#gephx is xml, which does not support accents, so we need to remove them
def remove_accents(word):
    return ''.join(x for x in unicodedata.normalize('NFKD', word) if x in string.ascii_letters)

df = pd.read_csv('authors_counts.csv', delimiter=',', index_col=0)

rows = list(df.index)
cols = list(df.columns.values)
num = len(rows)


gexf = Gexf("emCOMP","Authors")
G=gexf.addGraph("directed","static","Authors")

unreadable_names = {}
#add nodes
for r in rows:
	#gephx needs unicode, make sure the string is unicode
	if isinstance(unicode(r, "utf-8"), str):
		print "ordinary string"
	elif isinstance(unicode(r, "utf-8"), unicode):
		print "unicode string"
	#Checking myself
	print(r)
	print(remove_accents(unicode(r, "utf-8")))
	new_string = remove_accents(unicode(r, "utf-8"))
	count = 0
	if(len(new_string) == 0 ):
		new_string = "unreadable string " + chr(97 + count)
		unreadable_names[r] = new_string
		count = count+1
	print(new_string)
	G.addNode(new_string, new_string)

#add edges
count = 0
count_r = 0
for r in rows:
	print("r" + str(count_r))
	for c in cols:
		if(not r==c):
			new_string_r = remove_accents(unicode(r, "utf-8"))
			new_string_c = remove_accents(unicode(c, "utf-8"))
			if(len(new_string_r) == 0 ):
				new_string_r = unreadable_names[r]
			if(len(new_string_c) == 0 ):
				new_string_c = unreadable_names[c]
			#each edge needs a unique 'name' - here it's just a count
			G.addEdge(count, new_string_r, new_string_c, df.loc[r, c])
			count = count + 1
	count_r = count_r + 1

output_file=open("author_reference_graph.gexf","w")
gexf.write(output_file)


