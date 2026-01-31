"""Module: cache.py"""
from .config import CACHE_DIR
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

def safe_name(phrase: str) -> str:
    name = phrase.strip().replace("/", "_").replace("\\", "_")
    name = name.replace("..", "_")
    if not name:
        raise ValueError("Empty cache key/phrase.")
    if not name.lower().endswith(".html"):
        name += ".html"
    return name

def load(phrase: str, html: str) -> None:
    path = CACHE_DIR / safe_name(phrase)
    soup = BeautifulSoup(html, "html.parser")
    preet_html = soup.prettify()
    path.write_text(preet_html, encoding="utf-8")

def get(phrase: str) -> str | None:
    path = CACHE_DIR / safe_name(phrase)
    if not path.exists():
        raise FileNotFoundError(f"Cache miss for phrase={phrase!r} (expected: {path})")
    return path.read_text(encoding="utf-8")

def clear_cache(self):
    for item in CACHE_DIR.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)