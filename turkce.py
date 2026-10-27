"""Türkçe metin için küçük yardımcı fonksiyonlar."""

import re

UNLULER = "aeıioöuüâîû"


def kucuk_harf(metin: str) -> str:
    """Python'un lower() fonksiyonu 'I' harfini 'i' yapar; Türkçe'de 'ı' olmalı."""
    return metin.replace("I", "ı").replace("İ", "i").lower()


def cumlelere_bol(metin: str) -> list:
    """Metni . ! ? işaretlerinden sonra cümlelere böler.

    Madde işaretleri (•) de ayırıcı sayılır; aksi hâlde "• eğim • fonksiyon • ..."
    gibi kavram listeleri tek ve çok uzun bir cümle gibi görünür.
    """
    cumleler = re.split(r"(?<=[.!?])\s+|\s*•\s*", metin.strip())
    return [c for c in cumleler if c]


def kelimeler(metin: str) -> list:
    """Yalnızca harflerden oluşan kelimeleri döndürür (sayılar ve semboller hariç)."""
    return re.findall(r"[^\W\d_]+", metin)


def hece_sayisi(kelime: str) -> int:
    """Türkçe'de her hecede bir ünlü vardır, bu yüzden ünlüleri saymak yeterli."""
    return sum(1 for harf in kucuk_harf(kelime) if harf in UNLULER)
