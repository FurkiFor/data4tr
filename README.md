# 🇹🇷 data4tr

[![CI Tests](https://github.com/username/data4tr/workflows/CI%20Tests/badge.svg)](https://github.com/username/data4tr/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**data4tr**, Türkçe metinlerden açık kaynaklı ve etik bir şekilde veri seti oluşturmayı amaçlayan bir projedir.  
Yapay zekâ desteğiyle metinleri **toplar**, **temizler**, **sınıflandırır** ve **model eğitimine hazır hale getirir**.

---

## 🎯 Amaç

Türkçe doğal dil işleme (NLP) alanında kaliteli, açık ve yeniden üretilebilir veri setleri büyük eksikliktir.  
**data4tr**, bu eksikliği kapatmak için geliştirilen açık kaynaklı bir araç setidir.

Bu proje:
- Açık ve izinli kaynaklardan Türkçe metin toplar  
- AI yardımıyla dil temizliği ve sınıflandırma yapar  
- Çıktıyı JSONL veya CSV gibi veri bilimi dostu formatlarda üretir  

---

## 🧱 Proje Yapısı

```
data4tr/
 ├── config/               # Konfigürasyon yönetimi
 │   ├── config.yaml       # Merkezi konfigürasyon dosyası
 │   └── config.py         # Konfigürasyon yöneticisi
 │
 ├── scraper/              # Web'den veri toplama modülü
 │   ├── base.py           # Abstract base classes
 │   ├── scraper.py        # Ana scraper
 │   ├── cleaner.py        # HTML ve karakter temizliği
 │   └── sources/          # Kaynak-specific scraper'lar
 │       └── wikipedia.py
 │
 ├── processor/            # AI ile işleme ve etiketleme
 │   ├── classify.py       # Metin türü / konu sınıflandırması
 │   ├── deduplicate.py    # Yinelenen verilerin ayıklanması
 │   └── normalize.py      # İmla ve dil düzenleme
 │
 ├── algorithms/           # Matematiksel algoritmalar
 │   └── metrics.py        # Metin metrikleri ve kalite skorları
 │
 ├── exporter/             # Veri seti dışa aktarma modülü
 │   ├── export_jsonl.py
 │   ├── export_csv.py
 │   │   └── schema.json
 │
 ├── data/
 │   ├── raw/              # Ham çekilen metinler
 │   ├── cleaned/          # Temizlenmiş metinler
 │   └── output/           # Nihai veri setleri
 │
 ├── cli.py                # Komut satırı arayüzü
 ├── requirements.txt
 └── README.md
```

---

## ⚙️ Özellikler

✅ Açık kaynaklı ve şeffaf  
✅ Türkçe odaklı veri toplama  
✅ Yapay zekâ ile sınıflandırma ve temizlik  
✅ Tek komutla veri seti oluşturma  
✅ JSONL / CSV / Parquet format desteği  

---

## 🚀 Kullanım

Örnek terminal komutları:

```bash
# 1. Belirli bir kaynaktan veri topla
python cli.py scrape --source wikipedia --limit 500

# 2. AI ile metinleri işle
python cli.py process --model gpt-4

# 3. Temizlenmiş veri setini dışa aktar
python cli.py export --format jsonl
```

---

## 🧠 Yapay Zekâ Desteği

data4tr, toplanan metinleri şu görevlerde AI yardımıyla işler:

- **Sınıflandırma:** haber, eğitim, teknoloji, kültür vb.  
- **Temizlik:** imla hatalarını düzeltme, gereksiz ifadeleri ayıklama  
- **Filtreleme:** spam veya tekrar eden içerikleri çıkarma  
- **Genişletme (opsiyonel):** kı性别 metinleri anlam bozulmadan zenginleştirme

---

## 🔬 Matematiksel Algoritmalar

data4tr, veri kalitesini değerlendirmek için gelişmiş algoritmalar kullanır:

### 1. Metin Kalite Skoru (Quality Score)

Her metin için **0-1 arası kalite skoru** hesaplanır:

```
QS = (LQ + CQ + SQ + PQ) / 4
```

- **LQ (Length Quality):** Metin uzunluğu kalitesi
  - Optimum: 100-2000 karakter
  - Çok kısa veya uzun metinlerde azalır

- **CQ (Character Quality):** Karakter çeşitliliği
  - Türkçe karakter kullanımı kontrolü
  - Karakter çeşitliliği ölçümü

- **SQ (Structure Quality):** Yapısal kalite
  - Cümle uzunluğu analizi
  - Cümle sayısı değerlendirmesi

- **PQ (Punctuation Quality):** Noktalama kalitesi
  - Noktalama işareti kullanım oranı

### 2. TF-IDF (Term Frequency-Inverse Document Frequency)

Metinlerin içerik önemini ölçer:

```
TF(t,d) = kelime_sayısı(t,d) / toplam_kelime_sayısı(d)
```

```
IDF(t) = log(N / doküman_sayısı(t_geçen))
```

```
TF-IDF(t,d) = TF(t,d) × IDF(t)
```

**Kullanım:** Benzer konulu metinleri gruplama ve kategori tahmininde kullanılır.

### 3. Cosine Similarity (Kosinüs Benzerliği)

İki metin arasındaki benzerlik ölçümü:

```
cosine(θ) = (A · B) / (||A|| × ||B||)
```

**Kullanım:** Duplicate detection ve benzer içerik filtrelemede.

### 4. Jaccard Similarity (Jaccard Benzerliği)

Kelime kümesi benzerliği:

```
J(A,B) = |A ∩ B| / |A ∪ B|
```

**Kullanım:** Basit ve hızlı benzerlik hesaplama.

### 5. Metin Karmaşıklığı (Text Complexity)

Metin zorluk seviyesi:

```
C = 0.4 × (unique_words / total_words) + 
    0.3 × (avg_word_length / 10) + 
    0.3 × (sentence_count / 20)
```

**Kullanım:** Veri setinin hedef kitleye uygunluğunu değerlendirme.

### Algoritma Kullanım Örnekleri

```python
from algorithms import TextMetrics

metrics = TextMetrics()

# Kalite skoru
quality = metrics.calculate_quality_score(text)

# Benzerlik ölçümü
similarity = metrics.jaccard_similarity(text1, text2)

# TF-IDF vektörü
tfidf = metrics.calculate_tfidf(text, idf_scores)
```  

---

## 📊 Üretilen Veri Seti Formatı

Her veri kaydı aşağıdaki örneğe benzer şekilde saklanır:

```json
{
  "id": "a94f2c8e",
  "source": "wikipedia",
  "category": "bilim",
  "text": "Fotosentez, bitkilerin güneş ışığını enerjiye dönüştürdüğü süreçtir.",
  "cleaned": true
}
```

---

## ⚖️ Yasal ve Etik İlkeler

data4tr yalnızca:
- **Açık lisanslı (CC, MIT, GNU vb.)** içerikleri toplar  
- **Kamuya açık ve ticari olmayan** verileri işler  
- **Kişisel veri veya kullanıcı içeriği** barındırmaz  

Amacımız **Türkçe dil modellerinin gelişimini desteklemek**, telif veya gizlilik ihlali yapmak değildir.

---

## 🧩 Yol Haritası

- [ ] Yeni açık kaynak sitelerin eklenmesi  
- [ ] GPT tabanlı özetleme ve genişletme  
- [ ] HuggingFace veri seti entegrasyonu  
- [ ] Basit web arayüzü (Streamlit)  
- [ ] Label Studio entegrasyonu  

---

## 🤝 Katkı

Katkı yapmak isterseniz:
1. Repo’yu forklayın  
2. Yeni bir branch açın  
3. Kodunuzu ekleyip PR (Pull Request) gönderin  

Topluluk katkılarına tamamen açığız.  
Kodunuzu gönderirken **etik veri toplama prensiplerine** uymanız yeterlidir.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile yayımlanmıştır.  
Kodunuzu ve veri setlerinizi özgürce kullanabilir, değiştirebilir ve paylaşabilirsiniz.

---

## 💬 İletişim

**data4tr** topluluğu yakında açık olacak.  
Şimdilik öneri ve katkılarınızı GitHub Issues üzerinden iletebilirsiniz.
