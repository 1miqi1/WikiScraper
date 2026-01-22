from pathlib import Path
from wikiscraper import cache

def test_cache():

    content = Path("tests/data/test.html").read_text(encoding="utf-8")

    cache.load("test", content)
    assert cache.get("test") != ""

    cache.clear_cache()

    num_files = sum(1 for p in cache.cache_path.iterdir() if p.is_file())
    assert num_files == 0
    
    cache.load("test", content)
    assert cache.get("test") != ""

