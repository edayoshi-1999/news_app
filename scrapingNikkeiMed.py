# 日経メディカルをwebスクレイピングして、それを保存する処理を書く。
import requests
from bs4 import BeautifulSoup
import pandas as pd
import SpreadSheetModule

# 日経メディカルへアクセス
url = 'https://medical.nikkeibp.co.jp/inc/all/article/'
r = requests.get(url)
r.raise_for_status()

# 目的のタグを取得
soup = BeautifulSoup(r.text, 'html.parser')

titles = soup.find_all('p', class_='article-list-article-title')
dates = soup.find_all('p', class_='article-list-date')
tags = soup.find_all('a', class_='article-list-tag')
divs = soup.find_all('div', class_='detail-inner')

# divタグの1個下の子要素であるaタグを取得し、リストにする。
urls = []
for div in divs:
    urls.append(div.find('a', recursive=False))

# 取得したデータをリストに格納
values = []

for title, date, tag, url in zip(titles, dates, tags, urls):
    values.append([title.text, date.text, tag.text, 'https://medical.nikkeibp.co.jp' + url.attrs["href"]])

df = pd.DataFrame(values, columns=['title', 'date', 'tag', 'url'])

# スプレッドシートへの書き込み
sh = SpreadSheetModule.SpreadSheet()
sh.writeSpreadSheet(df, '日経メディカル')