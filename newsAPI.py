import requests
import pandas as pd

# NEWSAPIを呼び出す
headers = {'X-Api-Key': 'd95ef705b35546239ca5ab40398a99b7'}
url = 'https://newsapi.org/v2/everything'
params = {
    'sortedBy': 'publishedAt',
    'q': '医療'
}
response = requests.get(url, headers=headers, params=params)


# データを取得してDataFrameに変換
data = response.json()
df = pd.DataFrame(data['articles'])
print(df.head())

# データをエクセルファイルに保存
df.to_excel('data.xlsx')

