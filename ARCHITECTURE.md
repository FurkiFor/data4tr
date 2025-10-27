# 🏗️ data4tr - Mimari Dokümantasyonu

## Genel Bakış

data4tr, **modüler**, **konfigürasyon tabanlı** ve **genişletilebilir** bir mimari ile tasarlanmıştır.

## Mimari Prensipleri

### 1. **Configuration-Based Architecture**
- Tüm URL'ler, ayarlar ve konfigürasyonlar `config/config.yaml` dosyasında
- Hardcoded değerler yok
- Environment variable desteği

### 2. **Modular Design**
- Her modül bağımsız çalışabilir
- Loose coupling, high cohesion
- Interface-based design

### 3. **Pattern-Based Architecture**
- **Factory Pattern**: Scraper oluşturma
- **Registry Pattern**: Scraper kaydı
- **Abstract Base Classes**: BaseScraper, BaseProcessor
- **Singleton Pattern**: ConfigManager

## Proje Yapısı

```
data4tr/
├── config/              # Konfigürasyon Yönetimi
│   ├── config.yaml     # Tüm ayarlar burada
│   └── config.py       # ConfigManager (Singleton)
│
├── scraper/            # Veri Toplama Modülü
│   ├── base.py        # BaseScraper abstract class
│   ├── scraper.py     # Ana scraper orkestratörü
│   ├── cleaner.py     # Text cleaning utilities
│   └── sources/       # Kaynak-specific scraper'lar
│       ├── wikipedia.py
│       └── __init__.py
│
├── processor/         # İşleme Modülü
│   ├── classify.py    # Sınıflandırma
│   ├── deduplicate.py # Duplicate removal
│   └── normalize.py   # Text normalization
│
├── exporter/          # Dışa Aktarma Modülü
│   ├── export_jsonl.py
│   ├── export_csv.py
│   └── schema.json
│
├── algorithms/       # Matematiksel Algoritmalar
│   └── metrics.py   # Metin metrikleri ve kalite skorları
│
└── cli.py           # Command Line Interface
```

## Katmanlar

### Configuration Layer
```python
from config import get_config

config = get_config()
api_url = config.get('sources.wikipedia.api.base_url')
```

**Özellikler:**
- YAML tabanlı konfigürasyon
- Environment variable desteği `${VAR_NAME}`
- Nested key erişimi (`sources.wikipedia.api.base_url`)
- Singleton pattern ile global erişim

### Scraper Layer
```python
from scraper.scraper import Scraper
from scraper.sources.wikipedia import WikipediaScraper
from scraper.base import ScraperRegistry, BaseScraper
```

**Mimari:**
- `BaseScraper`: Tüm scraper'lar için abstract base class
- `ScraperRegistry`: Factory pattern ile scraper oluşturma
- Kaynak-specific scraper'lar `sources/` altında
- Konfigürasyondan otomatik olarak bilgi alır

**Yeni Scraper Ekleme:**
```python
# 1. Scraper oluştur
class MySourceScraper(BaseScraper):
    def validate_config(self):
        # Config validasyonu
        return True
    
    def scrape(self, limit):
        # Scraping logic
        return data

# 2. Registry'ye kaydet
ScraperRegistry.register('mysource', MySourceScraper)

# 3. config.yaml'a ekle
# sources:
#   mysource:
#     enabled: true
#     api:
#       base_url: "https://api.example.com"
```

### Processing Layer
- Modular processors
- Her processor bağımsız çalışabilir
- Pipeline pattern ile birleştirilebilir

### Export Layer
- Format-specific exporters
- Schema validation
- Configurable output

## Konfigürasyon Yönetimi

### YAML Konfigürasyonu
```yaml
sources:
  wikipedia:
    enabled: true
    api:
      base_url: "https://tr.wikipedia.org/api/rest_v1"
      random_page: "/page/random/summary"
      timeout: 10
    rate_limit:
      delay_between_requests: 1.0
```

### Environment Variables
```yaml
sources:
  mysource:
    api:
      api_key: "${MY_API_KEY}"  # Environment'tan alınır
```

### Programmatic Erişim
```python
config = get_config()

# Nested key erişimi
url = config.get('sources.wikipedia.api.base_url')

# Tam config objesi
source_config = config.get_source_config('wikipedia')

# Ayar değiştirme
config.set('sources.wikipedia.enabled', False)
```

## Genişletme Noktaları

### 1. Yeni Veri Kaynağı Ekleme

```python
# scraper/sources/mynews.py
class MyNewsScraper(BaseScraper):
    def validate_config(self):
        # Validate
        return True
    
    def scrape(self, limit):
        # Custom logic
        pass

# scraper/scraper.py
from .sources.mynews import MyNewsScraper
ScraperRegistry.register('mynews', MyNewsScraper)

# config/config.yaml
sources:
  mynews:
    enabled: true
    api:
      base_url: "${MY_NEWS_API_URL}"
```

### 2. Yeni İşleme Modülü Ekleme

```python
# processor/custom_processor.py
class CustomProcessor:
    def process(self, data):
        # Process data
        return processed_data

# cli.py
from processor.custom_processor import CustomProcessor
processor = CustomProcessor()
result = processor.process(data)
```

### 3. Yeni Export Formatı

```python
# exporter/export_parquet.py
class ParquetExporter:
    def export(self, data, filename):
        # Export logic
        pass

# cli.py
from exporter.export_parquet import ParquetExporter
exporter = ParquetExporter()
exporter.export(data, "output.parquet")
```

## Best Practices

1. **Hardcoded değer kullanmayın**: Her şey config'de olmalı
2. **Abstract class'lardan türetin**: BaseScraper, BaseProcessor
3. **Registry pattern kullanın**: Yeni kaynaklar eklerken
4. **Environment variable'ları tercih edin**: Hassas bilgiler için
5. **Logging ekleyin**: Tüm önemli işlemler için
6. **Error handling**: Try-catch blokları ile

## Konfigürasyon Önceliği

1. **Environment Variables** (en yüksek)
2. **config/config.yaml**
3. **Varsayılan değerler** (kod içinde)

## Örnek Kullanım

```python
from config import get_config
from scraper.scraper import Scraper
from processor.classify import TextClassifier

# Config'den oku
config = get_config()
if config.is_source_enabled('wikipedia'):
    # Scrape
    scraper = Scraper()
    data = scraper.scrape_source('wikipedia', limit=100)
    
    # Process
    classifier = TextClassifier()
    for record in data:
        record['category'] = classifier.classify(record['text'])
```

## Gelecek Gelişmeler

- [ ] Database backend desteği
- [ ] Streaming data işleme
- [ ] Distributed scraping
- [ ] Plugin system
- [ ] Web UI
- [ ] API server

