# 🚀 Hızlı Başlangıç Rehberi

## Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Kullanım Örnekleri

### 1. Wikipedia'dan Veri Çekme

```bash
python cli.py scrape --source wikipedia --limit 50
```

Bu komut:
- 50 rastgele Türkçe Wikipedia makalesi çeker
- HTML temizliği yapar ve metni normalize eder
- `data/raw/wikipedia_50.json` dosyasına kaydeder

### 2. Veriyi İşleme

```bash
python cli.py process --model rule-based
```

Bu komut:
- Metinleri kategorilere ayırır (bilim, teknoloji vb.)
- Yinelenen girişleri temizler
- Türkçe metinleri normalize eder
- `data/cleaned/processed_data.json` dosyasına kaydeder

### 3. Veri Setini Dışa Aktarma

```bash
# JSONL formatında dışa aktar (makine öğrenmesi için)
python cli.py export --format jsonl

# CSV formatında dışa aktar (veri analizi için)
python cli.py export --format csv
```

Çıktı dosyaları `data/output/` dizininde:
- `dataset.jsonl` - JSON Lines formatı
- `dataset.csv` - CSV formatı

## Tam İş Akışı

```bash
# Adım 1: Veri topla
python cli.py scrape --source wikipedia --limit 100

# Adım 2: Veriyi işle
python cli.py process --model rule-based

# Adım 3: Veri setini dışa aktar
python cli.py export --format jsonl
```

## Modül Kullanımı (Programatik API)

```python
from scraper.scraper import Scraper
from processor.classify import TextClassifier

# Veri çek
scraper = Scraper()
articles = scraper.scrape_source('wikipedia', limit=50)

# Metni sınıflandır
classifier = TextClassifier()
category = classifier.classify("Bu bir teknoloji makalesidir.")
print(category)  # "teknoloji"
```

## Algoritma Kullanımı

```python
from algorithms import TextMetrics

# Metin kalitesi ölçümü
metrics = TextMetrics()
quality_score = metrics.calculate_quality_score(metin)

# Metin benzerliği
similarity = metrics.jaccard_similarity(metin1, metin2)
```

## Konfigürasyon

Tüm ayarlar `config/config.yaml` dosyasında:

```yaml
sources:
  wikipedia:
    enabled: true
    api:
      base_url: "https://tr.wikipedia.org/api/rest_v1"
```

## Sonraki Adımlar

- `scraper/sources.yaml` dosyasına yeni veri kaynakları ekleyin
- OpenAI/Claude ile AI tabanlı sınıflandırma ekleyin
- `exporter/` modüllerinde export formatlarını özelleştirin
- `processor/classify.py` dosyasında kategorileri genişletin
