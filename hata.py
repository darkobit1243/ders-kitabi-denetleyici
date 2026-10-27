"""Bütün denetimlerin ortak kullandığı hata yapısı."""

from dataclasses import dataclass


@dataclass
class Hata:
    sayfa: int
    paragraf_no: int
    kriter: str         # "Yazım", "Yaş seviyesi" veya "Tutarlılık"
    aciklama: str       # hatanın ne olduğu
    alinti: str         # metinde hatanın geçtiği kısım
    oneri: str = ""     # varsa doğru yazım / öneri
