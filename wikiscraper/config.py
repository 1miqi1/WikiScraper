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

CACHE_DIR = REPO_ROOT / "cache"
WORD_COUNTS_JSON = REPO_ROOT / "word-counts.json"

TESTS_DIR = REPO_ROOT / "tests"
TESTS_DATA_DIR = TESTS_DIR / "data"

# Example integration-test HTML (you can change name if needed)
TEAM_ROCKET_HTML = TESTS_DATA_DIR / "team_rocket.html"


# --- HTTP settings ---
DEFAULT_TIMEOUT_S = 15


@dataclass(frozen=True)
class AppConfig:
    """Optional structured config object (useful for passing around)."""

    wiki_base_url: str = WIKI_BASE_URL
    article_href_prefix: str = WIKI_ARTICLE_HREF_PREFIX

    cache_dir: Path = CACHE_DIR
    word_counts_json: Path = WORD_COUNTS_JSON

    timeout_s: int = DEFAULT_TIMEOUT_S
