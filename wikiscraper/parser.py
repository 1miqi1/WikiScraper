"""Module: cli.py"""
import argparse


class Parser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Wiki scraper CLI")
        subparsers = self.parser.add_subparsers(dest="command", required=True)

        # ---------------- summary ----------------
        summary = subparsers.add_parser("summary", help="Summary of an article")
        summary.add_argument("phrase", help="Phrase to look for", required=True)

        # ---------------- count_words ----------------
        count_words = subparsers.add_parser("count_words", help="Counting words in an article")
        count_words.add_argument("phrase", help="Phrase to look for", required=True)

        # ---------------- table ----------------
        table = subparsers.add_parser("table", help="Finding n-th table in an article")
        table.add_argument("phrase", help="Phrase to look for", required=True)
        table.add_argument("--number", "-n", help="Number of a table", type=int, required=True)
        table.add_argument(
            "--first-row-is-header",
            help="If true, first row of the table is a header",
            action="store_true"
        )

        # ---------------- analyze_relative_word_freq ----------------
        analyze = subparsers.add_parser(
            "analyze_relative_word_freq",
            help="Analyzing relative word frequency"
        )
        analyze.add_argument("phrase", help="Phrase to look for", required=True)
        analyze.add_argument(
            "--mode",
            choices=["article", "language"],
            help="Sort according to occurrences in article/language",
            required=True
        )

        # positive integer validator
        def positive_int(value):
            value = int(value)
            if value <= 0:
                raise argparse.ArgumentTypeError(f"{value} is not > 0")
            return value

        analyze.add_argument(
            "--count",
            help="How many words will be displayed",
            type=positive_int,
            required=True
        )
        analyze.add_argument("--chart", help="Optional path to save chart")

        # ---------------- auto_count_words ----------------
        auto_count_words = subparsers.add_parser(
            "auto_count_words",
            help="Auto count words search"
        )
        auto_count_words.add_argument("phrase", help="Phrase to look for", required=True)
        auto_count_words.add_argument("--depth", help="Depth of search", type=int, required=True)
        auto_count_words.add_argument("--wait", help="Delay between searches in seconds", type=int, required=True)
    
    def parse_args(self):
        return self.parser.parse_args()        
        
        
            