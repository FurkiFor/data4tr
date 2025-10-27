"""
data4tr - CSV Export Module
Veri setini CSV formatında dışa aktaran modül.
"""

import csv
import logging
from typing import List, Dict, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVExporter:
    """CSV formatında veri seti dışa aktarma sınıfı"""

    def __init__(self, output_dir: str = "data/output"):
        """
        Args:
            output_dir: Çıktı dosyasının kaydedileceği dizin
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, data: List[Dict], filename: str = "dataset.csv") -> Path:
        """
        Veri setini CSV formatında dışa aktar

        Args:
            data: Dışa aktarılacak kayıtlar
            filename: Çıktı dosya adı

        Returns:
            Kaydedilen dosyanın yolu
        """
        output_path = self.output_dir / filename

        if not data:
            logger.warning("Boş veri seti dışa aktarılıyor")
            return output_path

        # Tüm kayıtlardan alanları topla
        fieldnames = set()
        for record in data:
            fieldnames.update(record.keys())

        fieldnames = sorted(list(fieldnames))

        logger.info(f"{len(data)} kayıt CSV formatında dışa aktarılıyor...")

        try:
            with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(data)

            logger.info(f"✓ Veri seti kaydedildi: {output_path}")
            logger.info(f"  Toplam kayıt: {len(data)}")
            logger.info(f"  Alan sayısı: {len(fieldnames)}")
            logger.info(f"  Dosya boyutu: {output_path.stat().st_size / 1024:.2f} KB")

            return output_path

        except Exception as e:
            logger.error(f"Dışa aktarma hatası: {e}")
            raise

    def export_text_only(self, data: List[Dict], filename: str = "text_dataset.csv") -> Path:
        """
        Sadece metin içeriğini dışa aktar (basitleştirilmiş CSV)

        Args:
            data: Dışa aktarılacak kayıtlar
            filename: Çıktı dosya adı

        Returns:
            Kaydedilen dosyanın yolu
        """
        output_path = self.output_dir / filename

        logger.info(f"{len(data)} metin kaydı CSV formatında dışa aktarılıyor...")

        try:
            with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "text"])  # Başlık

                for record in data:
                    record_id = record.get("id", "")
                    text = record.get("text", "")
                    writer.writerow([record_id, text])

            logger.info(f"✓ Metin veri seti kaydedildi: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Dışa aktarma hatası: {e}")
            raise


def export_to_csv(
    data: List[Dict], filename: str = "dataset.csv", output_dir: str = "data/output"
) -> Path:
    """
    Veri setini CSV formatında dışa aktar (basit API)

    Args:
        data: Dışa aktarılacak kayıtlar
        filename: Çıktı dosya adı
        output_dir: Çıktı dizini

    Returns:
        Kaydedilen dosyanın yolu
    """
    exporter = CSVExporter(output_dir)
    return exporter.export(data, filename)


def main():
    """Test ve örnek kullanım"""
    exporter = CSVExporter()

    sample_data = [
        {
            "id": "abc123",
            "source": "wikipedia",
            "category": "bilim",
            "text": "Fotosentez, bitkilerin güneş ışığını enerjiye dönüştürdüğü süreçtir.",
        },
        {
            "id": "def456",
            "source": "wikipedia",
            "category": "teknoloji",
            "text": "Yapay zeka, makine öğrenmesi alanında önemli gelişmeler kaydetmektedir.",
        },
    ]

    output_path = exporter.export(sample_data, "test_dataset.csv")

    print(f"\n✓ Örnek CSV veri seti oluşturuldu: {output_path}")

    # İçeriği göster
    print("\nİlk 2 satır:")
    with open(output_path, "r", encoding="utf-8-sig") as f:
        for i, line in enumerate(f):
            print(line.strip())
            if i >= 1:
                break


if __name__ == "__main__":
    main()
