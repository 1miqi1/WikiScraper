"""
Module: controller.py

Provides the Controller class for orchestrating wiki scraping operations.

Responsibilities:
    - Fetching pages via Scraper
    - Running CLI commands
    - Clearing cache, data, and JSON files
    - Counting words recursively across linked pages
    - Extracting summaries and tables
    - Analyzing and visualizing relative word frequencies
"""

import os
import time
import shutil
import random
import json
from queue import Queue
from pathlib import Path

import wordfreq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from wikiscraper.scraper import Scraper
from wikiscraper.page import Page
from wikiscraper import config


class Controller:
    """
    Orchestrates operations for wiki scraping, word counting, table extraction,
    and relative word frequency analysis.
    """

    def __init__(
        self,
        clear_cache: bool = False,
        clear_json: bool = False,
        clear_data: bool = False,
    ):
        """
        Initialize the Controller, ensuring necessary directories and files exist.

        Optionally clears cached HTML, JSON word counts, and output data.
        """
        if not os.path.exists(config.DATA_DIR):
            os.makedirs(config.DATA_DIR)

        if not os.path.exists(config.WORD_COUNTS_JSON):
            with open(config.WORD_COUNTS_JSON, "wb") as file:
                file.write(b"")

        if clear_data:
            self.clear_data()
        if clear_cache:
            self.clear_cache()
        if clear_json:
            self.clear_json()

    def run_func(self, args):
        """
        Automatically run the function associated with the CLI subcommand.

        Args:
            args (argparse.Namespace): Parsed arguments from CLI parser.

        Returns:
            Any: Return value of the called function.
        """
        func_name = args.command
        arg_dict = vars(args).copy()
        arg_dict.pop("command")

        func = getattr(self, func_name)
        return func(**arg_dict)

    def is_html_in_cache(self, phrase: str) -> bool:
        """Check if a cached HTML file exists for a given phrase."""
        path = config.CACHE_DIR / phrase
        return os.path.exists(path)

    def clear_data(self) -> None:
        """Delete all files in the data directory."""
        folder = config.DATA_DIR
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def clear_cache(self) -> None:
        """Delete all files and folders in the cache directory."""
        folder = config.CACHE_DIR
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def clear_json(self) -> None:
        """Clear the word count JSON file."""
        path = config.WORD_COUNTS_JSON
        with open(path, "wb") as file:
            file.write(b"")

    def _get_page(self, phrase: str, wait: int = 0) -> Page:
        """Fetch a Page object for a phrase, using cache if available."""
        if self.is_html_in_cache(phrase=phrase):
            sc = Scraper(phrase=phrase, use_local_html_file_instead=True)
            return sc.scrape()
        time.sleep(wait)
        sc = Scraper(phrase=phrase, use_local_html_file_instead=False)
        return sc.scrape()

    def summary(self, phrase: str):
        """Print the summary of a wiki page."""
        page = self._get_page(phrase=phrase)
        return page.summary()

    def count_words(self, phrase: str):
        """Count words on a wiki page and update JSON counts."""
        page = self._get_page(phrase=phrase)
        page.count_words()

    def table(
        self,
        phrase: str,
        number: int,
        output_dir: str = config.DATA_DIR,
        first_row_is_header: bool = False,
    ):
        """Extract, display, and save the n-th table from a wiki page."""
        page = self._get_page(phrase=phrase)
        page.table(n=number, output_dir=output_dir,
                   first_row_is_header=first_row_is_header)

    def next_page(self, page: Page, wait: int) -> Page:
        """Navigate to a randomly selected link from the current page."""
        links = page.links()
        winner = random.choice(links)
        return self._get_page(phrase=winner, wait=wait)

    def auto_count_words(self, phrase: str, depth: int, wait: int):
        """Recursively count words on a page and linked pages up to depth."""
        if depth <= 0:
            return

        visited = set()
        q = Queue()
        q.put((phrase, 0))

        while not q.empty():
            current_phrase, current_depth = q.get()
            if current_phrase in visited:
                continue
            visited.add(current_phrase)

            current_page = self._get_page(phrase=current_phrase, wait=wait)
            current_page.count_words()

            if current_depth >= depth:
                continue

            for link in current_page.links():
                q.put((link, current_depth + 1))

    def normalyze(self, v: list[float]) -> np.ndarray:
        """Normalize a list of numeric values so they sum to 1."""
        v = np.array(v)
        return v / np.sum(v)

    def analyze_relative_word_frequency(
        self,
        mode: str,
        count: int,
        chart: str = None,
    ):
        """Compare and visualize word frequencies in a wiki article vs. language."""
        language = "en"
        try:
            raw = config.WORD_COUNTS_JSON.read_text(encoding="utf-8").strip()
            data: dict[str, int] = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {}

        if mode == "article":
            sorted_freqs = sorted(data.items(), key=lambda item: item[1], reverse=True)
            words = [k for k, _ in sorted_freqs[:count]]
        else:
            words = wordfreq.top_n_list("en", count)

        words.reverse()
        counts_in_article = []
        counts_in_language = []

        for word in words:
            counts_in_language.append(
                wordfreq.word_frequency(word, language, wordlist="small") or 0
            )
            counts_in_article.append(data.get(word, 0))

        freq_in_language = self.normalyze(counts_in_language)
        freq_in_article = self.normalyze(counts_in_article)

        df = pd.DataFrame({
            "Word": words,
            "Language_Freq": freq_in_language,
            "Article_Freq": freq_in_article,
        })

        print(df)

        if chart is not None:
            x = np.arange(count)
            width = 0.35

            plt.xticks(rotation=45)
            plt.bar(x - width / 2, freq_in_language, width,
                    color="red", label=language)
            plt.bar(x + width / 2, freq_in_article, width,
                    color="blue", label="Article")

            plt.xticks(x, words)
            plt.ylabel("Frequency in %")
            plt.title("Frequency of some words on Wiki")
            plt.legend()
            plt.tight_layout()
            plt.savefig(chart)
            plt.clf()
            
            
