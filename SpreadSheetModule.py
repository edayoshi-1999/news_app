import gspread
import pandas as pd

# 認証情報を使ってスプレッドシートにアクセスするためのクライアントを作る
class SpreadSheet:
    def writeSpreadSheet(self, data):

        gc = gspread.service_account(
            filename=r"C:\Users\utaka\OneDrive\デスクトップ\programing\application\spread-sheet-test.json"
        )

        # スプレッドシートの作成
        sh = gc.create(
            "test_1",
            folder_id="1whd_faQzwajdZnuClNrNr6QUhzkd18K-"
        )

        # シートの作成
        ws = sh.worksheet("Sheet1")
        ws.clear()

        # 予備データ
        # data = {
        #     "name": ["aaa", "bbb"],
        #     "age": [10, 20]
        # }

        df = pd.DataFrame(data)

        # データフレームのスプレッドシートへの書き込み
        ws.update(
            [df.columns.values.tolist()] + df.values.tolist()
        )