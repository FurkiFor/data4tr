"""
data4tr - Web Scraper Module
Açık kaynaklı web sitelerinden Türkçe metin toplama modülü.
Refactored with configuration-based architecture
"""

import logging
from typing import List, Dict, Optional
import yaml
from pathlib import Path

from config import get_config
from .base import ScraperRegistry, BaseScraper
from .sources import WikipediaScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Scraper'ları registry'ye kaydet
ScraperRegistry.register('wikipedia', WikipediaScraper)


class Scraper:
    """
    Web'den Türkçe metinleri çeken ana sınıf
    Configuration-based, modular architecture
    """
    
    def __init__(self, sources_file: Optional[str] = None):
        """
        Args:
            sources_file: Kaynakların tanımlandığı YAML dosyası (opsiyonel)
        """
        self.config = get_config()
        
        # Sources file'dan kaynakları yükle (backward compatibility)
        if sources_file:
            self.sources = self._load_sources(sources_file)
        else:
            sources_file = self.config.get('paths.sources_file', 'scraper/sources.yaml')
            self.sources = self._load_sources(sources_file)
    
    def _load_sources(self, filepath: str) -> Dict:
        """Kaynak dosyasını yükle"""
        try:
            file_path = Path(filepath)
            if not file_path.exists():
                logger.warning(f"Kaynak dosyası bulunamadı: {filepath}, config.yaml kullanılacak")
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Kaynak dosyası yükleme hatası: {e}")
            return {}
    
    def scrape_source(self, source_name: str, limit: int = 100) -> List[Dict]:
        """
        Belirtilen kaynaktan veri çeker
        
        Args:
            source_name: Kaynak adı
            limit: Maksimum çekilecek kayıt sayısı
            
        Returns:
            Çekilen metinlerin listesi
        """
        # Konfigürasyondan kaynak bilgisini al
        source_config = self.config.get_source_config(source_name)
        
        if not source_config:
            # Fallback to sources.yaml
            if source_name in self.sources.get('sources', {}):
                source_config = self.sources['sources'][source_name]
            else:
                logger.error(f"Kaynak bulunamadı: {source_name}")
                return []
        
        # Scraper instance oluştur (Factory pattern)
        scraper_instance = ScraperRegistry.create(source_name, source_config)
        
        if scraper_instance is None:
            logger.error(f"Scraper oluşturulamadı: {source_name}")
            return []
        
        # Veriyi çek
        return scraper_instance.scrape(limit)
    
    def list_sources(self) -> List[str]:
        """
        Mevcut kaynakları listele
        
        Returns:
            Kaynak isimleri listesi
        """
        sources = []
        
        # Config'den kaynakları al
        sources_config = self.config.get('sources', {})
        for name, config in sources_config.items():
            if config.get('enabled', False):
                sources.append(name)
        
        return sources
    
    def get_source_info(self, source_name: str) -> Optional[Dict]:
        """
        Kaynak bilgilerini al
        
        Args:
            source_name: Kaynak adı
            
        Returns:
            Kaynak bilgileri
        """
        source_config = self.config.get_source_config(source_name)
        if source_config:
            return {
                'name': source_config.get('name'),
                'enabled': source_config.get('enabled'),
                'license': source_config.get('license')
            }
        return None


def main():
    """Test ve örnek kullanım"""
    scraper = Scraper()
    
    # Kaynakları listele
    print("Mevcut kaynaklar:")
    for source in scraper.list_sources():
        info = scraper.get_source_info(source)
        print(f"  - {source}: {info}")
    
    # Wikipedia'dan örnek veri çek
    articles = scraper.scrape_source('wikipedia', limit=10)
    
    print(f"\nOK: {len(articles)} sayfa cekildi")
    if articles:
        print(f"\nİlk makale başlığı: {articles[0]['title']}")
        print(f"Önizleme: {articles[0]['text'][:100]}...")


if __name__ == "__main__":
    main()
