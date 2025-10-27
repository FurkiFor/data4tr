"""
data4tr - Text Cleaner Module
HTML, karakter ve boşluk temizliği yapan modül.
"""

import re
import html
from typing import List, Optional


class TextCleaner:
    """Metin temizleme ve normalleştirme sınıfı"""

    @staticmethod
    def clean_html(text: str) -> str:
        """HTML etiketlerini temizle"""
        if not text:
            return ""

        # HTML decode
        text = html.unescape(text)

        # HTML etiketlerini kaldır
        text = re.sub(r"<[^>]+>", "", text)

        return text.strip()

    @staticmethod
    def clean_whitespace(text: str) -> str:
        """Gereksiz boşlukları temizle"""
        if not text:
            return ""

        # Çoklu boşlukları tek boşluğa çevir
        text = re.sub(r"\s+", " ", text)

        # Satır sonlarını normalize et
        text = re.sub(r"\n+", "\n", text)

        return text.strip()

    @staticmethod
    def remove_special_chars(text: str, keep_newlines: bool = True) -> str:
        """Özel karakterleri temizle (Türkçe karakterleri koru)"""
        if not text:
            return ""

        # Türkçe karakterleri koru
        # a-z, A-Z, 0-9, Türkçe karakterler, noktalama ve boşluk
        pattern = (
            r"[^a-zA-Z0-9çğıöşüÇĞIİÖŞÜ\s.,;:!?()\[\]{}'\"-]"
            if keep_newlines
            else r"[^a-zA-Z0-9çğıöşüÇĞIİÖŞÜ .,;:!?()\[\]{}'\"-]"
        )

        text = re.sub(pattern, "", text)

        return text

    @staticmethod
    def remove_urls(text: str) -> str:
        """URL'leri kaldır"""
        if not text:
            return ""

        url_pattern = (
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        )
        text = re.sub(url_pattern, "", text)

        return text.strip()

    @staticmethod
    def destructive_clean(text: str) -> str:
        """Kapsamlı temizlik (tüm işlemler)"""
        if not text:
            return ""

        text = TextCleaner.remove_urls(text)
        text = TextCleaner.clean_html(text)
        text = TextCleaner.remove_special_chars(text)
        text = TextCleaner.clean_whitespace(text)

        # Çok kısa cümleleri ve tekrar eden karakterleri temizle
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # Tekrar eden karakterleri kontrol et (örn: "aaa" -> "aa")
            line = re.sub(r"(.)\1{3,}", r"\1\1", line)

            if len(line) > 10:  # En az 10 karakterlik cümleler
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    @staticmethod
    def preprocess_for_ai(text: str) -> str:
        """AI işleme için optimizasyon"""
        if not text:
            return ""

        # URL'leri kaldır
        text = TextCleaner.remove_urls(text)

        # HTML temizliği
        text = TextCleaner.clean_html(text)

        # Boşluk normalize
        text = TextCleaner.clean_whitespace(text)

        # Paragrafları ayır (boş satırlarla)
        text = re.sub(r"\n\n+", "\n\n", text)

        return text.strip()


def main():
    """Test ve örnek kullanım"""
    dirty_text = """
    <html>
    <p>Bu bir <b>örnek</b> metindir. http://example.com link var.</p>
    <p>Çoklu     boşluk    ve    gereksiz       karakterler!!!</p>
    </html>
    """

    print("Orijinal metin:")
    print(repr(dirty_text))
    print("\n" + "=" * 50)

    cleaner = TextCleaner()
    cleaned = cleaner.destructive_clean(dirty_text)

    print("\nTemizlenmiş metin:")
    print(cleaned)
    print("\n" + "=" * 50)
    print(f"\nKarakter sayısı: {len(dirty_text)} -> {len(cleaned)}")


if __name__ == "__main__":
    main()
