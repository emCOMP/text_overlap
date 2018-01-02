#Some analysis of dates for iterations of an article
#For each article, find the time span (in seconds) between:
	#First iteration and second iteration
	#First iteration and last iteration

import pandas as pd
import numpy as np
import datetime
import math
import csv

df = pd.read_csv('paths.csv', delimiter=',')


shape = df.shape
length = shape[1]
height = shape[0]
dates = np.empty(shape)
dates[:, :] = 0

#Getting the date from the paths.csv format (which is a bit weird)
def get_date(entry):
	if(isinstance(entry, basestring)):
		e = entry.split("datetime.")
		date = e[1]
		date = date[:-1]
		return date
	return None

f = np.vectorize(get_date)
dates = f(df)

#a table of just dates, to make things easier
dates_write = pd.DataFrame(dates)
dates_write.to_csv('paths_dates.csv', sep=',')

#Our results
avg_diff_first = list()
avg_diff_last = list()

for r in range(height):
	#evaluate our dates so we can compare them
	d1 = eval('datetime.' + dates[r, 0])
	d2 = eval('datetime.' + dates[r, 1])
	diff = d2-d1
	avg_diff_first.append(diff.total_seconds())
	if(diff.total_seconds()< 100):
		#This suggests something funky is going on, I suspect our data needs more cleaning
		print dates[r,0]

	prev = dates[r, 0]
	count = 1
	#Get the last iteration (either 37 or last before None since they're sorted)
	while(count < 37 and not dates[r, count] == 'None'):
		prev = dates[r, count]
		count +=1
	dl = eval('datetime.' + prev)
	avg_diff_last.append((dl-d1).total_seconds())

diff_array = np.asarray((avg_diff_first, avg_diff_last))
diff_write = pd.DataFrame(diff_array)
#diff_write.to_csv('paths_dates_diffs.csv', sep=',')


