import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from spreadSheetModule import SpreadSheet
import gspread
from requests.models import Response

class TestSpreadSheet(unittest.TestCase):

    # 正常系：各メソッドが正しく呼ばれるか
    @patch('spreadSheetModule.os.getenv')
    @patch('spreadSheetModule.gspread.service_account')
    def test_write_spreadsheet_success(self, mock_service_account, mock_getenv):
        # --- 環境変数のモック ---
        mock_getenv.side_effect = lambda key: {
            "SERVICE_ACCOUNT_JSON_PATH": "dummy/path.json",
            "SPREADSHEET_FOLDER_ID": "dummy_folder_id"
        }[key]

        # --- gspread クライアントのモック ---
        mock_gc = MagicMock()
        mock_sh = MagicMock()
        mock_ws = MagicMock()
        mock_ws.id = 1234

        # モックチェーンを構築。入れ子構造のため。
        mock_service_account.return_value = mock_gc
        mock_gc.create.return_value = mock_sh
        mock_sh.worksheet.return_value = mock_ws

        # --- テストデータ ---
        data = pd.DataFrame([["タイトル", "2025-03-26", "https://example.com"]], columns=["title", "date", "url"])
        
        sheet = SpreadSheet()

        # 実行
        sheet.writeSpreadSheet(data, "テストシート")

        # --- 各メソッドが呼ばれたかをチェック ---
        mock_service_account.assert_called_once_with(filename="dummy/path.json")
        mock_gc.create.assert_called_once_with("テストシート", folder_id="dummy_folder_id")
        mock_sh.worksheet.assert_called_once_with("Sheet1")
        mock_ws.clear.assert_called_once()
        mock_sh.batch_update.assert_called_once()
        mock_ws.update.assert_called_once_with([data.columns.tolist()] + data.values.tolist())

    # 例外処理：APIエラーが発生したとき
    @patch('spreadSheetModule.os.getenv', return_value="dummy")
    @patch('spreadSheetModule.gspread.service_account')
    def test_write_spreadsheet_api_error(self, mock_service_account, mock_getenv):
        # 疑似レスポンスを作成
        response = Response()
        response.status_code = 403
        response._content = '''
        {
        "error": {
            "message": "アクセス拒否",
            "code": 403
        }
        }
        '''.encode('utf-8')

        # APIError を正しく生成
        api_error = gspread.exceptions.APIError(response)

        mock_gc = MagicMock()
        mock_service_account.return_value = mock_gc
        mock_gc.create.side_effect = api_error  # 正しく例外を投げる

        data = pd.DataFrame([["タイトル", "日付", "URL"]], columns=["title", "date", "url"])

        sheet = SpreadSheet()
        sheet.writeSpreadSheet(data, "APIエラーシート")

        mock_gc.create.assert_called_once()

    # 例外処理：認証用JSONファイルが見つからないとき
    @patch('spreadSheetModule.os.getenv', return_value="dummy")
    @patch('spreadSheetModule.gspread.service_account')
    def test_write_spreadsheet_file_not_found_error(self, mock_service_account, mock_getenv):
        mock_service_account.side_effect = FileNotFoundError("ファイルが見つかりません")

        data = pd.DataFrame([["タイトル", "日付", "URL"]], columns=["title", "date", "url"])
        sheet = SpreadSheet()
        sheet.writeSpreadSheet(data, "ファイルなし")

        mock_service_account.assert_called_once()

    # 例外処理：その他の例外が発生したとき
    @patch('spreadSheetModule.os.getenv', return_value="dummy")
    @patch('spreadSheetModule.gspread.service_account')
    def test_write_spreadsheet_other_exception(self, mock_service_account, mock_getenv):
        mock_gc = MagicMock()
        mock_service_account.return_value = mock_gc

        # worksheet() 呼び出しで想定外のエラーを発生させる
        mock_sh = MagicMock()
        mock_gc.create.return_value = mock_sh
        mock_sh.worksheet.side_effect = Exception("予期しないエラー")

        data = pd.DataFrame([["タイトル", "日付", "URL"]], columns=["title", "date", "url"])
        sheet = SpreadSheet()
        sheet.writeSpreadSheet(data, "例外シート")

        mock_gc.create.assert_called_once()