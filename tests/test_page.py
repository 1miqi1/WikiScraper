# test_models.py
import pytest
import pandas as pd
from pathlib import Path
import json
from wikiscraper import Page
from wikiscraper.config import WORD_COUNTS_JSON

# Make sure the JSON file path for word counts is isolated for testing
HERE = Path(__file__).parent

@pytest.fixture
def html_team_rocket():
    path = HERE / "test_data" / "team_rocket.html"
    return path.read_text(encoding="utf-8")

@pytest.fixture
def html_type():
    path = HERE / "test_data" / "type.html"
    return path.read_text(encoding="utf-8")

def test_summary_returns_text(html_team_rocket):
    page = Page(phrase="team_rocket", html=html_team_rocket)
    text = page.summary()
    assert isinstance(text, str)
    assert len(text) > 0  # There should be some text

def test_table_creates_dataframe_and_csv(html_type):
    page = Page(phrase="type", html=html_type)
    csv_path =  Path("type.csv")
    df = page.table(n=2, first_row_is_header=True)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert csv_path.exists()  # CSV should be saved

def test_count_words_creates_json(html_team_rocket):
    # Override the config path
    path = Path(WORD_COUNTS_JSON)
    page = Page(phrase="team_rocket", html=html_team_rocket)
    page.count_words()

    assert path.exists()
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    
    assert isinstance(data, dict)
    # There should be at least one word counted
    assert len(data) > 0
