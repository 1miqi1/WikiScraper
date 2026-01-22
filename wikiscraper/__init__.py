# wikiscraper/__init__.py
from . import config, text_utils
from .scraper import Scraper
from .controller import Controller
from .models import Page

__all__ = ["config", "text_utils", "Scraper", "Controller", "Page"]
__version__ = "0.1.0"
