from wikiscraper.controller import Controller
from wikiscraper.parser import Parser
import time

test_cases = [
    ["summary", "Team Rocket"],
    ["count_words", "Pikachu"],
    ["table", "Squirtle", "-n", "4"],
    ["analyze_relative_word_frequency", "--mode", "article", "--count", "10", "--chart", "chart.png"],
    ["auto_count_words", "Charmander", "--depth", "1", "--wait", "0"],
]

pr = Parser()
cl = Controller()

for case in test_cases:
    print(f"\nTesting: {case}")
    args = pr.parser.parse_args(case)
    print(args)
    cl.run_func(args)
    time.sleep(0.3)