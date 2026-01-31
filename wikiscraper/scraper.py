"""
Module: scraper.py

This module provides a `Scraper` class for fetching and caching HTML content
from a wiki page (defaulting to Bulbapedia). It can either download the page
from the internet or read it from a local cached HTML file.

Classes:
    Scraper: Handles constructing the page URL, downloading or reading the page,
             and returning a `Page` object containing the HTML content.

Usage Example:
    scraper = Scraper("Pikachu")
    page = scraper.scrape()
    print(page.html)  # Access the raw HTML content of the page
"""

import os
import re
import sys
from urllib.parse import unquote, urljoin

import requests
from wikiscraper import config
from wikiscraper.page import Page


class Scraper:
    """
    A scraper for fetching wiki pages and caching them locally.

    Attributes:
        phrase (str): The sanitized phrase used for file naming and page lookup.
        wiki_base_url (str): Base URL of the wiki to fetch pages from.
        use_local_html_file_instead (bool): Whether to skip downloading and use
            the local cached HTML file.
    """

    def __init__(
        self,
        phrase: str = None,
        wiki_base_url: str = config.BULBAPEDIA_MAIN_PAGE,
        use_local_html_file_instead: bool = False,
    ):
        """
        Initialize a Scraper instance.

        Args:
            phrase (str): The page name or phrase to fetch. Can include an anchor
                (e.g., 'Pikachu#Abilities').
            wiki_base_url (str, optional): The base URL of the wiki. Defaults to
                Bulbapedia's main page.
            use_local_html_file_instead (bool, optional): If True, skip downloading
                the page and use cached HTML.
        """
        if "#" in phrase:
            page_name, _ = phrase.split("#", 1)
        else:
            page_name, _ = phrase, None

        self.url = urljoin(wiki_base_url, page_name)

        title = unquote(phrase).replace(" ", "_")
        title = title.replace("/", "-")
        # replace forbidden filesystem characters with "_"
        self.title = re.sub(r'[\\/*?:"<>|#]', "_", title)

        self.use_local_html_file_instead = use_local_html_file_instead

    def scrape(self) -> Page:
        """
        Fetch the wiki page and return it as a Page object.

        This method will either:
            - Download the HTML content from the wiki and cache it locally, or
            - Read the HTML from a local cached file if
              `use_local_html_file_instead` is True.

        Returns:
            Page: A Page object containing the HTML content of the page.
                  Returns None if the page does not exist (HTTP 404).

        Raises:
            SystemExit: If the HTML file cannot be downloaded or read locally.
        """
        path = config.CACHE_DIR / f"{self.title}.html"

        if not self.use_local_html_file_instead:
            r = requests.get(self.url)
            if r.status_code == 200:
                num_files = len(os.listdir(config.CACHE_DIR))
                if num_files < config.MAX_CACHE_SIZE:
                    with open(path, "wb") as f:
                        f.write(r.content)
                else:
                    return Page(phrase=self.title, html=r.content)
            else:
                print(f"Cannot download contents from page: {r.status_code}")
                sys.exit(1)

        if os.path.exists(path):
            with open(path, "r") as f:
                return Page(phrase=self.title, html=f.read())
        else:
            print("Failed to download HTML file contents")
            sys.exit(1)
