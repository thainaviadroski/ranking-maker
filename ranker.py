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
top10ranking ={}

ranking={
  '3points':{'field': 'FG3M','label':'3PM'},
  'points':{'field': 'PTS','label':'PTS'},
  'assistants':{'field': 'AST','label':'AST'},
  'rebounds':{'field': 'REB','label':'REB'},
  'steals':{'field': 'STL','label':'STL'},
  'blocks':{'field': 'BLK','label':'3PM'},
}

def buildRank(type):
    field = ranking[type]['field']
    label = ranking[type]['label']

    driver.find_element_by_xpath( f"//div[@class='nba-stat-table__overflow']//table//thead//tr//th[@data-field='{field}']").click()
  
    element = driver.find_element_by_xpath("//div[@class='nba-stat-table__overflow']//table")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full= pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
    df.columns = ['pos','player','team','total']

    return df.to_dict('records')


option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(10)

for k in ranking:
    top10ranking[k] = buildRank(k)




driver.quit()

with open('ranking2.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)