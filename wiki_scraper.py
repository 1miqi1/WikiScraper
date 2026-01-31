"""Stub: wiki_scraper.py"""
from wikiscraper import config
from wikiscraper.controller import Controller
from wikiscraper.parser import Parser
import time

pr = Parser()
cl = Controller()
cl.run_func(pr.parse_args())