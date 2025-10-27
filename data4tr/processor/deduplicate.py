"""
data4tr - Deduplication Module
Yinelenen metinleri tespit eden ve temizleyen modül.
"""

import hashlib
import logging
from typing import List, Dict, Set, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Deduplicator:
    """Tekrar eden içerikleri tespit ve temizleme sınıfı"""

    def __init__(self):
        self.seen_hashes: Set[str] = set()

    def generate_hash(self, text: str) -> str:
        """Metinden hash oluştur"""
        # Metni normalize et (küçük harf, boşluk temizliği)
        normalized = text.lower().strip()
        normalized = " ".join(normalized.split())

        # MD5 hash
        return hashlib.md5(normalized.encode("utf-8")).hexdigest()

    def is_duplicate(self, text: str) -> bool:
        """Metin daha önce görüldü mü kontrol et"""
        text_hash = self.generate_hash(text)

        if text_hash in self.seen_hashes:
            return True

        self.seen_hashes.add(text_hash)
        return False

    def find_duplicates(self, texts: List[str]) -> List[int]:
        """
        Tekrar eden metinlerin indekslerini bul

        Args:
            texts: Kontrol edilecek metinler listesi

        Returns:
            Duplicate olan metinlerin indeksleri
        """
        duplicate_indices = []
        self.seen_hashes.clear()

        for idx, text in enumerate(texts):
            if self.is_duplicate(text):
                duplicate_indices.append(idx)

        return duplicate_indices

    def remove_duplicates(self, data: List[Dict]) -> List[Dict]:
        """
        Veri setinden duplicate kayıtları kaldır

        Args:
            data: Kayıtların listesi (her kayıt 'text' alanına sahip olmalı)

        Returns:
            Duplicate'leri temizlenmiş kayıt listesi
        """
        self.seen_hashes.clear()
        unique_data = []
        removed_count = 0

        for record in data:
            if "text" not in record:
                continue

            text = record["text"]
            if not self.is_duplicate(text):
                unique_data.append(record)
            else:
                removed_count += 1

        logger.info(f"{removed_count} duplicate kayıt temizlendi")
        return unique_data

    def find_similar(self, text: str, threshold: float = 0.8) -> List[Tuple[int, float]]:
        """
        Benzer metinleri bul (basit implementation)

        Args:
            text: Karşılaştırılacak metin
            threshold: Benzerlik eşiği (0-1 arası)

        Returns:
            (indeks, benzerlik skoru) çiftleri listesi
        """
        # Bu fonksiyon ileride daha gelişmiş algoritmalarla implement edilebilir
        # Şimdilik sadece exact match kontrolü yapıyoruz
        similarities = []

        for hash_val in self.seen_hashes:
            # Simplified similarity check
            # Gerçek implementasyon için Jaccard similarity veya embedding'ler kullanılabilir
            pass

        return similarities


def remove_exact_duplicates(data: List[Dict]) -> List[Dict]:
    """
    Veri setinden exact duplicate'leri kaldır (basit API)

    Args:
        data: Kayıtların listesi

    Returns:
        Temizlenmiş kayıt listesi
    """
    deduplicator = Deduplicator()
    return deduplicator.remove_duplicates(data)


def main():
    """Test ve örnek kullanım"""
    deduplicator = Deduplicator()

    test_data = [
        {"id": "1", "text": "Bu bir test metnidir."},
        {"id": "2", "text": "Bu başka bir metindir."},
        {"id": "3", "text": "Bu bir test metnidir."},  # Duplicate
        {"id": "4", "text": "Farklı içerik burada."},
        {"id": "5", "text": "BU BİR TEST METNİDİR."},  # Case farklı ama duplicate
    ]

    print("Duplicate Tespiti Testi\n" + "=" * 50)
    print(f"Orijinal kayıt sayısı: {len(test_data)}")

    cleaned = deduplicator.remove_duplicates(test_data)

    print(f"Temizlenmiş kayıt sayısı: {len(cleaned)}")
    print(f"Kaldırılan: {len(test_data) - len(cleaned)}")

    print("\nKalan kayıtlar:")
    for record in cleaned:
        print(f"  - ID: {record['id']}, Text: {record['text']}")


if __name__ == "__main__":
    main()
