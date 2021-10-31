
import requests
from bs4 import BeautifulSoup
import pandas as pd

#initialize requests and beatifulsoup
wiki_url = "https://nl.wikipedia.org/wiki/Lijst_van_baksteenformaten"
response = requests.get(url=wiki_url,)
soup = BeautifulSoup(response.text, 'html.parser')

#find title and heading
title = soup.find(id="firstHeading")


#use beautifulsoup to parse table and pass it into pandas module
brick_tables = soup.find_all("table",{"class":"wikitable sortable"})
dataframe_list = []
for brick_table in brick_tables:

	#print (brick_table)
	dataframe = pd.read_html(str(brick_table))
	dataframe_list.append(pd.read_html(str(brick_table)))
	#break



pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows',100)
pd.set_option('display.min_rows',100)
pd.set_option('display.width', 120)
pd.set_option('expand_frame_repr',True)




for data_frame in dataframe_list:
	print (data_frame)
