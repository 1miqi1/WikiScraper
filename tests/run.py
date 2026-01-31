import pytest
import pandas as pd
from pathlib import Path
import json
from wikiscraper import Page
from wikiscraper import config
from bs4 import BeautifulSoup
from urllib.parse import unquote
from wikiscraper.scraper import Scraper

HERE = Path(__file__).parent

path = HERE / "test_data" / "team_rocket.html"
text = path.read_text(encoding="utf-8")
soup = BeautifulSoup(text, "lxml")

path = config.TESTS_DATA_DIR/"team_rocket.html"
text = path.read_text(encoding="utf-8")
soup = BeautifulSoup(text, "lxml")

page = Page(html=text, phrase="team_rocekt")
s = page.summary()
print(s)

print(page.links())

sc = Scraper(phrase="Team Rocket")
p = sc.scrape()
print(p.summary())

sc = Scraper(phrase=p.links()[100])
p = sc.scrape()
print(p.summary())


