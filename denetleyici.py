"""Bütün adımları birleştirir: PDF'i oku -> denetlenecek paragrafları seç -> kriterleri uygula."""

import yas_seviyesi
import yazim_denetimi
from metin_filtresi import incelenebilir_mi
from pdf_okuyucu import paragraflari_cikar


def kitabi_denetle(pdf_yolu: str, sinif: int):
    paragraflar, metinsiz_sayfalar = paragraflari_cikar(pdf_yolu)
    incelenecekler = [p for p in paragraflar if incelenebilir_mi(p.metin)]

    hatalar = []
    for p in incelenecekler:
        bulunanlar = yazim_denetimi.denetle(p) + yas_seviyesi.denetle(p, sinif)
        for h in bulunanlar:
            h.konum = p.konum
        hatalar += bulunanlar

    istatistik = {
        "toplam_paragraf": len(paragraflar),
        "incelenen_paragraf": len(incelenecekler),
        "atlanan_paragraf": len(paragraflar) - len(incelenecekler),
        "metinsiz_sayfalar": metinsiz_sayfalar,
    }
    return hatalar, istatistik
