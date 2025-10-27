"""
data4tr - Processor Module
AI ile metin işleme ve etiketleme modülü.
"""

from .classify import TextClassifier, classify_batch
from .deduplicate import Deduplicator, remove_exact_duplicates
from .normalize import TextNormalizer, normalize_batch

__all__ = [
    'TextClassifier', 
    'classify_batch',
    'Deduplicator',
    'remove_exact_duplicates',
    'TextNormalizer',
    'normalize_batch'
]

