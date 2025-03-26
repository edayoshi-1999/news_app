import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from scrapingZiziMed import fetch_html, parse_articles, save_to_spreadsheet  # 実際のファイル名に合わせて
import requests


# fetch_html関数のテスト
class TestFetchHtml(unittest.TestCase):
    # 正常系（正常にHTMLを返すか）
    @patch('scrapingZiziMed.requests.get')
    def test_fetch_html_success(self, mock_get):

        # モックレスポンスを定義
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>test</body></html>'
        mock_get.return_value = mock_response

        html = fetch_html('https://dummyurl.com')
        self.assertEqual(html, '<html><body>test</body></html>')

    # 例外処理：（例外発生時にNoneを返すか）
    @patch('scrapingZiziMed.requests.get')
    def test_fetch_html_exception(self, mock_get):
        # リクエストで例外が発生するように設定
        mock_get.side_effect = requests.exceptions.RequestException("接続エラー")

        html = fetch_html('https://dummyurl.com')
        self.assertIsNone(html)  # Noneが返ってくることを確認


# parse_articles関数のテスト
class TestParseArticles(unittest.TestCase):
    # 正常系（HTMLから正しく記事リストを抽出できるか）
    def test_parse_articles(self):
        sample_html = '''
        <html><body>
            <p class="articleTextList__title">Title 1</p>
            <span class="articleTextList__date">2025-03-25</span>
            <li class="articleTextList__item"><a href="/article1.html"></a></li>
            <p class="articleTextList__title">Title 2</p>
            <span class="articleTextList__date">2025-03-24</span>
            <li class="articleTextList__item"><a href="/article2.html"></a></li>
        </body></html>
        '''
        expected = [
            ['Title 1', '2025-03-25', 'https://medical.jiji.com/article1.html'],
            ['Title 2', '2025-03-24', 'https://medical.jiji.com/article2.html']
        ]

        result = parse_articles(sample_html)
        self.assertEqual(result, expected)

    # 分岐処理：htmlがNoneのとき空リストを返すか
    def test_parse_articles_with_none(self):
        result = parse_articles(None)
        self.assertEqual(result, [])
    
    # 例外処理: 空リストを返すか
    def test_parse_articles_exception(self):
        result = parse_articles('invalid html')
        self.assertEqual(result, [])

# save_to_spreadsheet関数のテスト
class TestSaveToSpreadsheet(unittest.TestCase):
    # 正常系：データが正しく書き込まれるかを確認
    @patch('spreadSheetModule.SpreadSheet')  # SpreadSheetクラスをモック化
    def test_save_to_spreadsheet_success(self, mock_spreadsheet_class):
        # テスト用のサンプルデータ
        data = [['タイトル', '2025-03-25', 'https://example.com/article']]
        expected_df = pd.DataFrame(data, columns=['title', 'date', 'url'])

        # 関数を実行
        save_to_spreadsheet(data)

        # writeSpreadSheet が1回だけ呼び出されているか
        mock_instance = mock_spreadsheet_class.return_value
        mock_instance.writeSpreadSheet.assert_called_once()

        # 渡された引数（DataFrameとシート名）が正しいか確認
        args, kwargs = mock_instance.writeSpreadSheet.call_args
        pd.testing.assert_frame_equal(args[0], expected_df)
        self.assertEqual(args[1], '時事メディカル')

    # 分岐処理：空のデータが渡されたときに処理がスキップされるか
    @patch('spreadSheetModule.SpreadSheet')
    def test_save_to_spreadsheet_with_empty_data(self, mock_spreadsheet_class):
        # 空データで関数を実行
        save_to_spreadsheet([])

        # writeSpreadSheet は一度も呼ばれないはず
        mock_instance = mock_spreadsheet_class.return_value
        mock_instance.writeSpreadSheet.assert_not_called()

    # 例外処理：スプレッドシートへの書き込み時に例外が発生した場合でも関数が落ちないか
    @patch('spreadSheetModule.SpreadSheet')
    def test_save_to_spreadsheet_with_exception(self, mock_spreadsheet_class):
        # writeSpreadSheet が例外を投げるように設定
        mock_instance = mock_spreadsheet_class.return_value
        mock_instance.writeSpreadSheet.side_effect = Exception("書き込みエラー")

        data = [['タイトル', '2025-03-25', 'https://example.com/article']]
        
        # 関数を実行（printだけで例外は再スローされない想定）
        save_to_spreadsheet(data)

        # 呼び出しはされたが、例外を出して処理が止まらないことを確認
        mock_instance.writeSpreadSheet.assert_called_once()

    
if __name__ == '__main__':
    unittest.main(verbosity=2)