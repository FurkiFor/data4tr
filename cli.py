"""
data4tr - Command Line Interface
Türkçe veri seti oluşturma için komut satırı arayüzü.
"""

import argparse
import sys
import logging
from pathlib import Path

# Modülleri import et
from scraper.scraper import Scraper
from scraper.cleaner import TextCleaner
from processor.classify import TextClassifier
from processor.deduplicate import Deduplicator
from processor.normalize import TextNormalizer
from exporter.export_jsonl import JSONLExporter
from exporter.export_csv import CSVExporter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def scrape_command(args):
    """Veri toplama komutu"""
    logger.info(f"Kaynak: {args.source}, Limit: {args.limit}")

    scraper = Scraper()
    cleaner = TextCleaner()

    # Veri çek
    articles = scraper.scrape_source(args.source, limit=args.limit)

    if not articles:
        logger.error("Veri çekilemedi!")
        return

    # Temizle
    logger.info("Metinler temizleniyor...")
    for article in articles:
        if "text" in article:
            article["text"] = cleaner.destructive_clean(article["text"])
            article["cleaned"] = True
        else:
            article["cleaned"] = False

    # Kaydet
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    import json

    output_file = output_dir / f"{args.source}_{args.limit}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    logger.info(f"✓ {len(articles)} kayıt kaydedildi: {output_file}")
    print(f"\n✓ Veri toplama tamamlandı!")
    print(f"  Kayıt sayısı: {len(articles)}")
    print(f"  Dosya: {output_file}")


def process_command(args):
    """AI ile işleme komutu"""
    logger.info("Metinler işleniyor...")

    # Ham veriyi yükle
    import json
    from glob import glob

    raw_files = glob("data/raw/*.json")
    if not raw_files:
        logger.error("Ham veri bulunamadı! Önce 'scrape' komutunu çalıştırın.")
        return

    # En son dosyayı kullan
    latest_file = max(raw_files, key=lambda x: Path(x).stat().st_mtime)
    logger.info(f"Yüklenen dosya: {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Sınıflandır
    logger.info("Metinler sınıflandırılıyor...")
    classifier = TextClassifier(model=args.model)
    for record in data:
        if "text" in record:
            record["category"] = classifier.classify(record["text"])

    # Duplicate temizliği
    logger.info("Duplicate kayıtlar temizleniyor...")
    deduplicator = Deduplicator()
    data = deduplicator.remove_duplicates(data)

    # Normalize
    logger.info("Metinler normalize ediliyor...")
    normalizer = TextNormalizer()
    for record in data:
        if "text" in record:
            record["text"] = normalizer.normalize(record["text"])

    # Kaydet
    cleaned_dir = Path("data/cleaned")
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    output_file = cleaned_dir / "processed_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"✓ {len(data)} kayıt işlendi ve kaydedildi: {output_file}")
    print(f"\n✓ İşleme tamamlandı!")
    print(f"  Kayıt sayısı: {len(data)}")
    print(f"  Dosya: {output_file}")


def export_command(args):
    """Veri seti dışa aktarma komutu"""
    logger.info(f"Format: {args.format}")

    # İşlenmiş veriyi yükle
    import json

    cleaned_file = Path("data/cleaned/processed_data.json")
    if not cleaned_file.exists():
        logger.error("İşlenmiş veri bulunamadı! Önce 'process' komutunu çalıştırın.")
        return

    with open(cleaned_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Dışa aktar
    if args.format == "jsonl":
        exporter = JSONLExporter()
        output_path = exporter.export(data, "dataset.jsonl")
    elif args.format == "csv":
        exporter = CSVExporter()
        output_path = exporter.export(data, "dataset.csv")
    else:
        logger.error(f"Desteklenmeyen format: {args.format}")
        return

    print(f"\n✓ Veri seti dışa aktarıldı!")
    print(f"  Format: {args.format}")
    print(f"  Kayıt sayısı: {len(data)}")
    print(f"  Dosya: {output_path}")


def main():
    """Ana CLI fonksiyonu"""
    parser = argparse.ArgumentParser(
        description="data4tr - Türkçe veri seti oluşturma aracı",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek kullanımlar:
  # Wikipedia'dan 100 sayfa çek
  python cli.py scrape --source wikipedia --limit 100
  
  # AI ile işle
  python cli.py process --model gpt-4
  
  # JSONL formatında dışa aktar
  python cli.py export --format jsonl
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Komutlar")

    # Scrape komutu
    scrape_parser = subparsers.add_parser("scrape", help="Veri topla")
    scrape_parser.add_argument(
        "--source", type=str, default="wikipedia", help="Veri kaynağı (default: wikipedia)"
    )
    scrape_parser.add_argument(
        "--limit", type=int, default=100, help="Maksimum kayıt sayısı (default: 100)"
    )

    # Process komutu
    process_parser = subparsers.add_parser("process", help="Veriyi işle")
    process_parser.add_argument(
        "--model", type=str, default="rule-based", help="AI modeli (default: rule-based)"
    )

    # Export komutu
    export_parser = subparsers.add_parser("export", help="Veri setini dışa aktar")
    export_parser.add_argument(
        "--format",
        type=str,
        default="jsonl",
        choices=["jsonl", "csv"],
        help="Dışa aktarma formatı (default: jsonl)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Komutu çalıştır
    if args.command == "scrape":
        scrape_command(args)
    elif args.command == "process":
        process_command(args)
    elif args.command == "export":
        export_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
