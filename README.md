# 🇹🇷 data4tr

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
data4tr/
├── scraper/ # Web’den veri toplama modülü
│ ├── sources.yaml # İzinli kaynaklar listesi
│ ├── scraper.py # Metinleri çeker
│ └── cleaner.py # HTML ve karakter temizliği
│
├── processor/ # AI ile işleme ve etiketleme
│ ├── classify.py # Metin türü / konu sınıflandırması
│ ├── deduplicate.py # Yinelenen verilerin ayıklanması
│ └── normalize.py # İmla ve dil düzenleme
│
├── exporter/ # Veri seti dışa aktarma modülü
│ ├── export_jsonl.py
│ ├── export_csv.py
│ └── schema.json
│
├── data/
│ ├── raw/ # Ham çekilen metinler
│ ├── cleaned/ # Temizlenmiş metinler
│ └── output/ # Nihai veri setleri
│
├── cli.py # Komut satırı arayüzü
├── requirements.txt
└── README.md

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
🧠 Yapay Zekâ Desteği

data4tr, toplanan metinleri şu görevlerde AI yardımıyla işler:

Sınıflandırma: haber, eğitim, teknoloji, kültür vb.

Temizlik: imla hatalarını düzeltme, gereksiz ifadeleri ayıklama

Filtreleme: spam veya tekrar eden içerikleri çıkarma

Genişletme (opsiyonel): kısa metinleri anlam bozulmadan zenginleştirme

📊 Üretilen Veri Seti Formatı

Her veri kaydı aşağıdaki örneğe benzer şekilde saklanır:

{
  "id": "a94f2c8e",
  "source": "wikipedia",
  "category": "bilim",
  "text": "Fotosentez, bitkilerin güneş ışığını enerjiye dönüştürdüğü süreçtir.",
  "cleaned": true
}

⚖️ Yasal ve Etik İlkeler

data4tr yalnızca:

Açık lisanslı (CC, MIT, GNU vb.) içerikleri toplar

Kamuya açık ve ticari olmayan verileri işler

Kişisel veri veya kullanıcı içeriği barındırmaz

Amacımız Türkçe dil modellerinin gelişimini desteklemek, telif veya gizlilik ihlali yapmak değildir.

🧩 Yol Haritası

 Yeni açık kaynak sitelerin eklenmesi

 GPT tabanlı özetleme ve genişletme

 HuggingFace veri seti entegrasyonu

 Basit web arayüzü (Streamlit)

 Label Studio entegrasyonu

🤝 Katkı

Katkı yapmak isterseniz:

Repo’yu forklayın

Yeni bir branch açın

Kodunuzu ekleyip PR (Pull Request) gönderin

Topluluk katkılarına tamamen açığız.
Kodunuzu gönderirken etik veri toplama prensiplerine uymanız yeterlidir.

📜 Lisans

Bu proje MIT Lisansı ile yayımlanmıştır.
Kodunuzu ve veri setlerinizi özgürce kullanabilir, değiştirebilir ve paylaşabilirsiniz.

💬 İletişim

data4tr topluluğu yakında açık olacak.
Şimdilik öneri ve katkılarınızı GitHub Issues üzerinden iletebilirsiniz.
