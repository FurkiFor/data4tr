"""
data4tr - Config Test
Konfigürasyon yöneticisi için testler
"""

import pytest
import os
from data4tr.config import ConfigManager, get_config


class TestConfigManager:
    """ConfigManager sınıfı için testler"""

    def setup_method(self):
        """Her test öncesi çalışır"""
        self.config = get_config()

    def test_config_loaded(self):
        """Konfigürasyonun yüklendiğini test et"""
        assert self.config is not None
        assert self.config.to_dict() != {}

    def test_get_nested_key(self):
        """Nested key erişimi testi"""
        url = self.config.get("sources.wikipedia.api.base_url")
        assert url is not None

    def test_get_default_value(self):
        """Varsayılan değer testi"""
        value = self.config.get("nonexistent.key", "default")
        assert value == "default"

    def test_get_source_config(self):
        """Kaynak konfigürasyonu alma testi"""
        source_config = self.config.get_source_config("wikipedia")
        assert source_config is not None
        assert "name" in source_config or "enabled" in source_config

    def test_is_source_enabled(self):
        """Kaynağın etkin olup olmadığını test et"""
        is_enabled = self.config.is_source_enabled("wikipedia")
        assert isinstance(is_enabled, bool)

    def test_set_and_get(self):
        """Set ve get işlemleri testi"""
        test_value = "test_value"
        self.config.set("test.key", test_value)
        retrieved = self.config.get("test.key")
        assert retrieved == test_value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
