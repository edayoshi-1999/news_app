import SpreadSheetModule

# テストデータ
data = {
    "name": ["aaa", "bbb"],
    "age": [10, 20]
}

# テスト。スプレッドシートモジュールをよびだして、引数のデータを書きこむ。
sh = SpreadSheetModule.SpreadSheet()
sh.writeSpreadSheet(data)