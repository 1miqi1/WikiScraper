"""
Module: parser.py

This module provides a command-line interface (CLI) parser for the Wiki scraper.
It defines the `Parser` class, which sets up all supported commands and options
using argparse.

Supported commands:
    - summary: Get a summary of a wiki article.
    - count_words: Count words in a wiki article.
    - table: Find the n-th table in a wiki article.
    - analyze_relative_word_frequency: Analyze relative word frequency in an article or language.
    - auto_count_words: Automatically count words in articles up to a given depth.

Usage Example:
    parser = Parser()
    args = parser.parse_args()
    if args.command == "summary":
        print(f"Getting summary for {args.phrase}")
"""

import argparse


class Parser:
    """
    Command-line argument parser for the Wiki scraper CLI.

    Attributes:
        parser (argparse.ArgumentParser): The main argument parser.
    """

    def __init__(self):
        """Initialize the CLI parser and define all subcommands and arguments."""
        self.parser = argparse.ArgumentParser(description="Wiki scraper CLI")
        subparsers = self.parser.add_subparsers(dest="command")

        # ---------------- summary ----------------
        summary = subparsers.add_parser("summary", help="Summary of an article")
        summary.add_argument("phrase", help="Phrase to look for")

        # ---------------- count_words ----------------
        count_words = subparsers.add_parser(
            "count_words", help="Counting words in an article"
        )
        count_words.add_argument("phrase", help="Phrase to look for")

        # ---------------- table ----------------
        table = subparsers.add_parser(
            "table", help="Finding n-th table in an article"
        )
        table.add_argument("phrase", help="Phrase to look for")
        table.add_argument(
            "--number", "-n", help="Number of a table", type=int, required=True
        )
        table.add_argument(
            "--first-row-is-header",
            help="If true, first row of the table is a header",
            action="store_true",
        )

        # ---------------- analyze_relative_word_frequency ----------------
        analyze = subparsers.add_parser(
            "analyze_relative_word_frequency",
            help="Analyzing relative word frequency",
        )
        analyze.add_argument(
            "--mode",
            choices=["article", "language"],
            help="Sort according to occurrences in article/language",
            required=True,
        )

        # Positive integer validator
        def positive_int(value):
            value = int(value)
            if value <= 0:
                raise argparse.ArgumentTypeError(f"{value} is not > 0")
            return value

        analyze.add_argument(
            "--count",
            help="How many words will be displayed",
            type=positive_int,
            required=True,
        )
        analyze.add_argument(
            "--chart", help="Optional path to save chart"
        )

        # ---------------- auto_count_words ----------------
        auto_count_words = subparsers.add_parser(
            "auto_count_words", help="Auto count words search"
        )
        auto_count_words.add_argument("phrase", help="Phrase to look for")
        auto_count_words.add_argument(
            "--depth", help="Depth of search", type=int, required=True
        )
        auto_count_words.add_argument(
            "--wait", help="Delay between searches in seconds", type=float, required=True
        )

    def parse_args(self):
        """
        Parse the command-line arguments.

        Returns:
            argparse.Namespace: The parsed arguments as a namespace object.
        """
        return self.parser.parse_args()
