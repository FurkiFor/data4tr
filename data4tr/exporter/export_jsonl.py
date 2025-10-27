"""
data4tr - JSONL Export Module
Veri setini JSON Lines formatında dışa aktaran modül.
"""

import json
import logging
from typing import List, Dict, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JSONLExporter:
    """JSON Lines formatında veri seti dışa aktarma sınıfı"""

    def __init__(self, output_dir: str = "data/output"):
        """
        Args:
            output_dir: Çıktı dosyasının kaydedileceği dizin
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, data: List[Dict], filename: str = "dataset.jsonl") -> Path:
        """
        Veri setini JSONL formatında dışa aktar

        Args:
            data: Dışa aktarılacak kayıtlar
            filename: Çıktı dosya adı

        Returns:
            Kaydedilen dosyanın yolu
        """
        output_path = self.output_dir / filename

        logger.info(f"{len(data)} kayıt JSONL formatında dışa aktarılıyor...")

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for record in data:
                    # Her kaydı tek satır olarak yaz
                    json.dump(record, f, ensure_ascii=False)
                    f.write("\n")

            logger.info(f"✓ Veri seti kaydedildi: {output_path}")
            logger.info(f"  Toplam kayıt: {len(data)}")
            logger.info(f"  Dosya boyutu: {output_path.stat().st_size / 1024:.2f} KB")

            return output_path

        except Exception as e:
            logger.error(f"Dışa aktarma hatası: {e}")
            raise

    def validate_schema(self, record: Dict) -> bool:
        """
        Kaydın şemaya uygun olup olmadığını kontrol et

        Args:
            record: Kontrol edilecek kayıt

        Returns:
            Geçerli ise True
        """
        required_fields = ["id", "text", "source"]

        for field in required_fields:
            if field not in record:
                logger.warning(f"Kayıt eksik alan içeriyor: {field}")
                return False

        return True

    def export_with_validation(self, data: List[Dict], filename: str = "dataset.jsonl") -> Path:
        """
        Şema kontrolü ile dışa aktar

        Args:
            data: Dışa aktarılacak kayıtlar
            filename: Çıktı dosya adı

        Returns:
            Kaydedilen dosyanın yolu
        """
        valid_data = []
        invalid_count = 0

        for record in data:
            if self.validate_schema(record):
                valid_data.append(record)
            else:
                invalid_count += 1

        if invalid_count > 0:
            logger.warning(f"{invalid_count} geçersiz kayıt atlandı")

        return self.export(valid_data, filename)


def export_to_jsonl(
    data: List[Dict], filename: str = "dataset.jsonl", output_dir: str = "data/output"
) -> Path:
    """
    Veri setini JSONL formatında dışa aktar (basit API)

    Args:
        data: Dışa aktarılacak kayıtlar
        filename: Çıktı dosya adı
        output_dir: Çıktı dizini

    Returns:
        Kaydedilen dosyanın yolu
    """
    exporter = JSONLExporter(output_dir)
    return exporter.export(data, filename)


def main():
    """Test ve örnek kullanım"""
    exporter = JSONLExporter()

    sample_data = [
        {
            "id": "abc123",
            "source": "wikipedia",
            "category": "bilim",
            "text": "Fotosentez, bitkilerin gürollerin güneş ışığını enerjiye dönüştürdüğü süreçtir.",
            "cleaned": True,
        },
        {
            "id": "def456",
            "source": "wikipedia",
            "category": "teknoloji",
            "text": "Yapay zeka, makine öğrenmesi alanında önemli gelişmeler kaydetmektedir.",
            "cleaned": True,
        },
    ]

    output_path = exporter.export(sample_data, "test_dataset.jsonl")

    print(f"\n✓ Örnek veri seti oluşturuldu: {output_path}")
    print("\nİlk satır içeriği:")
    with open(output_path, "r", encoding="utf-8") as f:
        print(f.readline())


if __name__ == "__main__":
    main()
