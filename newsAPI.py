import requests
import pandas as pd
import SpreadSheetModule
from trasnlateByDeepl import translate_text
import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# sourceフィールドから辞書内の'name'キーを取り出す関数
# nameキーがないか、sourceが辞書でない場合は空文字を返す
def extract_source_name(source):
    if isinstance(source, dict) and 'name' in source:
        return source['name']
    return ""


# ニュースAPIからデータを取得する関数
def fetch_news_data():
    headers = {'X-Api-Key': os.getenv("X_Api_Key")}
    url = 'https://newsapi.org/v2/everything'
    params = {
        'sortedBy': 'publishedAt',
        'q': 'medical'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data['articles']
    except requests.exceptions.RequestException as e:
        print(f"[エラー] ニュースデータの取得に失敗しました: {e}")
        return []
    except ValueError as e:
        print(f"[エラー] レスポンスデータの解析に失敗しました: {e}")
        return []


# APIで取得した記事データを整形する関数
def clean_and_format_data(articles):
    if not articles:
        print("[情報] 記事データが空です。整形処理をスキップします。")
        return pd.DataFrame()
    
    try:
        df = pd.DataFrame(articles)              # 記事リストをDataFrameに変換
        df = df.fillna("")                            # 欠損値を空文字に置換
        df['source'] = df['source'].apply(extract_source_name)  # sourceフィールドから名前だけ取り出す
        return df
    except Exception as e:
        print(f"[エラー] データ整形中に問題が発生しました: {e}")
        return pd.DataFrame()


# titleカラムだけを翻訳する関数
def translate_titles(df):
    if 'title' not in df.columns:
        print("[情報] タイトルカラムが存在しません。翻訳処理をスキップします。")
        return df
    
    try:
        title_list = df['title'].tolist()        # タイトルをリスト化
        translated_title = translate_text(title_list)  # タイトルを翻訳
        df['title'] = pd.DataFrame(translated_title)  # 翻訳後のタイトルをDataFrameに反映
        return df
    except Exception as e:
        print(f"[エラー] タイトル翻訳中に問題が発生しました: {e}")
        return df


# 整形したデータをスプレッドシートに書き込む関数
def save_to_spreadsheet(df):
    if df.empty:
        print("[情報] 書き込むデータがないため、スプレッドシートへの保存をスキップします。")
        return

    try:    
        df = df.loc[:, ['title', 'source', 'author', 'publishedAt', 'url']]  # 必要な列だけ抽出
        sh = SpreadSheetModule.SpreadSheet()
        sh.writeSpreadSheet(df, 'medical_news_English')
        print("[成功] スプレッドシート「medical_news_English」に保存しました。")
    except Exception as e:
        print(f"[エラー] スプレッドシートへの書き込みに失敗しました: {e}")


# 処理のメイン関数
def main():
    try:    
        articles = fetch_news_data()             # APIから記事を取得
        df = clean_and_format_data(articles)     # 整形
        df = translate_titles(df)                # タイトルのみ翻訳
        save_to_spreadsheet(df)                  # スプレッドシートに保存
    except Exception as e:
        print(f"[エラー] メイン処理中に問題が発生しました: {e}")

# スクリプトが直接実行されたときだけmainを呼び出す
if __name__ == "__main__":
    main()


# ーーーーーーーーーーーーーーー
# 以下、リファクタリング前のコード

# def extract_source_name(source):
#     # sourceが辞書の場合、'name' キーの値を返す。それ以外の場合は空文字を返す。
#     if isinstance(source, dict) and 'name' in source:
#         return source['name']
#     return ""


# # NEWSAPIを呼び出す
# headers = {'X-Api-Key': os.getenv("X_Api_Key")}
# url = 'https://newsapi.org/v2/everything'
# params = {
#     'sortedBy': 'publishedAt',
#     'q': 'medical'
# }
# response = requests.get(url, headers=headers, params=params)

# # データを取得
# data = response.json()

# # 以下、データをDataFrame化して、整形 
# # APIの仕組みから、整形をしないとエラーになる（null、辞書型×）
# df = pd.DataFrame(data['articles'])
# # Noneを空文字化
# df.fillna("")
# #sourceカラムの辞書からnameを取り出し、文字列へ。
# df['source'] = df['source'].apply(extract_source_name)

# # titleのみ翻訳
# # リスト化
# title_list = df['title'].tolist()
# # 翻訳
# translated_title = transtate_text(title_list)
# # データフレームに格納
# df['title'] = pd.DataFrame(translated_title)

# # 特定の列のみを抽出
# df = df.loc[:, ['title', 'source', 'author', 'publishedAt', 'url']]

# # スプレッドシートモジュールを呼び出して、引数のデータを書きこむ
# sh = SpreadSheetModule.SpreadSheet()
# sh.writeSpreadSheet(df, 'medical_news_English')

# エクセルファイルに保存するときの処理は、以下。
# # データを取得してDataFrameに変換
# data = response.json()
# df = pd.DataFrame(data['articles'])
# print(df.head())

# # データをエクセルファイルに保存
# df.to_excel('data.xlsx')

