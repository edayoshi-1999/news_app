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
    try:
        response = requests.get(url, timeout=10)  # タイムアウトを設定
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[エラー] HTMLの取得に失敗しました: {e}")
        return None  # 後続処理で None チェックできるようにする

# 記事情報を抽出する関数
def parse_article_info(html):
    if html is None:
        print("[警告] HTMLが空です。記事情報の解析をスキップします。")
        return []

    try:
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.find_all('p', class_='article-list-article-title')
        dates = soup.find_all('p', class_='article-list-date')
        tags = soup.find_all('a', class_='article-list-tag')
        divs = soup.find_all('div', class_='detail-inner')

        urls = [div.find('a', recursive=False) for div in divs]

        articles = []
        for title, date, tag, url in zip(titles, dates, tags, urls):
            article = [
                title.text.strip(),
                date.text.strip(),
                tag.text.strip(),
                BASE_URL + url.attrs["href"]
            ]
            articles.append(article)

        return articles

    except Exception as e:
        print(f"[エラー] HTMLの解析中に問題が発生しました: {e}")
        return []

# スプレッドシートへ保存する関数
def save_to_spreadsheet(data, sheet_name='日経メディカル'):
    if not data:
        print("[情報] 保存するデータがありません。スプレッドシートへの書き込みをスキップします。")
        return

    try:
        df = pd.DataFrame(data, columns=['title', 'date', 'tag', 'url'])
        spreadsheet = SpreadSheetModule.SpreadSheet()
        spreadsheet.writeSpreadSheet(df, sheet_name)
        print(f"[成功] スプレッドシート『{sheet_name}』に保存しました。")
    except Exception as e:
        print(f"[エラー] スプレッドシートへの書き込みに失敗しました: {e}")


# メイン処理
def main():
    try:
        html = fetch_html(URL)   # HTML取得
        article_data = parse_article_info(html) # 記事情報を抽出
        save_to_spreadsheet(article_data)  # スプレッドシートへ保存
    except Exception as e:
        print(f"[エラー] メイン処理中に問題が発生しました: {e}")


# スクリプトが直接実行されたときだけmainを呼び出す
if __name__ == '__main__':
    main()


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