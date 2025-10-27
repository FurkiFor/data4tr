"""
data4tr - Text Normalization Module
Türkçe metinleri normalize eden ve dil kurallarına uygun hale getiren modül.
"""

import re
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextNormalizer:
    """Türkçe metin normalizasyon sınıfı"""

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Boşlukları normalize et"""
        if not text:
            return ""

        # Çoklu boşlukları tek boşluğa çevir
        text = re.sub(r" +", " ", text)

        # Satır başı ve sonundaki boşlukları temizle
        text = re.sub(r"^ +| +$", "", text, flags=re.MULTILINE)

        # Çoklu satır sonlarını normalize et
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @staticmethod
    def fix_turkish_quotes(text: str) -> str:
        """İngilizce tırnakları Türkçe tırnaklara çevir"""
        if not text:
            return ""

        # Basit tırnak düzeltmesi
        replacements = {
            '"': "\u201c",  # Açılış tırnağı
            '"': "\u201d",  # Kapanış tırnağı
            "'": "\u2018",  # Tek tırnak açılış
            "'": "\u2019",  # Tek tırnak kapanış
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    @staticmethod
    def fix_punctuation_spacing(text: str) -> str:
        """Noktalama işaretlerinden önce/sonra boşluk düzeltmesi"""
        if not text:
            return ""

        # Noktalama işaretlerinden önceki boşlukları kaldır
        text = re.sub(r" +([.,;:!?])", r"\1", text)

        # Noktalama işaretlerinden sonraki boşlukları ayarla
        text = re.sub(r"([.,;:!?])(?! )", r"\1 ", text)

        # Parantezler için boşluk ayarla
        text = re.sub(r" \((\w)", r" (\1", text)
        text = re.sub(r"(\w)\) ", r"\1) ", text)

        return text

    @staticmethod
    def normalize_turkish_chars(text: str) -> str:
        """Türkçe karakterleri normalize et"""
        if not text:
            return ""

        # Karakter düzeltmeleri
        char_map = {
            "Î": "İ",
            "î": "ı",
            "I": "I",  # İngilizce büyük I
        }

        for old, new in char_map.items():
            text = text.replace(old, new)

        return text

    @staticmethod
    def fix_common_mistakes(text: str) -> str:
        """Yaygın yazım hatalarını düzelt"""
        if not text:
            return ""

        mistakes = {
            # Kelime başında hatalı İ/ı kullanımı
            r"\bıntemet\b": "internet",
            r"\bımza\b": "imza",
            r"\bItırbul\b": "İstanbul",
        }

        for pattern, replacement in mistakes.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text

    @staticmethod
    def normalize(text: str) -> str:
        """Tüm normalizasyon işlemlerini uygula"""
        if not text:
            return ""

        text = TextNormalizer.normalize_turkish_chars(text)
        text = TextNormalizer.fix_common_mistakes(text)
        text = TextNormalizer.fix_turkish_quotes(text)
        text = TextNormalizer.fix_punctuation_spacing(text)
        text = TextNormalizer.normalize_whitespace(text)

        return text


def normalize_batch(texts: List[str]) -> List[str]:
    """
    Birden fazla metni toplu olarak normalize et

    Args:
        texts: Normalize edilecek metinler listesi

    Returns:
        Normalize edilmiş metinler listesi
    """
    normalizer = TextNormalizer()
    return [normalizer.normalize(text) for text in texts]


def main():
    """Test ve örnek kullanım"""
    normalizer = TextNormalizer()

    test_texts = [
        "Bu   metinde    cok   bosluk    var...",
        "Turkce'de noktalama isaretleri onemli !",
        "Istanbul'un tarihi cok zengindir.",
        'Ingiliz " ve Turkce " tirnaklar karismis.',
    ]

    print("Metin Normalizasyon Testi\n" + "=" * 50)

    for text in test_texts:
        normalized = normalizer.normalize(text)
        print(f"\nOrijinal: {text}")
        print(f"Normalize: {normalized}")


if __name__ == "__main__":
    main()
