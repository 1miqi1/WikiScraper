"""Module: models.py

Provides the Page class for processing HTML content of wiki pages.
Includes methods for extracting summaries, tables, word counts, and links.

Classes:
    Page: Represents a wiki page and provides methods to interact with its content.

Usage Example:
    page = Page("Pikachu", html_content)
    page.summary()  # Print the first paragraph
    df = page.table(1, first_row_is_header=True)  # Extract first table
    words = page.count_words()  # Count words
    links = page.links()  # Get all wiki links
"""

import pandas as pd
from . import config
from bs4 import BeautifulSoup
import textwrap
import io
import json
from typing import Any
from pathlib import Path
from urllib.parse import unquote
import sys


class Page:
    """
    Represents a wiki page.

    Provides methods for:
        - Extracting the main content
        - Printing a summary paragraph
        - Extracting tables as DataFrames and saving them to CSV
        - Counting words and updating a JSON word count file
        - Extracting valid wiki links

    Attributes:
        phrase (str): The search phrase corresponding to the wiki page.
        html (str): The HTML content of the page.
    """

    def __init__(self, phrase: str, html: str):
        """
        Initialize the Page object.

        Args:
            phrase (str): Search phrase.
            html (str): HTML content of the page.
        """
        self.phrase = phrase
        self.html = html

    def get_content(self):
        """
        Extract the main content div from the HTML.

        Tries to select 'div.mw-content-ltr', falling back to '#mw-content-text'.

        Returns:
            BeautifulSoup tag or None: The main content of the page.
        """
        soup = BeautifulSoup(self.html, "lxml")
        return soup.select_one("div.mw-content-ltr") or soup.select_one("#mw-content-text")

    def summary(self) -> None:
        """
        Print the first non-empty paragraph of the page, wrapped at 150 characters.

        Iterates through all <p> tags in the content and prints the first paragraph
        containing text. If no content is found, prints an empty string.

        Returns:
            None
        """
        content = self.get_content()
        if not content:
            print("")
            return ""

        for p in content.find_all("p", recursive=True):
            text = p.get_text(" ", strip=True)
            if text:
                summary = "\n".join(textwrap.wrap(text, width=150))
                print(summary)
                return summary

        print("")
        return ""
    
    def is_real_table(self, table_tag) -> bool:
        """
        Determine if a BeautifulSoup <table> tag is likely a meaningful data table.

        Criteria:
            - Must have at least one <tr>
            - Must have at least one <td> or <th>
            - Ignore tables with common metadata or navigation classes (optional)

        Args:
            table_tag (bs4.element.Tag): The <table> tag to check.

        Returns:
            bool: True if the table is likely meaningful, False otherwise.
        """
        # Ignore tables with classes that are usually non-data
        bad_classes = (
            "navbox", "vertical-navbox", "infobox", "metadata", "toc", "sisterproject", "mbox"
        )
        if any(cls in table_tag.get("class", []) for cls in bad_classes):
            return False

        rows = table_tag.find_all("tr", recursive=True)
        if len(rows) < 2:
            return False

        # Check if at least one row has 2 or more cells
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                # Check if at least one cell has visible text
                if any(cell.get_text(strip=True) for cell in cells):
                    return True

        return False

    def table(self, n: int, output_dir: str = config.DATA_DIR, first_row_is_header: bool = False):
        """
        Extract the n-th table from the page, print it, save it to CSV, and
        count occurrences of each cell value.

        Args:
            n (int): Table index (1-based).
            output_dir (str | Path): Directory to save CSV file.
            first_row_is_header (bool): Treat first row as header if True.

        Returns:
            pd.DataFrame: The extracted table as a DataFrame.

        Raises:
            ValueError: If n is not within the number of tables found.
        """
        content = self.get_content()
        tables = content.find_all("table")

        if n < 1 or n > len(tables):
            raise ValueError(f"Znaleziono {len(tables)} tabel, a wybrano numer {n}.")

        cnt = 0
        target_table_html = None
        for table in tables:
            if not self.is_real_table(table):
                continue
            cnt += 1
            
            if cnt == n:
                target_table_html = str(table)
        
        if target_table_html is None:
            raise ValueError(f"Found {cnt} real tables, but chosen number {n}.")
        
        target_table_html = str(tables[n - 1])
        header = 0 if first_row_is_header else None
        dfs = pd.read_html(io.StringIO(target_table_html), header=header)

        if not dfs:
            return None
        df = dfs[0]

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ["_".join(str(level) for level in col if "Unnamed" not in str(level)) for col in df.columns]

        # Save CSV
        filename = f"{self.phrase}_{n}.csv"
        filepath = Path(output_dir) / filename
        df.to_csv(filepath, index=False)

        # Count occurrences
        all_values = df.to_numpy().flatten()
        all_values = [v for v in all_values if pd.notna(v)]
        counts = pd.Series(all_values).value_counts().reset_index()
        counts.columns = ['Wartość', 'Liczba wystąpień']
        print(counts.to_string(index=False))

        print(df)
        return df

    def count_words(self) -> list[str]:
        """
        Count words in the page and update the JSON file with cumulative counts.

        Only alphabetic words are counted. Updates or creates a JSON file defined
        in config.WORD_COUNTS_JSON with cumulative word counts across all pages.

        Returns:
            list[str]: List of words found in the page.
        """
        soup = BeautifulSoup(self.html, "lxml")
        text = soup.get_text(separator="\n")

        path = Path(config.WORD_COUNTS_JSON)

        if not path.exists():
            path.write_text("{}", encoding="utf-8")

        try:
            raw = path.read_text(encoding="utf-8").strip()
            data: dict[str, Any] = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {}

        words_found = []
        for word in text.split():
            if word.isalpha():
                data[word] = int(data.get(word, 0)) + 1
                words_found.append(word)

        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return words_found

    def links(self) -> list[str]:
        """
        Extract valid wiki links from the page.

        Filters out links based on prefixes, extensions, and a predefined list
        in config to avoid unwanted or external links.

        Returns:
            list[str]: List of linked phrases on the wiki page.
        """
        content = self.get_content()
        links = []
        for a in content.find_all('a', href=True):
            link = (a['href'])
            if not link.startswith("/wiki/"):
                continue
            if any(link.startswith(prefix) for prefix in config.BAD_PREFIXES):
                continue
            if any(link.endswith(ext) for ext in config.BAD_EXTENSIONS):
                continue
            if link in config.BAD_LINKS:
                continue
            links.append(link.removeprefix("/wiki/"))

        return list(set(links))
