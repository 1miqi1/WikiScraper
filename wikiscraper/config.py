"""
Central configuration for the WikiScraper project.

Keep all paths and wiki-related constants here so the rest of the codebase
doesn't hardcode URLs or filesystem locations.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# --- Wiki settings (Bulbapedia) ---
BULBAPEDIA_MAIN_PAGE = "https://bulbapedia.bulbagarden.net/wiki/Main_Page"
WIKI_BASE_URL = "https://bulbapedia.bulbagarden.net/wiki/"
WIKI_ARTICLE_HREF_PREFIX = "/wiki/"  # used to recognize internal article links


# --- Project paths (repository root inferred from this file location) ---
# wikiscraper/config.py -> wikiscraper/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = REPO_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
WORD_COUNTS_JSON = DATA_DIR / "word-counts.json"

TESTS_DIR = REPO_ROOT / "tests"
TESTS_DATA_DIR = TESTS_DIR / "test_data"


# --- HTTP settings ---
DEFAULT_TIMEOUT_S = 15

BAD_PREFIXES = (
    "/wiki/Special:",
    "/wiki/Help:",
    "/wiki/Category:",
    "/wiki/File:",
    "/wiki/Template:",
)

BAD_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"
)

BAD_LINKS = (
    '/wiki/Main_Page'
    '/wiki/Main_Page'
    "/wiki/Bulbapedia:Editor's_Hub"
    '/wiki/Bulbapedia:FAQ'
    '/wiki/Bulbapedia:Copyrights'
    '/wiki/Bulbapedia:Privacy_policy'
    '/wiki/Bulbapedia:About'
    '/wiki/Bulbapedia:General_disclaimer'
)
