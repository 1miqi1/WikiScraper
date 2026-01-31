"""
Unit and integration tests for the WikiScraper project.

Tests include:
- Page class: summary extraction, table parsing, word counting, link extraction
- Scraper class: reading local HTML, downloading HTML, error handling
- Controller class: cache logic, clearing cache, analyzing word frequency

Uses unittest and mocking to isolate components where needed.
"""

import unittest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from wikiscraper.page import Page
from wikiscraper import config
from wikiscraper.controller import Controller
from wikiscraper.scraper import Scraper

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
    """Tests for the Page class functionality."""

    def setUp(self):
        """Initialize a Page object for testing."""
        self.page = Page("Team Rocket", HTML_SAMPLE)

    def test_summary(self):
        """Test that the summary prints the first paragraph correctly."""
        print("\n--- Summary Test ---")
        self.page.summary()

    def test_table(self):
        """Test table extraction returns correct DataFrame structure."""
        print("\n--- Table Test ---")
        df = self.page.table(1, first_row_is_header=True)
        self.assertEqual(list(df.columns), ["Pokemon", "Type"])
        self.assertEqual(len(df), 2)

    def test_count_words(self):
        """Test that count_words returns expected words from HTML content."""
        print("\n--- Count Words Test ---")
        words = self.page.count_words()
        self.assertIn("team", words)
        self.assertIn("rocket", words)

    def test_links(self):
        """Test that valid wiki links are extracted and filtered correctly."""
        print("\n--- Links Test ---")
        links = self.page.links()
        self.assertIn("Bulbasaur", links)
        self.assertIn("Charmander", links)


class TestScraper(unittest.TestCase):
    """Tests for the Scraper class."""

    @patch("builtins.open", new_callable=mock_open, read_data="<html>Test</html>")
    @patch("os.path.exists")
    def test_scrape_reads_local_file(self, mock_exists, mock_file):
        """Test Scraper returns correct Page when reading a local HTML file."""
        mock_exists.return_value = True
        scraper = Scraper("TestPhrase", use_local_html_file_instead=True)
        page = scraper.scrape()
        self.assertIsInstance(page, Page)
        self.assertEqual(page.html, "<html>Test</html>")

    @patch("pathlib.Path.open")
    @patch("requests.get")
    @patch("os.path.exists")
    def test_scrape_downloads_if_not_local(self, mock_exists, mock_get, mock_path_open):
        """Test Scraper downloads HTML if local file does not exist."""
        mock_exists.return_value = True
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html>Downloaded</html>"
        mock_get.return_value = mock_response

        scraper = Scraper("TestPhrase", use_local_html_file_instead=False)
        page = scraper.scrape()
        mock_get.assert_called_once()
        self.assertIsInstance(page, Page)
        self.assertEqual(page.html, "<html>Downloaded</html>")

    @patch("os.path.exists")
    def test_scrape_fails_if_file_missing(self, mock_exists):
        """Test Scraper exits if local HTML file missing and download not allowed."""
        mock_exists.return_value = False
        scraper = Scraper("MissingFile", use_local_html_file_instead=True)
        with self.assertRaises(SystemExit):
            scraper.scrape()


class TestController(unittest.TestCase):
    """Tests for the Controller class."""

    def setUp(self):
        """Initialize Controller instance for tests."""
        self.controller = Controller()

    @patch("os.path.exists")
    @patch("wikiscraper.config.CACHE_DIR", Path("/mock/cache"))
    def test_is_html_in_cache(self, mock_exists):
        """Test that cached HTML detection works correctly."""
        mock_exists.return_value = True
        result = self.controller.is_html_in_cache("test_phrase")
        self.assertTrue(result)
        mock_exists.assert_called_once_with(Path("/mock/cache/test_phrase"))

    @patch("os.listdir")
    @patch("os.path.isfile")
    @patch("os.unlink")
    def test_clear_cache_removes_files(self, mock_unlink, mock_isfile, mock_listdir):
        """Test that clear_cache deletes files in the cache directory."""
        mock_listdir.return_value = ["file1.html"]
        mock_isfile.return_value = True
        self.controller.clear_cache()
        mock_unlink.assert_called_once()

    @patch("wordfreq.word_frequency")
    @patch("wordfreq.top_n_list")
    @patch("json.loads")
    @patch("pathlib.Path.read_text")
    def test_analyze_relative_word_frequency_article_mode(
        self, mock_read, mock_json, mock_top_n, mock_word_freq
    ):
        """
        Test relative word frequency analysis in article mode.
        """
        mock_read.return_value = '{"hello": 10}'
        mock_json.return_value = {"hello": 10}
        mock_word_freq.return_value = 0.01
        with patch("pandas.DataFrame.info"):
            self.controller.analyze_relative_word_frequency(mode="article", count=1)
        mock_word_freq.assert_called_with("hello", "en", wordlist="small")


if __name__ == "__main__":
    unittest.main()
