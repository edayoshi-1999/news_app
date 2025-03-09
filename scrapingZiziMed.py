# 時事メディカルをwebスクレイピングして、それを保存する処理を書く。
import requests
from bs4 import BeautifulSoup
import pandas as pd
import SpreadSheetModule

# 時事メディカルへアクセス
url = 'https://medical.jiji.com/news/?c=medical'
r = requests.get(url)
r.raise_for_status()

# 目的のタグを取得
soup = BeautifulSoup(r.text, 'html.parser')

titles = soup.find_all('p', class_='articleTextList__title')
dates = soup.find_all('span', class_='articleTextList__date')
lis = soup.find_all('li', class_='articleTextList__item')

# liタグの1個下の子要素であるaタグを取得し、リストにする。
urls = []
for li in lis:
    urls.append(li.find('a', recursive=False))

# 取得したデータをリストに格納し、DataFrameに変換
values = []
for title, date, url in zip(titles, dates, urls):
    values.append([title.text, date.text, 'https://medical.jiji.com/' + url.attrs["href"]])
df = pd.DataFrame(values, columns=['title', 'date', 'url'])

# スプレッドシートへの書き込み
sh = SpreadSheetModule.SpreadSheet()
sh.writeSpreadSheet(df, '時事メディカル')

