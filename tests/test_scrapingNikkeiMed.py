import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from scrapingNikkeiMed import fetch_html, parse_article_info, save_to_spreadsheet

# === テストクラス ===
class TestScrapingNikkeiMed(unittest.TestCase):

    # fetch_htmlのテスト（正常にHTMLを返すか）
    @patch('scrapingNikkeiMed.requests.get')
    def test_fetch_html_success(self, mock_get):

        # モックレスポンスを定義
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>test</body></html>'
        mock_get.return_value = mock_response

        html = fetch_html('https://dummyurl.com')
        self.assertEqual(html, '<html><body>test</body></html>')

    # parse_article_infoのテスト（HTMLから正しく記事リストを抽出できるか）
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

    # save_to_spreadsheetのテスト（DataFrameが正しく渡されるか）
    @patch('SpreadSheetModule.SpreadSheet')  # ファイル名に応じて要修正
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


if __name__ == '__main__':
    unittest.main(verbosity=2)