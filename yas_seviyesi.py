"""Kriter 3: Yaş seviyesine uygunluk.

Ateşman Okunabilirlik Formülü (Ateşman, 1997) Türkçe metinler için geliştirilmiştir:

    Puan = 198,825 - 40,175 x (hece sayısı / kelime sayısı) - 2,610 x (kelime sayısı / cümle sayısı)

Kelimeler ne kadar uzun (çok heceli) ve cümleler ne kadar uzunsa puan o kadar düşer.
  90-100 çok kolay | 70-89 kolay | 50-69 orta | 30-49 zor | 0-29 çok zor
"""

from hata import Hata
from turkce import cumlelere_bol, hece_sayisi, kelimeler

KRITER = "Yaş seviyesi"

# Sınıf düzeyine göre beklenen en düşük Ateşman puanı ve en uzun cümle (kelime sayısı).
# Bu eşikleri projede biz belirledik: küçük sınıflarda daha kolay metin bekleniyor.
SEVIYELER = [
    (range(1, 5), 70, 12),    # İlkokul (1-4. sınıf): kolay metin, kısa cümleler
    (range(5, 9), 50, 18),    # Ortaokul (5-8. sınıf): orta zorluk
    (range(9, 13), 30, 25),   # Lise (9-12. sınıf): zor metin kabul edilebilir
]

EN_AZ_KELIME = 15   # çok kısa paragraflarda formül güvenilir sonuç vermez


def esikler(sinif: int):
    for siniflar, en_dusuk_puan, en_uzun_cumle in SEVIYELER:
        if sinif in siniflar:
            return en_dusuk_puan, en_uzun_cumle
    raise ValueError("Sınıf 1 ile 12 arasında olmalı.")


def atesman_puani(metin: str) -> float:
    kelime_listesi = kelimeler(metin)
    cumle_sayisi = max(1, len(cumlelere_bol(metin)))
    if not kelime_listesi:
        return 100.0
    hece = sum(hece_sayisi(k) for k in kelime_listesi)
    puan = 198.825 - 40.175 * (hece / len(kelime_listesi)) - 2.610 * (len(kelime_listesi) / cumle_sayisi)
    return max(0.0, min(100.0, puan))


def zorluk_adi(puan: float) -> str:
    if puan >= 90:
        return "çok kolay"
    if puan >= 70:
        return "kolay"
    if puan >= 50:
        return "orta"
    if puan >= 30:
        return "zor"
    return "çok zor"


def isim_listesi_mi(kelime_listesi) -> bool:
    """Kelimelerin yarısından fazlası büyük harfle başlıyorsa bu bir cümle değil,
    yazar/kurul listesi veya başlıktır (ör. "Yazarlar Cem DEMİRCİ Dilek HABALI ...")."""
    buyuk = sum(1 for k in kelime_listesi if k[0].isupper())
    return buyuk > len(kelime_listesi) / 2


def denetle(paragraf, sinif: int) -> list:
    hatalar = []
    en_dusuk_puan, en_uzun_cumle = esikler(sinif)

    # 1) Çok uzun cümleler
    for cumle in cumlelere_bol(paragraf.metin):
        kelime_listesi = kelimeler(cumle)
        kelime_sayisi = len(kelime_listesi)
        if kelime_sayisi > en_uzun_cumle and not isim_listesi_mi(kelime_listesi):
            hatalar.append(Hata(
                paragraf.sayfa, paragraf.paragraf_no, KRITER,
                f"Cümle çok uzun: {kelime_sayisi} kelime ({sinif}. sınıf için en fazla {en_uzun_cumle} önerilir).",
                cumle, "Cümleyi birkaç kısa cümleye bölün."))

    # 2) Paragrafın genel okunabilirliği
    if len(kelimeler(paragraf.metin)) >= EN_AZ_KELIME:
        puan = atesman_puani(paragraf.metin)
        if puan < en_dusuk_puan:
            hatalar.append(Hata(
                paragraf.sayfa, paragraf.paragraf_no, KRITER,
                f"Okunabilirlik puanı {puan:.0f} ({zorluk_adi(puan)}); {sinif}. sınıf için en az "
                f"{en_dusuk_puan} beklenir.",
                paragraf.metin[:150] + ("..." if len(paragraf.metin) > 150 else ""),
                "Daha kısa cümleler ve daha az heceli, tanıdık kelimeler kullanın."))
    return hatalar
