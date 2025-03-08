import gspread
import pandas as pd



class SpreadSheet:

    # 引数のdataは、DataFrame型のデータを受け取る
    def writeSpreadSheet(self, data, sheet_name):

        # 認証情報を使ってスプレッドシートにアクセスするためのクライアントを作る
        gc = gspread.service_account(
            filename=r"C:\Users\utaka\OneDrive\デスクトップ\programing\application\spread-sheet-test.json"
        )

        # スプレッドシートの作成
        sh = gc.create(
            sheet_name,  #スプレッドシートファイルの名前
            folder_id="1whd_faQzwajdZnuClNrNr6QUhzkd18K-" # スプレッドシートを保存するフォルダのID
        )

        # シートの作成
        ws = sh.worksheet('Sheet1')
        ws.clear()

        # 列幅の調整
        request = {
            "requests": [{
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": ws.id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,  # A列（0から開始）
                        "endIndex": 1
                    },
                    "properties": {"pixelSize": 500},  # 500pxに固定
                    "fields": "pixelSize"
                }
            }]
        }
        sh.batch_update(request)

        # データフレームのスプレッドシートへの書き込み
        ws.update(
            [data.columns.values.tolist()] + data.values.tolist()
        )