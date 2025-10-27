"""
data4tr - Text Metrics and Quality Algorithms
Matematiksel algoritmalar ile metin kalitesi ve benzerlik ölçümleri.
"""

import re
import math
import hashlib
from typing import List, Dict, Tuple, Set
from collections import Counter


class TextMetrics:
    """
    Metin metrikleri ve kalite ölçümleri için algoritmalar
    """
    
    @staticmethod
    def calculate_quality_score(text: str) -> float:
        """
        Metin kalite skoru hesaplar (0-1 arası)
        
        Algoritma:
        QS = (LQ + CQ + SQ + PQ) / 4
        
        LQ (Length Quality): Metin uzunluğu kalitesi
        CQ (Character Quality): Karakter çeşitliliği
        SQ (Structure Quality): Yapısal kalite
        PQ (Punctuation Quality): Noktalama kalitesi
        
        Args:
            text: Değerlendirilecek metin
            
        Returns:
            Kalite skoru (0.0 - 1.0)
        """
        if not text or len(text.strip()) == 0:
            return 0.0
        
        text = text.strip()
        
        # 1. Length Quality (LQ)
        # Optimum uzunluk: 100-2000 karakter
        length = len(text)
        if length < 50:
            lq = length / 50.0 * 0.5  # Çok kısa: 0-0.5
        elif 50 <= length <= 2000:
            lq = 0.5 + 0.5 * (1 - abs(length - 1000) / 1000)  # Optimum: 0.5-1.0
        else:
            # Çok uzun: 1.0'dan azalt
            lq = max(0.5, 1.0 - (length - 2000) / 10000.0)
        
        # 2. Character Quality (CQ)
        # Türkçe karakter çeşitliliği
        turkish_chars = set('çğıöşüÇĞIİÖŞÜ')
        char_variety = len(set(text)) / len(text) if len(text) > 0 else 0
        has_turkish = len([c for c in text if c in turkish_chars]) > 0
        cq = (char_variety * 0.7) + (0.3 if has_turkish else 0.0)
        cq = min(1.0, cq)
        
        # 3. Structure Quality (SQ)
        # Cümle yapısı kalitesi
        sentences = re.split(r'[.!?]+', text)
        valid_sentences = [s for s in sentences if len(s.strip()) > 10]
        avg_sentence_length = sum(len(s) for s in valid_sentences) / len(valid_sentences) if valid_sentences else 0
        
        # Optimum cümle uzunluğu: 50-150 karakter
        if 50 <= avg_sentence_length <= 150:
            sq = 1.0
        elif avg_sentence_length < 50:
            sq = avg_sentence_length / 50.0
        else:
            sq = max(0.3, 1.0 - (avg_sentence_length - 150) / 500.0)
        
        # 4. Punctuation Quality (PQ)
        # Noktalama işareti kullanımı
        punctuation_marks = set('.,;:!?')
        words = text.split()
        words_with_punct = sum(1 for w in words if any(p in w for p in punctuation_marks))
        pq = words_with_punct / len(words) if words else 0.5
        pq = min(1.0, pq * 2)  # Normalize
        
        # Final score
        quality_score = (lq + cq + sq + pq) / 4.0
        return round(quality_score, 3)
    
    @staticmethod
    def calculate_tf(text: str) -> Dict[str, float]:
        """
        Term Frequency (TF) hesaplar
        
        TF(t,d) = (t'nin d'de görülme sayısı) / (d'deki toplam kelime sayısı)
        
        Args:
            text: Doküman metni
            
        Returns:
            Kelime -> TF skoru dictionary
        """
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        word_counts = Counter(words)
        tf_scores = {word: count / total_words for word, count in word_counts.items()}
        
        return tf_scores
    
    @staticmethod
    def calculate_idf(documents: List[str]) -> Dict[str, float]:
        """
        Inverse Document Frequency (IDF) hesaplar
        
        IDF(t) = log(N / (doküman sayısı(t içeren)))
        
        Args:
            documents: Tüm dokümanlar
            
        Returns:
            Kelime -> IDF skoru dictionary
        """
        N = len(documents)
        
        # Her kelime için kaç dokümanda geçtiğini hesapla
        document_frequency = Counter()
        
        for doc in documents:
            words = set(re.findall(r'\b\w+\b', doc.lower()))
            document_frequency.update(words)
        
        # IDF hesapla
        idf_scores = {
            word: math.log(N / (count + 1))  # +1 to avoid division by zero
            for word, count in document_frequency.items()
        }
        
        return idf_scores
    
    @staticmethod
    def calculate_tfidf(text: str, idf_scores: Dict[str, float]) -> Dict[str, float]:
        """
        TF-IDF skorunu hesaplar
        
        TF-IDF(t,d) = TF(t,d) × IDF(t)
        
        Args:
            text: Doküman metni
            idf_scores: IDF skorları
            
        Returns:
            Kelime -> TF-IDF skoru dictionary
        """
        tf_scores = TextMetrics.calculate_tf(text)
        
        tfidf_scores = {
            word: tf * idf_scores.get(word, 0)
            for word, tf in tf_scores.items()
        }
        
        return tfidf_scores
    
    @staticmethod
    def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        İki vektör arasında cosine similarity hesaplar
        
        cosine(θ) = (A · B) / (||A|| × ||B||)
        
        Args:
            vec1: İlk vektör (kelime -> skor)
            vec2: İkinci vektör (kelime -> skor)
            
        Returns:
            Benzerlik skoru (0-1 arası)
        """
        # Tüm unique kelimeleri topla
        all_words = set(vec1.keys()) | set(vec2.keys())
        
        if not all_words:
            return 0.0
        
        # Dot product
        dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in all_words)
        
        # Vector magnitudes
        magnitude1 = math.sqrt(sum(vec1.get(word, 0) ** 2 for word in all_words))
        magnitude2 = math.sqrt(sum(vec2.get(word, 0) ** 2 for word in all_words))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        similarity = dot_product / (magnitude1 * magnitude2)
        return round(similarity, 4)
    
    @staticmethod
    def jaccard_similarity(text1: str, text2: str) -> float:
        """
        Jaccard similarity hesaplar
        
        J(A,B) = |A ∩ B| / |A ∪ B|
        
        Args:
            text1: İlk metin
            text2: İkinci metin
            
        Returns:
            Jaccard similarity skoru (0-1 arası)
        """
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        similarity = intersection / union if union > 0 else 0.0
        return round(similarity, 4)
    
    @staticmethod
    def calculate_text_complexity(text: str) -> float:
        """
        Metin karmaşıklığını hesaplar (0-1 arası, yüksek = karmaşık)
        
        Algoritma:
        C = α × (unique_words / total_words) + β × (avg_word_length / max_word_length) + γ × (sentence_count)
        
        Args:
            text: Değerlendirilecek metin
            
        Returns:
            Karmaşıklık skoru
        """
        if not text:
            return 0.0
        
        # Kelime bazlı analiz
        words = re.findall(r'\b\w+\b', text)
        unique_words = len(set(words))
        total_words = len(words)
        
        # Ortalama kelime uzunluğu
        avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
        
        # Cümle sayısı
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if len(s.strip()) > 0])
        
        # Skorlar
        word_diversity = unique_words / total_words if total_words > 0 else 0
        length_complexity = avg_word_length / 10.0  # Normalize
        sentence_complexity = sentence_count / 20.0  # Normalize
        
        # Ağırlıklı ortalama
        complexity = (
            0.4 * word_diversity +
            0.3 * length_complexity +
            0.3 * sentence_complexity
        )
        
        return round(min(1.0, complexity), 3)


def main():
    """Test algoritmalar"""
    print("Text Metrics Algorithms Test\n" + "="*50)
    
    # Test metinleri
    text1 = "Türkçe doğal dil işleme, bilgisayar biliminin önemli bir alanıdır. Yapay zeka ve makine öğrenmesi teknikleri kullanılarak metinler analiz edilir."
    text2 = "Python programlama dili, veri bilimi ve yapay zeka projelerinde yaygın olarak kullanılmaktadır. Basit ve okunabilir sözdizimi sayesinde tercih edilmektedir."
    
    metrics = TextMetrics()
    
    # Kalite skoru
    quality1 = metrics.calculate_quality_score(text1)
    quality2 = metrics.calculate_quality_score(text2)
    print(f"\nKalite Skorları:")
    print(f"  Metin 1: {quality1}")
    print(f"  Metin 2: {quality2}")
    
    # Jaccard benzerliği
    jaccard = metrics.jaccard_similarity(text1, text2)
    print(f"\nJaccard Benzerliği: {jaccard}")
    
    # TF-IDF benzerliği
    documents = [text1, text2]
    idf_scores = metrics.calculate_idf(documents)
    tfidf1 = metrics.calculate_tfidf(text1, idf_scores)
    tfidf2 = metrics.calculate_tfidf(text2, idf_scores)
    cosine = metrics.cosine_similarity(tfidf1, tfidf2)
    print(f"Cosine Benzerliği (TF-IDF): {cosine}")
    
    # Karmaşıklık
    complexity1 = metrics.calculate_text_complexity(text1)
    complexity2 = metrics.calculate_text_complexity(text2)
    print(f"\nKarmaşıklık Skorları:")
    print(f"  Metin 1: {complexity1}")
    print(f"  Metin 2: {complexity2}")


if __name__ == "__main__":
    main()

