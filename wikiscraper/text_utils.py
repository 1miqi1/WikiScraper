"""Module: text_utils.py"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import config


def _path() -> Path:
    return Path(config.WORD_COUNTS_JSON)


def add_json() -> None:
    path = _path()
    path.write_text("{}", encoding="utf-8")


def clear_json() -> None:
    add_json()


def convert_to_text(html: str) -> str:
    pass

def count_words(text: str):
    path = _path()

    if not path.exists():
        add_json()

    try:
        raw = path.read_text(encoding="utf-8").strip()
        data: dict[str, Any] = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        data = {}

    for word in text.split():
        data[word] = int(data.get(word, 0)) + 1
        
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
