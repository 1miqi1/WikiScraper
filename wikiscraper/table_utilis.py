from __future__ import annotations

import json
import pandas as pd
from pathlib import Path
from typing import Any
from bs4 import BeautifulSoup

from . import config

def get_nth_table(html: str, n: int) -> pd.DataFrame:
    soup = BeautifulSoup(html, features="lxml")
    tables = soup.find_all("table")
    if n < 1 or n > len(tables):
        raise ValueError(f"There are {len(tables)} tabels on page, but you ask for table nr: #{n}.")
    return pd.read_html(str(tables[n - 1])[0])

def count_values(df: pd.DataFrame):
    occurences: dict
    
    for value in df.values.flatten():
        if pd.notna(value): 
            occurences[value] += 1
            
    out = pd.DataFrame(occurences)
    print(out)

def table(html: str, n: int, first_row_is_header: bool = False):
    df = get_nth_table(html=html, n=n)
    
    if first_row_is_header:
        df.columns = df.iloc[0]
    
    df = df[1:].reset_index(drop=True)
    
    df.to_csv('my_data.csv', index=False)
    
    count_values(df=df)
    
    