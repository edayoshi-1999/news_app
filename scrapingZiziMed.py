# 時事メディカルをwebスクレイピングして、それを保存する処理を書く。
import requests
from bs4 import BeautifulSoup
import pandas as pd
import spreadSheetModule


URL = 'https://medical.jiji.com/news/?c=medical'
BASE_URL = 'https://medical.jiji.com'

def fetch_html(url):
    """指定したURLからHTMLを取得する"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPエラーがあれば例外に
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[エラー] HTML取得に失敗しました: {e}")
        return None


def parse_articles(html):
    """HTMLから記事情報（タイトル・日付・URL）を抽出する"""
    if html is None:
        print("[警告] HTMLが空なので、記事の解析をスキップします。")
        return []

    try:
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.find_all('p', class_='articleTextList__title')
        dates = soup.find_all('span', class_='articleTextList__date')
        lis = soup.find_all('li', class_='articleTextList__item')
        
        # liタグの1個下の子要素であるaタグを取得し、リストにする。
        urls = []
        for li in lis:
            urls.append(li.find('a', recursive=False))

        # 取得したデータをリストに格納
        articles = []
        for title, date, url_tag in zip(titles, dates, urls):
            article = [
                title.text,
                date.text,
                BASE_URL + url_tag['href']
            ]
            articles.append(article)
        return articles

    except Exception as e:
        print(f"[エラー] 記事情報の解析に失敗しました: {e}")
        return []
    

def save_to_spreadsheet(data, sheet_name='時事メディカル'):
    """記事データをスプレッドシートに保存する"""
    if not data:
        print("[情報] 保存するデータがありません。スプレッドシートへの書き込みをスキップします。")
        return

    try:
        df = pd.DataFrame(data, columns=['title', 'date', 'url'])
        spreadsheet = spreadSheetModule.SpreadSheet()
        spreadsheet.writeSpreadSheet(df, sheet_name)
        print(f"[成功] スプレッドシート『{sheet_name}』に保存しました。")
    except Exception as e:
        print(f"[エラー] スプレッドシートへの書き込みに失敗しました: {e}")


def main():
    """メイン処理：スクレイピング → 整形 → 保存"""
    try:
        html = fetch_html(URL)
        articles = parse_articles(html)
        save_to_spreadsheet(articles)
    except Exception as e:
        print(f"[エラー] メイン処理中に問題が発生しました: {e}")

if __name__ == '__main__':
    main()


# ---------------------------------------
# 以下、リファクタリング前のコード
# # 時事メディカルへアクセス
# url = 'https://medical.jiji.com/news/?c=medical'
# r = requests.get(url)
# r.raise_for_status()

# # 目的のタグを取得
# soup = BeautifulSoup(r.text, 'html.parser')

# titles = soup.find_all('p', class_='articleTextList__title')
# dates = soup.find_all('span', class_='articleTextList__date')
# lis = soup.find_all('li', class_='articleTextList__item')

# # liタグの1個下の子要素であるaタグを取得し、リストにする。
# urls = []
# for li in lis:
#     urls.append(li.find('a', recursive=False))

# # 取得したデータをリストに格納し、DataFrameに変換
# values = []
# for title, date, url in zip(titles, dates, urls):
#     values.append([title.text, date.text, 'https://medical.jiji.com/' + url.attrs["href"]])
# df = pd.DataFrame(values, columns=['title', 'date', 'url'])

# # スプレッドシートへの書き込み
# sh = SpreadSheetModule.SpreadSheet()
# sh.writeSpreadSheet(df, '時事メディカル')

