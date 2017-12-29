#Take in list of replacer and replacee
#Update article spreadsheet
#Update dates and frequencies

import pandas as pd
import numpy as np 
import datetime
import xlrd

df = pd.read_csv('master_articles_11_16 - new_articles.csv(1).csv', sep=',', index_col=0)
df_filtered = pd.read_csv('filtered_url_list.csv', sep=',')

freq = df.loc[:, "est_freq"]
ftimes = df.loc[:, "first_ts"]
ltimes = df.loc[:, "last_ts"]
urls = list(df.index)
replaced_list = df_filtered.loc[:, "Replaced"]
replacer_list = df_filtered.loc[:, "Replacer"]

num = len(replaced_list)

for i in range(0, num):
	#get frequencies and add them, then replace the "replacer" freqeuncy with the sum
	replaced = replaced_list[i]
	replacer = replacer_list[i]
	replaced_ind = urls.index(replaced)
	replacer_ind = urls.index(replacer)
	replaced_freq = freq[replaced_ind]
	replacer_freq = freq[replacer_ind]
	df.at[replacer, "est_freq"] = replaced_freq + replacer_freq
	try:
		#Get times, put the earliest as the replacer time for first_ts and latest for last_ts
		freplaced_time = datetime.datetime.strptime(str(ftimes[replaced_ind]), '%Y-%m-%d %H:%M:%S')
		freplacer_time = datetime.datetime.strptime(str(ftimes[replacer_ind]), '%Y-%m-%d %H:%M:%S')
		lreplaced_time = datetime.datetime.strptime(str(ltimes[replaced_ind]), '%Y-%m-%d %H:%M:%S')
		lreplacer_time = datetime.datetime.strptime(str(ltimes[replacer_ind]), '%Y-%m-%d %H:%M:%S')
		df.at[replacer, "first_ts"] = min(freplacer_time, freplaced_time)
		df.at[replacer, "last_ts"] = max(lreplacer_time, lreplaced_time)
	except ValueError:
		#If there's a problem (e.g. malformed date) print so we can see it
		print(replacer)
		print(replaced)
		print(df.loc[replacer, "first_ts"])
		print(df.loc[replacer, "last_ts"])
		print()
	#drop the replaced row
	df = df.drop(replaced, axis=0)

df.to_csv('scraped_filtered_aritcles.csv', index=True, header=True, sep=',')
	
