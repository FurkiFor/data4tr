"""
data4tr - Wikipedia Scraper
Wikipedia API için özel scraper implementation
"""

import requests
import time
import hashlib
import logging
from typing import List, Dict
from ..base import BaseScraper

logger = logging.getLogger(__name__)


class WikipediaScraper(BaseScraper):
    """
    Wikipedia API için özel scraper
    Abstract BaseScraper'dan türetilmiştir
    """
    
    def __init__(self, config: Dict):
        """Wikipedia scraper'ı başlat"""
        super().__init__(config)
        self.session = requests.Session()
        self.session.headers.update(self.get_headers())
    
    def validate_config(self) -> bool:
        """Konfigürasyonun geçerli olup olmadığını kontrol et"""
        # Nested key'leri kontrol et
        api_url = self.api_config.get('base_url')
        random_page = self.api_config.get('random_page')
        
        if not api_url or not random_page:
            logger.error("Gerekli konfigürasyon anahtarları eksik: api.base_url, api.random_page")
            return False
        
        return True
    
    def scrape(self, limit: int = 100) -> List[Dict]:
        """
        Wikipedia'dan Türkçe metinleri çeker
        
        Args:
            limit: Çekilecek sayfa sayısı
            
        Returns:
            Metinlerin listesi
        """
        if not self.enabled:
            logger.warning(f"Kaynak devre dışı: {self.name}")
            return []
        
        logger.info(f"Wikipedia'dan {limit} sayfa çekiliyor...")
        articles = []
        
        # API URL'i konfigürasyondan al
        random_page_path = self.api_config.get('random_page', '/page/random/summary')
        api_url = self.get_api_url(random_page_path)
        
        for i in range(limit):
            try:
                response = self.session.get(
                    api_url,
                    timeout=self.get_timeout()
                )
                response.raise_for_status()
                data = response.json()
                
                article = {
                    'id': self._generate_id(data.get('title', '')),
                    'source': 'wikipedia',
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'title': data.get('title', ''),
                    'text': data.get('extract', ''),
                    'timestamp': time.time()
                }
                
                if article['text']:
                    articles.append(article)
                
                # Rate limiting - konfigürasyondan al
                time.sleep(self.get_rate_limit_delay())
                
                if (i + 1) % 10 == 0:
                    logger.info(f"{i + 1}/{limit} sayfa çekildi")
                    
            except Exception as e:
                logger.error(f"Hata: {e}")
                continue
        
        logger.info(f"Toplam {len(articles)} sayfa başarıyla çekildi")
        return articles
    
    def _generate_id(self, text: str) -> str:
        """Metinden benzersiz ID oluştur"""
        return hashlib.md5(text.encode()).hexdigest()[:8]

