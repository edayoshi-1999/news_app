import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from newsAPI import extract_source_name, clean_and_format_data, translate_titles, fetch_news_data, save_to_spreadsheet


# ニュース処理に関する各関数の単体テストを行うクラス
class TestNewsAPI(unittest.TestCase):

     # source辞書からnameを抽出する関数のテスト
    def test_extract_source_name(self):
        # 正常に'name'を取り出せるケース
        self.assertEqual(extract_source_name({'name': 'BBC'}), 'BBC')
        # nameキーが存在しない場合、空文字が返る
        self.assertEqual(extract_source_name({}), '')
        # 入力が辞書でない場合、例外を出さずに空文字が返る
        self.assertEqual(extract_source_name('not a dict'), '')

    # ニュースAPIからの取得処理のテスト（requests.getとos.getenvをモック）
    @patch('newsAPI.requests.get')
    @patch('newsAPI.os.getenv')
    def test_fetch_news_data(self, mock_getenv, mock_get):
        # APIキーの取得とHTTPレスポンスをモック
        mock_getenv.return_value = 'fake-api-key'
        mock_response = MagicMock()
        mock_response.json.return_value = {'articles': [{'title': 'Test', 'source': {'name': 'Test Source'}}]}
        mock_get.return_value = mock_response

        articles = fetch_news_data()
        # 結果がリストであることを確認
        self.assertIsInstance(articles, list)
        # 正しくデータが取得されているか確認
        self.assertEqual(articles[0]['title'], 'Test')

    # APIで取得した記事データを整形する関数のテスト
    def test_clean_and_format_data(self):
        # 模擬データ（正常値と欠損値を含む）
        articles = [
            {'title': 'Test Title', 'source': {'name': 'CNN'}, 'author': 'Author A', 'publishedAt': '2025-03-24', 'url': 'http://example.com'},
            {'title': None, 'source': {'name': 'BBC'}, 'author': None, 'publishedAt': None, 'url': None},
            {'title': 'Another Title', 'source': None, 'author': 'Author B', 'publishedAt': '2025-03-25', 'url': 'http://another.com'},
            {'title': 'No Source Key', 'source': {}, 'author': 'Author C', 'publishedAt': '2025-03-26', 'url': 'http://nosource.com'}
        ]
        df = clean_and_format_data(articles)
        # DataFrameであることを確認
        self.assertIsInstance(df, pd.DataFrame)
        # source列が含まれているか確認
        self.assertIn('source', df.columns)
        # 各列の値が正しく変換されているか
        self.assertEqual(df.loc[0, 'source'], 'CNN')
        self.assertEqual(df.loc[1, 'source'], 'BBC')
        self.assertEqual(df.loc[1, 'title'], '')  # 欠損値が空文字に変換されているか
        self.assertEqual(df.loc[2, 'source'], '')  # sourceがNoneの場合も空文字に変換されるか
        self.assertEqual(df.loc[3, 'source'], '')  # sourceが{}のときも空文字に変換されるか

    # タイトル翻訳処理のテスト（翻訳APIをモック）
    @patch('newsAPI.translate_text')
    def test_translate_titles(self, mock_translate_text):
        # モックで翻訳結果を返す
        mock_translate_text.return_value = ['Translated Title 1', 'Translated Title 2']
        df = pd.DataFrame({'title': ['Title 1', 'Title 2']})
        result_df = translate_titles(df)
        # タイトルが翻訳された内容に置き換わっているか確認
        self.assertEqual(result_df.loc[0, 'title'], 'Translated Title 1')
        self.assertEqual(result_df.loc[1, 'title'], 'Translated Title 2')

    # スプレッドシートへの書き込み処理のテスト（SpreadSheetクラスをモック）
    @patch('SpreadSheetModule.SpreadSheet')
    def test_save_to_spreadsheet(self, mock_spreadsheet_class):
        # モックのスプレッドシートオブジェクトを準備
        mock_spreadsheet = MagicMock()
        mock_spreadsheet_class.return_value = mock_spreadsheet

        # 仮のニュースデータフレーム
        df = pd.DataFrame({
            'title': ['Test Title'],
            'source': ['Test Source'],
            'author': ['Test Author'],
            'publishedAt': ['2025-03-24'],
            'url': ['http://example.com']
        })

        save_to_spreadsheet(df)
        # writeSpreadSheet メソッドが1回呼ばれたことを検証
        mock_spreadsheet.writeSpreadSheet.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)