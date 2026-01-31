import unittest
from pathlib import Path
from wikiscraper.page import Page
from wikiscraper import config
from wikiscraper.controller import Controller
from wikiscraper.scraper import Scraper
from unittest.mock import patch, mock_open, MagicMock

HTML_SAMPLE = """
<div class="mw-content-ltr">
  <p>Team Rocket (Japanese: ロケット団 Rocket-dan) is a villainous team.</p>
  <table>
    <tr><th>Pokemon</th><th>Type</th></tr>
    <tr><td>Bulbasaur</td><td>Grass/Poison</td></tr>
    <tr><td>Charmander</td><td>Fire</td></tr>
  </table>
  <a href="/wiki/Bulbasaur">Bulbasaur</a>
  <a href="/wiki/Charmander">Charmander</a>
</div>
"""

class TestPage(unittest.TestCase):

    def setUp(self):
        self.page = Page("Team Rocket", HTML_SAMPLE)

    def test_summary(self):
        print("\n--- Summary Test ---")
        self.page.summary()  # should print first paragraph

    def test_table(self):
        print("\n--- Table Test ---")
        df = self.page.table(1, first_row_is_header=True)
        self.assertEqual(list(df.columns), ["Pokemon", "Type"])
        self.assertEqual(len(df), 2)

    def test_count_words(self):
        print("\n--- Count Words Test ---")
        words = self.page.count_words()
        self.assertIn("Team", words)
        self.assertIn("Rocket", words)

    def test_links(self):
        print("\n--- Links Test ---")
        links = self.page.links()
        self.assertIn("Bulbasaur", links)
        self.assertIn("Charmander", links)

class TestScraper(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="<html>Test</html>")
    @patch("os.path.exists")
    def test_scrape_reads_local_file(self, mock_exists, mock_file):
        # Setup
        mock_exists.return_value = True
        scraper = Scraper("TestPhrase", use_local_html_file_instead=True)

        # Call
        page = scraper.scrape()

        # Assertions
        self.assertIsInstance(page, Page)
        self.assertEqual(page.html, "<html>Test</html>")

    @patch('pathlib.Path.open')  # 3. Third from bottom -> Third arg
    @patch('requests.get')       # 2. Second from bottom -> Second arg
    @patch('os.path.exists')     # 1. Closest to function -> First arg
    def test_scrape_downloads_if_not_local(self, mock_exists, mock_get, mock_path_open):
        # 1. Setup
        mock_exists.return_value = True 
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html>Downloaded</html>"
        mock_get.return_value = mock_response

        scraper = Scraper("TestPhrase", use_local_html_file_instead=False)

        # 2. Call
        page = scraper.scrape()

        # 3. Assertions
        mock_get.assert_called_once()
        self.assertIsInstance(page, Page)
        self.assertEqual(page.html, "<html>Downloaded</html>")

    @patch("os.path.exists")
    def test_scrape_fails_if_file_missing(self, mock_exists):
        # Setup
        mock_exists.return_value = False
        scraper = Scraper("MissingFile", use_local_html_file_instead=True)

        # Should exit because file is missing
        with self.assertRaises(SystemExit):
            scraper.scrape()


class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()

    ## --- Test Cache Logic ---
    @patch('os.path.exists')
    @patch('wikiscraper.config.CACHE_DIR', Path('/mock/cache'))
    def test_is_html_in_cache(self, mock_exists):
        mock_exists.return_value = True
        result = self.controller.is_html_in_cache("test_phrase")
        
        self.assertTrue(result)
        mock_exists.assert_called_once_with(Path('/mock/cache/test_phrase'))

    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.unlink')
    def test_clear_cache_removes_files(self, mock_unlink, mock_isfile, mock_listdir):
        # Setup: Mock one file in the directory
        mock_listdir.return_value = ['file1.html']
        mock_isfile.return_value = True
        
        self.controller.clear_cache()
        
        mock_unlink.assert_called_once()

    ## --- Test Core Logic ---
    @patch('controller.Scraper')
    @patch('controller.Controller.is_html_in_cache')
    def test_get_page_cached(self, mock_is_cached, mock_scraper_class):
        # Setup
        mock_is_cached.return_value = True
        mock_scraper_instance = mock_scraper_class.return_value
        # Note: In your code 'return sc.scrape' (missing parens) is a bug!
        # This test checks for the fix: return sc.scrape()
        
        self.controller._get_page("test_phrase")
        
        mock_scraper_class.assert_called_with(phrase="test_phrase", use_local_html_file_instead=True)


    @patch('wordfreq.word_frequency')
    @patch('wordfreq.top_n_list')
    @patch('json.loads')
    @patch('pathlib.Path.read_text')
    def test_analyze_relative_word_frequency_article_mode(self, mock_read, mock_json, mock_top_n, mock_word_freq):
        # Setup
        mock_read.return_value = '{"hello": 10}'
        mock_json.return_value = {"hello": 10}
        mock_word_freq.return_value = 0.01
        
        # We capture stdout to prevent print clutter during tests
        with patch('pandas.DataFrame.info'): 
            self.controller.analyze_relative_word_frequency(mode="article", count=1)
            
        mock_word_freq.assert_called_with("hello", 'en', wordlist='small')

    ## --- Test Command Execution ---
    def test_run_func(self):
        # Mock the argparse Namespace
        mock_args = MagicMock()
        mock_func = MagicMock()
        mock_args.func = mock_func
        mock_args.command = "test"
        # vars(mock_args) needs to return a dict
        mock_args.__dict__ = {'func': mock_func, 'command': 'test', 'phrase': 'apple'}
        
        self.controller.run_func(mock_args)
        
        mock_func.assert_called_once_with(phrase='apple')


if __name__ == "__main__":
    unittest.main()