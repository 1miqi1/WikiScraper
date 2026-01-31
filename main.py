from wikiscraper.controller import Controller
from wikiscraper.parser import Parser

pr = Parser()
args = pr.parse_args()
cl = Controller
cl.run_func(args)