"""
data4tr - Algorithms Test
Metin metrikleri algoritmaları için birim testleri
"""

import pytest
from algorithms import TextMetrics


class TestTextMetrics:
    """TextMetrics sınıfı için testler"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.metrics = TextMetrics()
    
    def test_quality_score_empty_text(self):
        """Boş metin için kalite skoru testi"""
        score = self.metrics.calculate_quality_score("")
        assert score == 0.0
    
    def test_quality_score_short_text(self):
        """Kısa metin için kalite skoru testi"""
        text = "Kısa metin."
        score = self.metrics.calculate_quality_score(text)
        assert 0.0 <= score <= 1.0
    
    def test_quality_score_good_text(self):
        """İyi bir metin için kalite skoru testi"""
        text = """
        Türkçe doğal dil işleme, bilgisayar biliminin önemli bir alanıdır.
        Yapay zeka ve makine öğrenmesi teknikleri kullanılarak metinler analiz edilir.
        Bu alan, dil modelleri ve sentetik veri üretimi gibi konuları kapsar.
        """
        score = self.metrics.calculate_quality_score(text)
        assert 0.4 <= score <= 1.0
    
    def test_tf_calculation(self):
        """Term Frequency hesaplama testi"""
        text = "çiçek bahçe çiçek"
        tf_scores = self.metrics.calculate_tf(text)
        
        assert 'çiçek' in tf_scores
        assert tf_scores['çiçek'] == pytest.approx(0.67, abs=0.1)
        assert tf_scores['bahçe'] == pytest.approx(0.33, abs=0.1)
    
    def test_jaccard_similarity(self):
        """Jaccard benzerliği testi"""
        text1 = "türkçe dil işleme bilgisayar"
        text2 = "dil işleme yapay zeka"
        
        similarity = self.metrics.jaccard_similarity(text1, text2)
        assert 0.0 <= similarity <= 1.0
        assert similarity > 0
    
    def test_jaccard_similarity_no_common(self):
        """Ortak kelime yokken Jaccard benzerliği testi"""
        text1 = "türkçe dil"
        text2 = "python kod"
        
        similarity = self.metrics.jaccard_similarity(text1, text2)
        assert similarity == 0.0
    
    def test_text_complexity(self):
        """Metin karmaşıklığı testi"""
        text = "Basit metin."
        complexity = self.metrics.calculate_text_complexity(text)
        assert 0.0 <= complexity <= 1.0
    
    def test_tfidf_calculation(self):
        """TF-IDF hesaplama testi"""
        documents = [
            "türkçe dil işleme",
            "yapay zeka makine öğrenmesi",
            "dil model nlp"
        ]
        
        idf_scores = self.metrics.calculate_idf(documents)
        assert 'dil' in idf_scores
        assert idf_scores['dil'] >= 0  # Her kelime en az 0 IDF skoru almalı
        
        text = "dil işleme"
        tfidf_scores = self.metrics.calculate_tfidf(text, idf_scores)
        assert 'dil' in tfidf_scores
        assert tfidf_scores['dil'] >= 0  # TF-IDF skoru >= 0 olmalı


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

