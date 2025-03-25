# 日経メディカルをwebスクレイピングして、それを保存する処理を書く。
import requests
from bs4 import BeautifulSoup
import pandas as pd
import SpreadSheetModule

# 定数：スクレイピング対象URL
URL = 'https://medical.nikkeibp.co.jp/inc/all/article/'
BASE_URL = 'https://medical.nikkeibp.co.jp'

# HTMLを取得する関数
def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()  # HTTPエラーがあれば例外を投げる
    return response.text

# 記事情報を抽出する関数
def parse_article_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # 各要素のリストを取得
    titles = soup.find_all('p', class_='article-list-article-title')
    dates = soup.find_all('p', class_='article-list-date')
    tags = soup.find_all('a', class_='article-list-tag')
    divs = soup.find_all('div', class_='detail-inner')

    # URL情報はaタグから直接取得（divの子要素）
    urls = []
    for div in divs:
        urls.append(div.find('a', recursive=False))

    # データをまとめてリストに格納
    articles = []
    for title, date, tag, url in zip(titles, dates, tags, urls):
        article = [
            title.text,  # タイトル
            date.text,   # 日付
            tag.text,    # タグ（カテゴリなど）
            BASE_URL + url.attrs["href"]  # フルURL
        ]
        articles.append(article)

    return articles

# スプレッドシートへ保存する関数
def save_to_spreadsheet(data, sheet_name='日経メディカル'):
    df = pd.DataFrame(data, columns=['title', 'date', 'tag', 'url'])
    spreadsheet = SpreadSheetModule.SpreadSheet()
    spreadsheet.writeSpreadSheet(df, sheet_name)

# メイン処理
if __name__ == '__main__':
    html = fetch_html(URL)
    article_data = parse_article_info(html)
    save_to_spreadsheet(article_data)



# ーーーーーーーーーーーーーーーーーーーーーーーーーー
# 以下、リファクタリング前のコード
# # 日経メディカルへアクセス
# url = 'https://medical.nikkeibp.co.jp/inc/all/article/'
# r = requests.get(url)
# r.raise_for_status()

# # 目的のタグを取得
# soup = BeautifulSoup(r.text, 'html.parser')

# titles = soup.find_all('p', class_='article-list-article-title')
# dates = soup.find_all('p', class_='article-list-date')
# tags = soup.find_all('a', class_='article-list-tag')
# divs = soup.find_all('div', class_='detail-inner')

# # divタグの1個下の子要素であるaタグを取得し、リストにする。
# urls = []
# for div in divs:
#     urls.append(div.find('a', recursive=False))

# # 取得したデータをリストに格納
# values = []

# for title, date, tag, url in zip(titles, dates, tags, urls):
#     values.append([title.text, date.text, tag.text, 'https://medical.nikkeibp.co.jp' + url.attrs["href"]])

# df = pd.DataFrame(values, columns=['title', 'date', 'tag', 'url'])

# # スプレッドシートへの書き込み
# sh = SpreadSheetModule.SpreadSheet()
# sh.writeSpreadSheet(df, '日経メディカル')