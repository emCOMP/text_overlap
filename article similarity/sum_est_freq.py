import numpy as np
import pandas as pd
import math

df = pd.read_csv('scraped_filtered_aritcles.csv', delimiter=',', index_col=0)

urls = list(df.index)

s = 0
for u in urls:
	c = df.loc[u, "est_freq"]
	if math.isnan(c):
		c = 0
	s = s + c
print s