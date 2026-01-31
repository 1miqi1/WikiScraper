from wikiscraper.controller import Controller
from wikiscraper.parser import Parser
import time

test_cases = [
    ["summary", "Team Rocket"],
    ["count_words", "Pikachu"],
    ["table", "Squirtle", "-n", "1"],
    ["table", "Squirtle", "-n", "2"],
    ["table", "Squirtle", "-n", "3"],
    ["table", "Squirtle", "-n", "4"],
    ["table", "Squirtle", "-n", "5"],
    ["table", "Squirtle", "-n", "6"],
    ["table", "Squirtle", "-n", "7"],
    ["table", "Squirtle", "-n", "8"],
    ["analyze_relative_word_frequency", "--mode", "article", "--count", "10", "--chart", "chart.png"],
]

pr = Parser()
cl = Controller()

for case in test_cases:
    print(f"\nTesting: {case}")
    args = pr.parser.parse_args(case)
    print(args)
    cl.run_func(args)
    time.sleep(0.3)