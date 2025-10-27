# 📚 data4tr - Kütüphane Kullanımı

data4tr, hem CLI aracı hem de Python kütüphanesi olarak kullanılabilir.

## 📦 Kurulum

### Pip ile Kurulum

```bash
# Local kurulum
pip install -e .

# Geliştirme bağımlılıkları ile
pip install -e ".[dev]"

# AI modülleri ile
pip install -e ".[ai]"
```

## 🚀 Kütüphane Kullanımı

### Basit Kullanım

```python
import data4tr

# Veri çek
articles = data4tr.scrape('wikipedia', limit=50)

# Metni sınıflandır
category = data4tr.classify("Bu bir teknoloji makalesidir.")

# Kalite ölç
quality = data4tr.quality("Uzun ve iyi bir metin...")

# Temizle
cleaned = data4tr.clean("<html>Metin</html>")
```

## 📝 Örnek Projeler

Detaylı örnekler için README ve ARCHITECTURE dokümantasyonuna bakın.

