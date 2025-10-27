"""
data4tr - Scraper Module
Web'den Türkçe veri toplama modülü.
"""

from .scraper import Scraper
from .cleaner import TextCleaner

__all__ = ['Scraper', 'TextCleaner']

