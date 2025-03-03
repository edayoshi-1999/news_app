import gspread
import pandas as pd

# 認証情報を使ってスプレッドシートにアクセスするためのクライアントを作る
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
df = pd.DataFrame({
    "名前": ["山田", "佐藤", "鈴木"],
    "年齢": [20, 30, 40]
})

# データフレームのスプレッドシートへの書き込み
ws.update(
    [df.columns.values.tolist()] + df.values.tolist()
)