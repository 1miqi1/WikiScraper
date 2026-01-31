"""
Integration tests for the WikiScraper project.

This module provides stub integration tests for key functionality of the
WikiScraper, including extracting summaries and counting words. These tests
check the interaction between the Parser, Controller, and Page classes, as well
as file I/O for word counts.
"""

import json
import tempfile
from pathlib import Path

from wikiscraper.page import Page
from wikiscraper import config
from wikiscraper.controller import Controller
from wikiscraper.scraper import Scraper
from wikiscraper.parser import Parser


def integration_test_summary():
    """
    Integration test for extracting the summary of a wiki page.

    Uses the Parser and Controller to retrieve the summary of "Team Rocket"
    and asserts that the returned text starts and ends with expected phrases.

    Raises:
        AssertionError: If the summary does not match expected values.
    """
    parser = Parser()
    controller = Controller()
    test_args = ["summary", "Team Rocket"]

    summary = controller.run_func(parser.parser.parse_args(test_args))
    assert summary.startswith("Team Rocket")
    assert summary.endswith("Sevii Islands .")
    print("INTEGRATION_TEST_COUNT_SUMMARY: Passed")


def integration_test_count_words():
    """
    Integration test for counting words on a wiki page.

    This test:
        - Uses a temporary JSON file to simulate `WORD_COUNTS_JSON`.
        - Records the current count of the word "Fossils".
        - Runs the Controller to count words on the "Team Rocket" page.
        - Verifies that the count of "Fossils" increases by 1.
        - Restores the original configuration path.

    Raises:
        AssertionError: If the word count does not increase as expected.
    """
    parser = Parser()
    controller = Controller()
    test_args = ["count_words", "Team Rocket"]

    # Use a temporary file instead of the real WORD_COUNTS_JSON
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp_file:
        tmp_file.write(json.dumps({"Fossils": 3}))  # initial value
        tmp_file.flush()

        original_path = config.WORD_COUNTS_JSON
        config.WORD_COUNTS_JSON = tmp_file.name

        with open(config.WORD_COUNTS_JSON, "r", encoding="utf-8") as file:
            words = json.load(file)
        current_word_fossils = words.get("Fossils", 0)

        controller.run_func(parser.parser.parse_args(test_args))

        with open(config.WORD_COUNTS_JSON, "r", encoding="utf-8") as file:
            words = json.load(file)
        after_change_fossils = words.get("Fossils", 0)

        assert after_change_fossils - current_word_fossils == 1

        # Restore config path
        config.WORD_COUNTS_JSON = original_path

    print("INTEGRATION_TEST_COUNT_WORDS: Passed")


if __name__ == "__main__":
    integration_test_count_words()
    integration_test_summary()
