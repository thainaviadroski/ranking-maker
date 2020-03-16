# Imports librarys

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# Capturar a url 

url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"


option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(10)


driver.find_element_by_xpath( f"//div[@class='nba-stat-table__overflow']//table//thead//tr//th[@data-field='PTS']").click()
element = driver.find_element_by_xpath("//div[@class='nba-stat-table__overflow']//table")
html_content = element.get_attribute('outerHTML')


# Teste da captura do html da pagina.
# print(html_content)

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


df_full= pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos','player','team','total']

# Teste da formatação e limpeza dos dados capturados. 
# print(df)


top10ranking = {}
top10ranking['point'] = df.to_dict('records')

# Teste da formatação dos dados
# print(top10ranking)


driver.quit()

js= json.dumps(top10ranking)
fp = open('ranking.json','w')
fp.write(js)
fp.close()