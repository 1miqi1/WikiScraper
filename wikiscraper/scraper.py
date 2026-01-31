"""Module: scraper.py"""

from wikiscraper import config
from wikiscraper.page import Page
from urllib.parse import urljoin
import requests
import sys
import os

class Scraper():
    def __init__(self, phrase: str, wiki_base_url: str = config.BULBAPEDIA_MAIN_PAGE, use_local_html_file_instead=False):
        self.phrase = phrase
        self.wiki_base_url = wiki_base_url
        self.use_local_html_file_instead = use_local_html_file_instead
    
    def scrape(self) -> Page:
        path = config.CACHE_DIR/f"{self.phrase}.html"
        
        if not self.use_local_html_file_instead :  
            url = urljoin(self.wiki_base_url, self.phrase)
            r = requests.get(url)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)
            else:
                print("Failed to fetch page:", r.status_code)
                sys.exit(1)
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return Page(phrase=self.phrase, html=f.read())
        else:
            print("Failed to download html file contents")
            sys.exit(1)
        
        
                