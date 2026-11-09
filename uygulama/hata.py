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
    konum: tuple = None # paragrafın sayfadaki dikdörtgeni (x0, y0, x1, y1); arayüzde işaretlemek için
