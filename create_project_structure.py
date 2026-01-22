#!/usr/bin/env python3
"""
Create the WikiScraper project structure in the CURRENT directory.

Usage:
  python create_project_structure.py

This script:
- creates directories and placeholder files only if they don't exist
- does NOT overwrite existing files
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(".")  # current directory

ROOT_FILES = [
    "wiki_scraper.py",
    "requirements.txt",
    "word-counts.json",
    "analysis.ipynb",
    "wiki_scraper_integration_test.py",  # optional, created as stub
]

PKG_DIR = ROOT / "wikiscraper"
PKG_FILES = [
    "__init__.py",
    "cli.py",
    "controller.py",
    "scraper.py",
    "html_parser.py",
    "cache.py",
    "models.py",
    "text_utils.py",
    "output.py",
    "analyze.py",
]

CACHE_DIR = ROOT / "cache"

TESTS_DIR = ROOT / "tests"
TESTS_DATA_DIR = TESTS_DIR / "data"
TESTS_FILES = [
    "wiki_scraper_integration_test.py",
    "test_unit_example_1.py",
    "test_unit_example_2.py",
    "test_unit_example_3.py",
    "test_unit_example_4.py",
]
TEST_DATA_FILES = [
    "team_rocket.html",
]


def safe_touch(path: Path, content: str = "") -> None:
    """Create a file if it doesn't exist. Do not overwrite."""
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    # Root files
    for fname in ROOT_FILES:
        fpath = ROOT / fname
        if fname.endswith(".py"):
            safe_touch(fpath, content=f'"""Stub: {fname}"""\n')
        elif fname.endswith(".json"):
            safe_touch(fpath, content="{}\n")
        else:
            safe_touch(fpath, content="")

    # Package directory
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    for fname in PKG_FILES:
        fpath = PKG_DIR / fname
        if fname == "__init__.py":
            safe_touch(fpath, content='"""WikiScraper package."""\n')
        else:
            safe_touch(fpath, content=f'"""Module: {fname}"""\n')

    # Cache directory (and .gitkeep so it can exist in git if you want)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe_touch(CACHE_DIR / ".gitkeep", content="")

    # Tests directory + data
    TESTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for fname in TESTS_FILES:
        safe_touch(TESTS_DIR / fname, content=f'"""Stub test file: {fname}"""\n')

    for fname in TEST_DATA_FILES:
        safe_touch(TESTS_DATA_DIR / fname, content="<!-- Paste saved HTML here -->\n")

    print("✅ Project structure created in:", Path.cwd())
    print("Note: Existing files were not overwritten.")


if __name__ == "__main__":
    main()
