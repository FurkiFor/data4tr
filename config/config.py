"""
data4tr - Configuration Manager
Merkezi konfigürasyon yönetimi ve environment variable desteği.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Konfigürasyon yöneticisi - tüm ayarlar buradan yönetilir
    Environment variable'ları destekler
    """
    
    _instance = None
    _config = {}
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """ConfigManager'i başlat"""
        if self._initialized:
            return
        
        self._initialized = True
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / "config.yaml"
        self.load_config()
    
    def load_config(self) -> None:
        """Konfigürasyon dosyasını yükle ve environment variable'ları işle"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                raw_config = yaml.safe_load(f) or {}
            
            # Environment variable'ları resolve et
            self._config = self._resolve_env_vars(raw_config)
            
            logger.info(f"Konfigürasyon yüklendi: {self.config_file}")
            
        except FileNotFoundError:
            logger.error(f"Konfigürasyon dosyası bulunamadı: {self.config_file}")
            self._config = {}
        except Exception as e:
            logger.error(f"Konfigürasyon yükleme hatası: {e}")
            self._config = {}
    
    def _resolve_env_vars(self, obj: Any) -> Any:
        """
        YAML içindeki ${VAR_NAME} formatındaki environment variable'ları resolve et
        
        Args:
            obj: YAML'dan yüklenen obje
            
        Returns:
            Environment variable'ları resolve edilmiş obje
        """
        if isinstance(obj, dict):
            return {k: self._resolve_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._resolve_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
            # ${VAR_NAME} formatını çöz
            var_name = obj[2:-1]
            default_value = None
            
            # ${VAR_NAME:default} formatını destekle
            if ':' in var_name:
                var_name, default_value = var_name.split(':', 1)
            
            env_value = os.getenv(var_name, default_value)
            
            if env_value is None:
                logger.warning(f"Environment variable bulunamadı: {var_name}")
                return ""
            
            return env_value
        else:
            return obj
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Konfigürasyon değeri al (nested key desteği ile)
        
        Args:
            key: Nokta ile ayrılmış nested key (örn: "sources.wikipedia.api.base_url")
            default: Varsayılan değer
            
        Returns:
            Konfigürasyon değeri
        """
        if not key:
            return default
        
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Konfigürasyon değeri set et
        
        Args:
            key: Nokta ile ayrılmış nested key
            value: Ayar edilecek değer
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_source_config(self, source_name: str) -> Optional[Dict]:
        """Belirli bir kaynağın konfigürasyonunu al"""
        return self.get(f"sources.{source_name}")
    
    def is_source_enabled(self, source_name: str) -> bool:
        """Kaynağın etkin olup olmadığını kontrol et"""
        return self.get(f"sources.{source_name}.enabled", False)
    
    def reload(self) -> None:
        """Konfigürasyonu yeniden yükle"""
        self.load_config()
    
    def to_dict(self) -> Dict:
        """Tüm konfigürasyonu dict olarak döndür"""
        return self._config.copy()


# Global config instance
_config_manager = None

def get_config() -> ConfigManager:
    """Global config manager instance'ı al"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def main():
    """Test konfigürasyon yöneticisi"""
    config = get_config()
    
    # Test environment variable
    os.environ['TEST_VAR'] = 'test_value'
    
    print("Konfigürasyon Testi\n" + "="*50)
    
    # App bilgileri
    print(f"\nUygulama: {config.get('app.name')}")
    print(f"Versiyon: {config.get('app.version')}")
    
    # Kaynak konfigürasyonu
    print(f"\nWikipedia URL: {config.get('sources.wikipedia.api.base_url')}")
    print(f"Wikipedia etkin: {config.get('sources.wikipedia.enabled')}")
    
    # Kaynak config objesi
    wiki_config = config.get_source_config('wikipedia')
    print(f"\nWikipedia API: {wiki_config.get('api.base_url') if wiki_config else 'N/A'}")
    
    # Tüm konfigürasyon
    print(f"\nToplam konfigürasyon anahtarları: {len(config.to_dict())}")


if __name__ == "__main__":
    main()

