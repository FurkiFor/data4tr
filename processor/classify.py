"""
data4tr - Text Classification Module
AI yardımıyla metinleri kategorilere ayıran modül.
"""

import json
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Önceden tanımlanmış kategoriler
CATEGORIES = [
    "bilim",
    "teknoloji", 
    "edebiyat",
    "kültür",
    "tarih",
    "coğrafya",
    "sanat",
    "spor",
    "ekonomi",
    "eğitim",
    "sağlık",
    "genel"
]


class TextClassifier:
    """Metin sınıflandırma sınıfı"""
    
    def __init__(self, model: Optional[str] = None):
        """
        Args:
            model: AI model adı (örn: gpt-4, claude, local-llm)
        """
        self.model = model or "rule-based"
        self.categories = CATEGORIES
    
    def classify_with_keywords(self, text: str) -> Dict[str, any]:
        """
        Anahtar kelimelere dayalı basit sınıflandırma
        
        Args:
            text: Sınıflandırılacak metin
            
        Returns:
            Kategori bilgileri içeren sözlük
        """
        text_lower = text.lower()
        
        # Kategori anahtar kelimeleri
        keywords = {
            "bilim": ["bilim", "araştırma", "deney", "hipotez", "teori", "fizik", "kimya"],
            "teknoloji": ["teknoloji", "yazılım", "donanım", "bilgisayar", "internet", "dijital"],
            "edebiyat": ["edebiyat", "roman", "şiir", "yazar", "kitap", "eser"],
            "kültür": ["kültür", "gelenek", "görenek", "folklor", "milli"],
            "tarih": ["tarih", "geçmiş", "tarihi", "savaş", "imparatorluk", "devlet"],
            "coğrafya": ["coğrafya", "ülke", "şehir", "iklim", "dağ", "deniz"],
            "sanat": ["sanat", "resim", "heykel", "müze", "galeri", "sanatçı"],
            "spor": ["spor", "futbol", "basketbol", "oyuncu", "maç", "takım"],
            "ekonomi": ["ekonomi", "finans", "para", "bank", "ticaret", "piyasa"],
            "eğitim": ["eğitim", "okul", "öğrenci", "ders", "sınav", "üniversite"],
            "sağlık": ["sağlık", "tedavi", "hastalık", "doktor", "ilaç", "hastane"],
        }
        
        scores = {}
        for category, words in keywords.items():
            score = sum(1 for word in words if word in text_lower)
            scores[category] = score
        
        # En yüksek skora sahip kategoriyi bul
        if max(scores.values()) > 0:
            top_category = max(scores, key=scores.get)
            confidence = scores[top_category] / len(text.split())
        else:
            top_category = "genel"
            confidence = 0.5
        
        return {
            "category": top_category,
            "confidence": min(confidence, 1.0),
            "all_scores": scores
        }
    
    def classify_with_ai(self, text: str) -> Dict[str, any]:
        """
        AI model kullanarak sınıflandırma (placeholder)
        
        Args:
            text: Sınıflandırılacak metin
            
        Returns:
            AI'nın tahmin ettiği kategori
        """
        # Bu fonksiyon ileride OpenAI, Anthropic veya local LLM ile implement edilecek
        logger.warning("AI sınıflandırma henüz implement edilmedi, keyword-based fallback kullanılıyor")
        return self.classify_with_keywords(text)
    
    def classify(self, text: str) -> str:
        """
        Metni sınıflandır (basit API)
        
        Args:
            text: Sınıflandırılacak metin
            
        Returns:
            Kategori adı
        """
        if self.model and self.model != "rule-based":
            result = self.classify_with_ai(text)
        else:
            result = self.classify_with_keywords(text)
        
        return result["category"]


def classify_batch(texts: List[str]) -> List[Dict]:
    """
    Birden fazla metni toplu olarak sınıflandır
    
    Args:
        texts: Sınıflandırılacak metinler listesi
        
    Returns:
        Her metin için kategori bilgisi
    """
    classifier = TextClassifier()
    results = []
    
    for text in texts:
        category_info = classifier.classify_with_keywords(text)
        results.append(category_info)
    
    return results


def main():
    """Test ve örnek kullanım"""
    classifier = TextClassifier()
    
    test_texts = [
        "Albert Einstein izafiyet teorisini geliştirmiştir.",
        "Python programlama dili modern yazılım geliştirmede yaygın kullanılır.",
        "İstanbul Boğazı Asya ve Avrupa'yı birbirine bağlar."
    ]
    
    print("Metin Sınıflandırma Testi\n" + "="*50)
    
    for text in test_texts:
        result = classifier.classify(text)
        print(f"\nMetin: {text[:50]}...")
        print(f"Kategori: {result}")


if __name__ == "__main__":
    main()

