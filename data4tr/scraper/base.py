"""
data4tr - Base Scraper Classes
Tüm scraper'lar için abstract base class'lar
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Tüm scraper'lar için abstract base class
    Her veri kaynağı için show isimli scraper bu sınıftan türetilmelidir.
    """

    def __init__(self, config: Dict):
        """
        Args:
            config: Kaynak konfigürasyonu
        """
        self.config = config
        self.name = config.get("name", "Unknown")
        self.enabled = config.get("enabled", False)
        self.api_config = config.get("api", {})
        self.rate_limit_config = config.get("rate_limit", {})

    @abstractmethod
    def scrape(self, limit: int = 100) -> List[Dict]:
        """
        Veri çekme metodu - her scraper'da implement edilmeli

        Args:
            limit: Çekilecek kayıt sayısı

        Returns:
            Çekilen veri listesi
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Konfigürasyonun geçerli olup olmadığını kontrol et

        Returns:
            Geçerli ise True
        """
        pass

    def get_api_url(self, endpoint: str = "") -> str:
        """
        API URL'ini oluştur

        Args:
            endpoint: Endpoint yolu

        Returns:
            Tam API URL'i
        """
        base_url = self.api_config.get("base_url", "")
        endpoint = endpoint.lstrip("/")
        return f"{base_url}/{endpoint}" if endpoint else base_url

    def get_headers(self) -> Dict[str, str]:
        """
        HTTP headers'ı al

        Returns:
            Headers dictionary
        """
        headers = self.api_config.get("headers", {})
        # String keys'e çevir (YAML'dan dict olarak geliyor olabilir)
        return {str(k): str(v) for k, v in headers.items()}

    def get_timeout(self) -> int:
        """
        Request timeout değerini al

        Returns:
            Timeout süresi (saniye)
        """
        return self.api_config.get("timeout", 30)

    def get_rate_limit_delay(self) -> float:
        """
        Rate limit için bekleme süresi

        Returns:
            Bekleme süresi (saniye)
        """
        return self.rate_limit_config.get("delay_between_requests", 1.0)


class ScraperRegistry:
    """
    Scraper'ları kaydeden ve yöneten registry pattern implementation
    Factory pattern ile birlikte kullanılır
    """

    _registry = {}

    @classmethod
    def register(cls, name: str, scraper_class: type):
        """
        Bir scraper class'ını kaydet

        Args:
            name: Kaynak adı (örn: 'wikipedia')
            scraper_class: Scraper class'ı (BaseScraper'dan türetilmiş)
        """
        cls._registry[name] = scraper_class
        logger.info(f"Scraper kaydedildi: {name} -> {scraper_class.__name__}")

    @classmethod
    def get(cls, name: str) -> Optional[type]:
        """
        Kayıtlı scraper class'ını al

        Args:
            name: Scraper adı

        Returns:
            Scraper class'ı veya None
        """
        return cls._registry.get(name)

    @classmethod
    def list_registered(cls) -> List[str]:
        """
        Kayıtlı tüm scraper'ları listele

        Returns:
            Scraper isimleri listesi
        """
        return list(cls._registry.keys())

    @classmethod
    def create(cls, name: str, config: Dict) -> Optional[BaseScraper]:
        """
        Scraper instance'ı oluştur (Factory method)

        Args:
            name: Scraper adı
            config: Konfigürasyon

        Returns:
            Scraper instance veya None
        """
        scraper_class = cls.get(name)
        if scraper_class is None:
            logger.error(f"Scraper bulunamadı: {name}")
            return None

        try:
            instance = scraper_class(config)
            if instance.validate_config():
                return instance
            else:
                logger.error(f"Geçersiz konfigürasyon: {name}")
                return None
        except Exception as e:
            logger.error(f"Scraper oluşturma hatası: {e}")
            return None
