import requests
import pandas as pd
import SpreadSheetModule
from trasnlateByDeepl import transtate_text

def extract_source_name(source):
    """
    sourceが辞書の場合、'name' キーの値を返す。
    それ以外の場合は空文字を返す。
    """
    if isinstance(source, dict) and 'name' in source:
        return source['name']
    return ""

# NEWSAPIを呼び出す
headers = {'X-Api-Key': 'd95ef705b35546239ca5ab40398a99b7'}
url = 'https://newsapi.org/v2/everything'
params = {
    'sortedBy': 'publishedAt',
    'q': 'medical'
}
response = requests.get(url, headers=headers, params=params)

# データを取得
data = response.json()

# 以下、データをDataFrame化して、整形 
# APIの仕組みから、整形をしないとエラーになる（null、辞書型×）
df = pd.DataFrame(data['articles'])
# Noneを空文字化
df.fillna("")
#sourceカラムの辞書からnameを取り出し、文字列へ。
df['source'] = df['source'].apply(extract_source_name)

# titleのみ翻訳
# リスト化
title_list = df['title'].tolist()
# 翻訳
translated_title = transtate_text(title_list)
# データフレームに格納
df['title'] = pd.DataFrame(translated_title)

# 特定の列のみを抽出
df = df.loc[:, ['title', 'source', 'author', 'publishedAt', 'url']]

# スプレッドシートモジュールを呼び出して、引数のデータを書きこむ
sh = SpreadSheetModule.SpreadSheet()
sh.writeSpreadSheet(df, 'medical_news_English')








# エクセルファイルに保存するときの処理は、以下。
# # データを取得してDataFrameに変換
# data = response.json()
# df = pd.DataFrame(data['articles'])
# print(df.head())

# # データをエクセルファイルに保存
# df.to_excel('data.xlsx')

