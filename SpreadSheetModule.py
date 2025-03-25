import gspread
import pandas as pd
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()
class SpreadSheet:

    # Google スプレッドシートにDataFrameを書き込む
    def writeSpreadSheet(self, data:pd.DataFrame, sheet_name:str):
        try:
            # .envから設定を取得
            json_path = os.getenv("SERVICE_ACCOUNT_JSON_PATH")
            folder_id = os.getenv("SPREADSHEET_FOLDER_ID")

            # 認証情報を使ってスプレッドシートにアクセスするためのクライアントを作る
            gc = gspread.service_account(
                filename = json_path
            )

            # スプレッドシートの作成
            sh = gc.create(
                sheet_name,  #スプレッドシートファイルの名前
                folder_id = folder_id # スプレッドシートを保存するフォルダのID
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

            # データフレームのスプレッドシートへの書き込み（1行目: ヘッダー, 2行目以降: データ）
            ws.update(
                [data.columns.tolist()] + data.values.tolist()
            )

            print(f"[成功] スプレッドシート『{sheet_name}』に書き込み完了。")
        
        except gspread.exceptions.APIError as e:
            print(f"[エラー] GoogleAPIの呼び出しに失敗しました: {e}")
        except FileNotFoundError as e:
            print(f"[エラー] 認証用JSONファイルが見つかりません: {e}")
        except Exception as e:
            print(f"[エラー] スプレッドシートへの書きこみで予期しないエラー: {e}")