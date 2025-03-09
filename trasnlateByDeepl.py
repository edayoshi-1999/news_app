import deepl
import os
import pandas as pd

# リスト型のデータを翻訳して、そのリストを返す。
def transtate_text(data):
    #環境変数からAPIキーを取得
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)

    # dataを翻訳し、リストに格納
    results = translator.translate_text(data, target_lang="JA")
    values = []
    for result in results:
        values.append(result.text)
    
    return values


# # テスト
# testdata = {
#     "title": ["Hello1", "Hello2", "Hello3"]
# }
# df = pd.DataFrame(testdata)
# df_list = df['title'].tolist()
# print(df_list)
# result = transtate_text(df_list)
# print(result)