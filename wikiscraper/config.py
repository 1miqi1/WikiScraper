"""
Central configuration for the WikiScraper project.

This module defines all paths, URLs, and constants used across the project,
so that other parts of the codebase do not hardcode file locations, wiki URLs,
or HTTP-related settings. Keeping these centralized makes the project easier
to maintain and update.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# --- Wiki settings (Bulbapedia) ---
BULBAPEDIA_MAIN_PAGE = "https://bulbapedia.bulbagarden.net/wiki/Main_Page"
"""str: URL of Bulbapedia's main page."""

WIKI_BASE_URL = "https://bulbapedia.bulbagarden.net/wiki/"
"""str: Base URL used to construct links to Bulbapedia articles."""

WIKI_ARTICLE_HREF_PREFIX = "/wiki/"
"""str: Prefix used to identify internal Bulbapedia article links."""


# --- Project paths (repository root inferred from this file location) ---
# wikiscraper/config.py -> wikiscraper/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
"""Path: Root directory of the repository, inferred from this config file."""

DATA_DIR = REPO_ROOT / "data"
"""Path: Directory for storing scraped data."""

CACHE_DIR = DATA_DIR / "cache"
"""Path: Directory for cached data to speed up repeated operations."""

WORD_COUNTS_JSON = DATA_DIR / "word-counts.json"
"""Path: JSON file storing computed word counts."""

TESTS_DIR = REPO_ROOT / "tests"
"""Path: Directory containing project tests."""

TESTS_DATA_DIR = TESTS_DIR / "test_data"
"""Path: Directory containing test-specific data files."""

MAX_CACHE_SIZE = 100
"""int: Maximum number of items to keep in cache."""


# --- HTTP settings ---
DEFAULT_TIMEOUT_S = 15
"""int: Default timeout (in seconds) for HTTP requests."""

BAD_PREFIXES = (
    "/wiki/Special:",
    "/wiki/Help:",
    "/wiki/Category:",
    "/wiki/File:",
    "/wiki/Template:",
    "/wiki/Bulbapedia:Projects",
    "/wiki/Bulbapedia:"
)
"""tuple[str]: URL prefixes of links to ignore when scraping articles."""

BAD_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"
)
"""tuple[str]: File extensions to ignore when processing links."""

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
"""tuple[str]: Specific article links to skip during scraping."""
