"""Türkçe için geliştirilmiş üç okunabilirlik formülü.

Türkiye'de ders kitaplarının okunabilirliğini inceleyen çalışmalarda bu üç formül birlikte
kullanılır; formüller farklı sonuç verebildiği için tek başına birine güvenilmez.

  Ateşman (1997):        198,825 - 40,175 x (hece/kelime) - 2,610 x (kelime/cümle)
  Çetinkaya-Uzun (2010): 118,823 - 25,987 x (hece/kelime) - 0,971 x (kelime/cümle)
  Bezirci-Yılmaz (2010): YOD = √(OKS x ((H3 x 0,84) + (H4 x 1,5) + (H5 x 3,5) + (H6 x 26,25)))
      OKS: cümle başına ortalama kelime sayısı
      H3..H6: cümle başına ortalama 3, 4, 5 ve 6+ heceli kelime sayısı
"""

import math

from turkce import cumlelere_bol, hece_sayisi, kelimeler


def istatistik(metin: str) -> dict:
    kelime_listesi = kelimeler(metin)
    cumle = max(1, len(cumlelere_bol(metin)))
    heceler = [hece_sayisi(k) for k in kelime_listesi]
    return {
        "kelime": len(kelime_listesi),
        "cumle": cumle,
        "hece": sum(heceler),
        "h3": sum(1 for h in heceler if h == 3),
        "h4": sum(1 for h in heceler if h == 4),
        "h5": sum(1 for h in heceler if h == 5),
        "h6": sum(1 for h in heceler if h >= 6),
    }


def _sinirla(puan: float) -> float:
    return max(0.0, min(100.0, puan))


def atesman(s: dict) -> float:
    if not s["kelime"]:
        return 100.0
    return _sinirla(198.825 - 40.175 * (s["hece"] / s["kelime"]) - 2.610 * (s["kelime"] / s["cumle"]))


def cetinkaya_uzun(s: dict) -> float:
    if not s["kelime"]:
        return 100.0
    return _sinirla(118.823 - 25.987 * (s["hece"] / s["kelime"]) - 0.971 * (s["kelime"] / s["cumle"]))


def bezirci_yilmaz(s: dict) -> float:
    c = s["cumle"]
    oks = s["kelime"] / c
    return math.sqrt(oks * (s["h3"] / c * 0.84 + s["h4"] / c * 1.5 + s["h5"] / c * 3.5 + s["h6"] / c * 26.25))


def atesman_duzeyi(puan: float) -> str:
    for sinir, ad in [(90, "Çok kolay"), (70, "Kolay"), (50, "Orta güçlükte"), (30, "Zor")]:
        if puan >= sinir:
            return ad
    return "Çok zor"


def cetinkaya_duzeyi(puan: float) -> str:
    if puan >= 51:
        return "Bağımsız okuma (5.-7. Sınıf)"
    if puan >= 35:
        return "Eğitsel okuma (8.-9. Sınıf)"
    return "Engelli düzey (10.-12. Sınıf)"


def bezirci_duzeyi(yod: float) -> str:
    if yod <= 8:
        return "İlköğretim"
    if yod <= 12:
        return "Lise"
    if yod <= 16:
        return "Lisans"
    return "Akademik"


EN_AZ_KELIME = 15          # çok kısa paragraflarda formüller güvenilir sonuç vermez


def yod_ust_siniri(sinif: int) -> int:
    """Bezirci-Yılmaz tablosuna göre kitabın kademesinin üst sınırı: İlköğretim 1-8, Lise 9-12."""
    return 8 if sinif <= 8 else 12


def kitap_ozeti(paragraflar, sinif: int) -> dict:
    """Kitabın bütünü için üç formülün sonucu ve Bezirci-Yılmaz'a göre kitabın kademesinin (İlköğretim/Lise)
    üstünde kalan paragrafların sayısı."""
    ust_sinir = yod_ust_siniri(sinif)
    toplam = {"kelime": 0, "cumle": 0, "hece": 0, "h3": 0, "h4": 0, "h5": 0, "h6": 0}
    olculen, ustunde = 0, 0
    for p in paragraflar:
        s = istatistik(p.metin)
        for anahtar in toplam:
            toplam[anahtar] += s[anahtar]
        if s["kelime"] >= EN_AZ_KELIME:
            olculen += 1
            if bezirci_yilmaz(s) > ust_sinir:
                ustunde += 1
    toplam["cumle"] = max(1, toplam["cumle"])
    a, c, b = atesman(toplam), cetinkaya_uzun(toplam), bezirci_yilmaz(toplam)
    return {
        "atesman": a, "atesman_duzeyi": atesman_duzeyi(a),
        "cetinkaya_uzun": c, "cetinkaya_duzeyi": cetinkaya_duzeyi(c),
        "bezirci_yilmaz": b, "bezirci_duzeyi": bezirci_duzeyi(b),
        "olculen_paragraf": olculen, "seviye_ustu_paragraf": ustunde,
        "ortalama_cumle": toplam["kelime"] / toplam["cumle"],
        "ortalama_hece": toplam["hece"] / max(1, toplam["kelime"]),
    }
