import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.html import read_html
from selenium import webdriver




#initialize requests and beatifulsoup
url = "https://login.easyhosting.nl/manage_dns/cbd7c2c1-11e8-4057-a824-20ea39f62d22"



driver = webdriver.Chrome()
driver.get(url)

x_path = "/html/body/div[1]/main/div/div/div[2]/div[2]/div[3]/div/div/div/div/table"
table = driver.find_element_by_xpath(x_path)
table_html = table.get_attribute('innerHTML')

df = read_html(table_html)[0]
print ('hoi',df)

driver.close()


""" 
response = requests.get(url=url,)
soup = BeautifulSoup(response.text, 'html.parser')




driver = webdriver.Firefox()
driver.get('http://www1.nyse.com/about/listed/IPO_Index.html')

table = driver.find_element_by_xpath('//div[@class="sp5"]/table//table/..')
table_html = table.get_attribute('innerHTML')

df = read_html(table_html)[0]
print (df)

driver.close()

#print (df)
#//*[@id="name_0"]
#/html/body/div[1]/main/div/div/div[2]/div[2]/div[3]/div/div/div/div/table/tbody/tr[1]/td[1]/div/div/input

#/html/body/div[1]/main/div/div/div[2]/div[2]/div[3]/div/div/div/div/table/tbody/tr[3]/td[1]/div/div/input
#/html/body/div[1]/main/div/div/div[2]/div[2]/div[3]/div/div/div/div/table/tbody/tr[3]/td[2]/div/div/select


#find title and heading
#title = soup.find(id="firstHeading")

#use beautifulsoup to parse table and pass it into pandas module
#brick_table = soup.find_all("table",{"class":"table.w-full"})


#df = pd.read_html(str(brick_table))
#df = pd.concat(df)




#r = requests.get(url)
#df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
#df = df_list[0]
#df.head()

#print (df.head())

"""