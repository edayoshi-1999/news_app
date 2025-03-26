import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from scrapingNikkeiMed import fetch_html, parse_article_info, save_to_spreadsheet
import requests

# fetch_html関数のテスト
class TestFetchHtml(unittest.TestCase):

    # 正常系:（正常にHTMLを返すか）
    @patch('scrapingNikkeiMed.requests.get')
    def test_fetch_html_success(self, mock_get):

        # モックレスポンスを定義
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>test</body></html>'
        mock_get.return_value = mock_response

        html = fetch_html('https://dummyurl.com')
        self.assertEqual(html, '<html><body>test</body></html>')

    # 例外処理：（例外発生時にNoneを返すか）
    @patch('scrapingNikkeiMed.requests.get')
    def test_fetch_html_exception(self, mock_get):
        # リクエストで例外が発生するように設定
        mock_get.side_effect = requests.exceptions.RequestException("接続エラー")

        html = fetch_html('https://dummyurl.com')
        self.assertIsNone(html)  # Noneが返ってくることを確認

# parse_article_info関数のテスト
class TestParseArticleInfo(unittest.TestCase):
    # 正常系：（HTMLから正しく記事リストを抽出できるか）
    def test_parse_article_info(self):
        sample_html = '''
        <html><body>
            <div class="detail-inner"><a href="/article1.html"></a></div>
            <p class="article-list-article-title">Title 1</p>
            <p class="article-list-date">2025-03-25</p>
            <a class="article-list-tag">News</a>
            <div class="detail-inner"><a href="/article2.html"></a></div>
            <p class="article-list-article-title">Title 2</p>
            <p class="article-list-date">2025-03-24</p>
            <a class="article-list-tag">Update</a>
        </body></html>
        '''
        expected = [
            ['Title 1', '2025-03-25', 'News', 'https://medical.nikkeibp.co.jp/article1.html'],
            ['Title 2', '2025-03-24', 'Update', 'https://medical.nikkeibp.co.jp/article2.html']
        ]

        result = parse_article_info(sample_html)
        self.assertEqual(result, expected)

    # 分岐処理：htmlがNoneのとき空リストを返すか
    def test_parse_article_info_with_none(self):
        result = parse_article_info(None)
        self.assertEqual(result, [])

    # 例外処理：HTML構造が不正で例外が発生した場合でも空リストを返すか
    def test_parse_article_info_with_invalid_html(self):
        # URLがNoneで .attrs["href"] を読もうとして例外になるケースを作る
        invalid_html = '''
        <html><body>
            <div class="detail-inner"></div>  <!-- aタグがない -->
            <p class="article-list-article-title">Title 1</p>
            <p class="article-list-date">2025-03-25</p>
            <a class="article-list-tag">News</a>
        </body></html>
        '''
        result = parse_article_info(invalid_html)
        self.assertEqual(result, [])  # エラー時は空リストになるはず


# save_to_spreadsheet関数のテスト
class TestSaveToSpreadsheet(unittest.TestCase):
    # 正常系：（DataFrameが正しく渡されるか）
    @patch('spreadSheetModule.SpreadSheet')  
    def test_save_to_spreadsheet(self, mock_spreadsheet_class):
        data = [['Title 1', '2025-03-25', 'News', 'https://medical.nikkeibp.co.jp/article1.html']]
        df_expected = pd.DataFrame(data, columns=['title', 'date', 'tag', 'url'])

        save_to_spreadsheet(data)

        # writeSpreadSheetが正しく呼び出されたかをチェック
        mock_instance = mock_spreadsheet_class.return_value
        mock_instance.writeSpreadSheet.assert_called_once()
        # writeSpreadSheetに渡された引数が正しいかをチェック
        args, kwargs = mock_instance.writeSpreadSheet.call_args
        pd.testing.assert_frame_equal(args[0], df_expected)
        self.assertEqual(args[1], '日経メディカル')

    # 分岐処理：空データが渡されたときにスキップされるか
    @patch('spreadSheetModule.SpreadSheet')
    def test_save_to_spreadsheet_with_empty_data(self, mock_spreadsheet_class):
        save_to_spreadsheet([])  # 空リスト

        # writeSpreadSheetは呼び出されないはず
        mock_instance = mock_spreadsheet_class.return_value
        mock_instance.writeSpreadSheet.assert_not_called()

    # 例外処理：書き込み中に例外が発生したとき
    @patch('spreadSheetModule.SpreadSheet')
    def test_save_to_spreadsheet_with_exception(self, mock_spreadsheet_class):
        # モックで例外を投げるように設定
        mock_instance = mock_spreadsheet_class.return_value
        mock_instance.writeSpreadSheet.side_effect = Exception("書き込みエラー")

        data = [['Title 1', '2025-03-25', 'News', 'https://medical.nikkeibp.co.jp/article1.html']]
        save_to_spreadsheet(data)

        # 呼び出されたが例外を処理したことを確認（例外が上がらない＝printで処理されている）
        mock_instance.writeSpreadSheet.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)