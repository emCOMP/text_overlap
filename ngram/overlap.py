import pandas as pd
import nltk
from nltk.util import ngrams
import numpy as np
import datetime

def get_ngram_tuples(i, j, n, counts, text):
	url_a = list(counts.columns.values)[i]
	url_b = list(counts.columns.values)[j]
	try:
		text_a = text.loc[url_a, "Text"]
		text_b = text.loc[url_b, "Text"]
	except KeyError:
		return None;
	ngrams_a = list(ngrams(text_a.split(), n))
	ngrams_b = list(ngrams(text_b.split(), n))
	a = set(tuple(i) for i in ngrams_a)
	b = set(tuple(i) for i in ngrams_b)
	common_ngrams = a.intersection(b)
	overlaps = []
	for ngram in common_ngrams:
		index_a = ngrams_a.index(tuple(ngram))
		index_b = ngrams_b.index(tuple(ngram))
		overlaps.append((index_a, index_b, n))
	return overlaps


counts_200 = pd.read_csv('ngram_category_count_200.csv', delimiter=',', header=0, index_col=0)
counts_150 = pd.read_csv('ngram_category_count_150.csv', delimiter=',', header=0, index_col=0)
counts_100 = pd.read_csv('ngram_category_count_100.csv', delimiter=',', header=0, index_col=0)
counts_50 = pd.read_csv('ngram_category_count_50.csv', delimiter=',', header=0, index_col=0)
df = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', encoding='latin1', index_col=0)
num = len(counts_200)
results_matrix = np.empty((num, num), dtype=object)

for i in range(0, num):
	for j in range(i+1, num):
		is_overlap = False
		overlaps_200 = None
		overlaps_150 = None
		overlaps_100 = None
		overlaps_50 = None
		if counts_200.iloc[i][j] > 0:
			overlaps_200 = get_ngram_tuples(i, j, 200, counts_200, df)
			is_overlap = (overlaps_200 is not None)
		if counts_150.iloc[i][j] > 0:
			overlaps_150 = get_ngram_tuples(i, j, 150, counts_150, df)
			is_overlap = (overlaps_150 is not None)
		if counts_100.iloc[i][j] > 0:
			overlaps_100 = get_ngram_tuples(i, j, 100, counts_100, df)
			is_overlap = (overlaps_100 is not None)
		'''if counts_50.iloc[i][j] > 0:
			overlaps_50 = get_ngram_tuples(i, j, 50, counts_50, texts)
			is_overlap = True '''
		if is_overlap:
			print(str(i) +  ", " + str(j))
			overlap = []
			if overlaps_200 is not None:
				for n in overlaps_200:
					a = (n[0], n[0]+n[2])
					b = (n[1], n[1]+n[2])
					overlapped = False
					for n2 in overlap:
						a_2 = (n2[0], n2[0]+n2[2])
						b_2 = (n2[1], n2[0]+n2[2])
						if not (((a[0] < a_2[0] and a[1] < a_2[0]) or (a[0] > a_2[1] and a[1] > a_2[1]))
							and ((b[0] < b_2[0] and b[1] < b_2[0]) or (b[0] > b_2[1] and b[1] > b_2[1]))):
							overlapped = True
					if not overlapped:
						overlap.append(n)
			if overlaps_150 is not None:
				for n in overlaps_150:
					a = (n[0], n[0]+n[2])
					b = (n[1], n[1]+n[2])
					overlapped = False
					for n2 in overlap:
						a_2 = (n2[0], n2[0]+n2[2])
						b_2 = (n2[1], n2[0]+n2[2])
						if not (((a[0] < a_2[0] and a[1] < a_2[0]) or (a[0] > a_2[1] and a[1] > a_2[1]))
							and ((b[0] < b_2[0] and b[1] < b_2[0]) or (b[0] > b_2[1] and b[1] > b_2[1]))):
							overlapped = True
					if not overlapped:
						overlap.append(n)
			if overlaps_100 is not None:
				for n in overlaps_100:
					a = (n[0], n[0]+n[2])
					b = (n[1], n[1]+n[2])
					overlapped = False
					for n2 in overlap:
						a_2 = (n2[0], n2[0]+n2[2])
						b_2 = (n2[1], n2[0]+n2[2])
						if not (((a[0] < a_2[0] and a[1] < a_2[0]) or (a[0] > a_2[1] and a[1] > a_2[1]))
							and ((b[0] < b_2[0] and b[1] < b_2[0]) or (b[0] > b_2[1] and b[1] > b_2[1]))):
							overlapped = True
					if not overlapped:
						overlap.append(n)
			counts = [0, 0, 0, 0]
			print overlap
			exit(1)
			for n in overlap:
				counts[(n[2]/50)-1] += 1
			results_matrix[i][j] = counts
df = pd.DataFrame(results_matrix, index=list(counts_200.columns.values), columns=list(counts_200.columns.values))
df.to_csv('ngram_overlap_count.csv', index=True, header=True, sep=',')


						



						