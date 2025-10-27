"""
data4tr - Cleaner Test
Metin temizleme fonksiyonları için testler
"""

import pytest
from scraper.cleaner import TextCleaner


class TestTextCleaner:
    """TextCleaner sınıfı için testler"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.cleaner = TextCleaner()
    
    def test_clean_html(self):
        """HTML temizleme testi"""
        dirty_text = "<html><p>Test</p></html>"
        cleaned = self.cleaner.clean_html(dirty_text)
        assert "<html>" not in cleaned
        assert "<p>" not in cleaned
    
    def test_clean_whitespace(self):
        """Boşluk temizleme testi"""
        dirty_text = "Çok   boşluk    var."
        cleaned = self.cleaner.clean_whitespace(dirty_text)
        assert "  " not in cleaned
    
    def test_remove_urls(self):
        """URL kaldırma testi"""
        text_with_url = "Bu bir link: https://example.com/test"
        cleaned = self.cleaner.remove_urls(text_with_url)
        assert "https://" not in cleaned
    
    def test_remove_special_chars(self):
        """Özel karakter kaldırma testi"""
        text = "Türkçe karakterler: çğıöşü ÇĞIİÖŞÜ"
        cleaned = self.cleaner.remove_special_chars(text)
        assert "ç" in cleaned  # Türkçe karakterler korunmalı
    
    def test_destructive_clean(self):
        """Kapsamlı temizlik testi"""
        dirty_text = "<html>Test   metin   https://example.com</html>"
        cleaned = self.cleaner.destructive_clean(dirty_text)
        assert "<html>" not in cleaned
        assert "  " not in cleaned
        assert "https://" not in cleaned


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

