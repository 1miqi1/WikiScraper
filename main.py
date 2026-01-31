"""
Run all WikiScraper functionalities in a batch, simulating CLI usage.

This script iterates through multiple command/argument combinations:
- summary
- count_words
- table (with multiple table numbers)
- analyze_relative_word_frequency (with chart)
- auto_count_words
"""

from wikiscraper.controller import Controller
from wikiscraper.parser import Parser
import time

# Define all test cases
test_cases = [
    # Summaries
    ["summary", "Team Rocket"],
    ["summary", "Pikachu"],

    # Word counts
    ["count_words", "Pikachu"],
    ["count_words", "Bulbasaur"],

    # Table extraction (example with multiple table numbers)
    ["table", "Squirtle", "--number", "1", "--first-row-is-header"],
    ["table", "Squirtle", "--number", "2"],
    ["table", "Squirtle", "--number", "3"],
    ["table", "Squirtle", "--number", "4"],

    # Analyze relative word frequency
    ["analyze_relative_word_frequency", "--mode", "article", "--count", "5", "--chart", "chart_article.png"],
    ["analyze_relative_word_frequency", "--mode", "language", "--count", "5", "--chart", "chart_language.png"],

    # Auto-count words starting from a phrase
    ["auto_count_words", "Team Rocket", "--depth", "1", "--wait", "0"],
]

# Initialize parser and controller
pr = Parser()
cl = Controller()

# Run each test case
for case in test_cases:
    print(f"\n--- Running CLI case: {case} ---")
    args = pr.parser.parse_args(case)
    print(f"Parsed arguments: {args}")
    cl.run_func(args)
    time.sleep(0.2)  # short delay between cases
