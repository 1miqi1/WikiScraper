"""Module: models.py"""

import pandas as pd
from . import config
from bs4 import BeautifulSoup
import textwrap
import io
import json
from typing import Any
from pathlib import Path
from urllib.parse import unquote

class Page():
    def __init__(self, phrase: str, html: str):
        self.phrase = phrase
        self.html = html
    
    def get_content(self):
        soup = BeautifulSoup(self.html, "lxml")
        return soup.select_one("div.mw-content-ltr") or soup.select_one("#mw-content-text")
    
    def summary(self):

        # Try to find main content
        content = self.get_content()

        if not content:
            print("")
            return ""

        # Find the first non-empty paragraph
        for p in content.find_all("p", recursive=True):
            text = p.get_text(" ", strip=True)  # Get paragraph text as a single string
            if text:
                # Wrap text at 40 characters per line
                return str("\n".join(textwrap.wrap(text, width=150)))

        # Fallback if no paragraph found
        print("")
        return ""

    def table(self, n: int, output_dir: str = config.DATA_DIR, first_row_is_header: bool = False):
        content = self.get_content()
        tables = content.find_all("table")

        if n < 1 or n > len(tables):
            raise ValueError(f"Znaleziono {len(tables)} tabel, a wybrano numer {n}.")

        target_table_html = str(tables[n - 1])
        
        # Nagłówek: pandas automatycznie obsłuży <th> jeśli header=0
        header = 0 if first_row_is_header else None
        
        # Wczytanie do DataFrame (używamy StringIO, aby uniknąć ostrzeżeń o surowym HTML)
        dfs = pd.read_html(io.StringIO(target_table_html), header=header)
        
        if not dfs:
            return None
        df = dfs[0]
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ["_".join(str(level) for level in col if "Unnamed" not in str(level)) for col in df.columns]

        # 1. Zapis do CSV (nazwa pliku to fraza wyszukiwania)
        print(df)
        filename = f"{self.phrase}_{n}.csv"
        filepath = output_dir / filename
        df.to_csv(filepath, index=False)

        # stack() zamienia tabelę w jedną długą kolumnę danych, co ułatwia liczenie
        all_values = df.to_numpy().flatten()
        # Usuwamy wartości NaN (puste komórki)
        all_values = [v for v in all_values if pd.notna(v)]

        # Tworzymy prosty DataFrame z wynikami
        counts = pd.Series(all_values).value_counts().reset_index()
        counts.columns = ['Wartość', 'Liczba wystąpień']

        print(counts.to_string(index=False))

        return df
    
    def count_words(self) -> list[str]:
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

        for word in text.split():
            data[word] = int(data.get(word, 0)) + 1
            
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def links(self):
        content = self.get_content()
        links = []
        for a in content.find_all('a', href =True):
            link = unquote(a['href'])
            if not link.startswith("/wiki/"):
                continue
            if link.startswith(config.BAD_PREFIXES):
                continue
            if link.endswith(config.BAD_EXTENSIONS):
                continue
            if link in config.BAD_LINKS:
                continue
            
            links.append(link.split('/')[-1])
        
        links = list(set(link))
        return links
        

    
        