"""
data4tr - Türkçe Veri Seti Oluşturma Kütüphanesi

Açık kaynaklı ve etik bir şekilde Türkçe veri setleri oluşturmak için gelişmiş bir kütüphane.

Kullanım Örneği:
    >>> from data4tr import Scraper, TextMetrics
    >>>
    >>> # Veri çek
    >>> scraper = Scraper()
    >>> articles = scraper.scrape_source('wikipedia', limit=50)
    >>>
    >>> # Kalite ölç
    >>> metrics = TextMetrics()
    >>> quality = metrics.calculate_quality_score(articles[0]['text'])
"""

__version__ = "1.0.0"
__author__ = "data4tr Contributors"

# Ana modülleri import et (relative imports)
try:
    from .scraper.scraper import Scraper
    from .scraper.cleaner import TextCleaner
    from .processor.classify import TextClassifier
    from .processor.deduplicate import Deduplicator
    from .processor.normalize import TextNormalizer
    from .exporter.export_jsonl import JSONLExporter
    from .exporter.export_csv import CSVExporter
    from .algorithms import TextMetrics
    from .config import get_config
except ImportError:
    # Eğer modüller bulunamazsa, boş pass
    pass

__all__ = [
    # Versiyon
    "__version__",
    # Scraper
    "Scraper",
    "TextCleaner",
    # Processor
    "TextClassifier",
    "Deduplicator",
    "TextNormalizer",
    # Exporter
    "JSONLExporter",
    "CSVExporter",
    # Algorithms
    "TextMetrics",
    # Config
    "get_config",
]


# Kolay import için namespace
class data4tr:
    """Ana namespace sınıfı"""

    @staticmethod
    def scrape(source="wikipedia", limit=100):
        """Hızlı veri çekme"""
        scraper = Scraper()
        return scraper.scrape_source(source, limit=limit)

    @staticmethod
    def classify(text):
        """Hızlı sınıflandırma"""
        classifier = TextClassifier()
        return classifier.classify(text)

    @staticmethod
    def quality(text):
        """Hızlı kalite ölçümü"""
        metrics = TextMetrics()
        return metrics.calculate_quality_score(text)

    @staticmethod
    def clean(text):
        """Hızlı temizlik"""
        cleaner = TextCleaner()
        return cleaner.destructive_clean(text)
