"""PDF ders kitabından metni sayfa ve paragraf bilgisiyle birlikte çıkarır."""

import json
import os
import re
from dataclasses import dataclass

import pymupdf

TESSDATA = r"C:\Program Files\Tesseract-OCR\tessdata"   # Tesseract dil dosyaları
OCR_DILI = "tur+eng"
ONBELLEK_KLASORU = ".onbellek"


@dataclass
class Paragraf:
    sayfa: int          # 1'den başlayan sayfa numarası
    paragraf_no: int    # sayfa içindeki sıra (1'den başlar)
    metin: str
    konum: tuple        # (x0, y0, x1, y1) sayfa üzerindeki dikdörtgen
    ocr: bool = False   # metin OCR ile mi okundu? (OCR hatalı okuyabilir)


def satirlari_birlestir(blok_metni: str) -> str:
    """Bir bloğun satırlarını tek paragraf metnine çevirir.

    Satır sonunda tireyle bölünmüş kelimeleri birleştirir:
    "öğren-\\nciler" -> "öğrenciler"
    """
    # \xad = yumuşak tire: dizgi programlarının satır sonunda kelimeyi böldüğü görünmez tire
    blok_metni = blok_metni.replace("\xad", "-")
    satirlar = [s.strip() for s in blok_metni.splitlines() if s.strip()]
    metin = ""
    for satir in satirlar:
        if metin.endswith("-") and satir[:1].islower():
            metin = metin[:-1] + satir          # tireli kelimeyi birleştir
        elif metin:
            metin += " " + satir
        else:
            metin = satir
    return re.sub(r"\s+", " ", metin)


def sayfa_numarasi_mi(metin: str) -> bool:
    """Yalnızca sayı içeren kısa blokları (ör. sayfa numarası) ayıklamak için."""
    return metin.isdigit() and len(metin) <= 4


def bloklari_paragraflara_birlestir(bloklar):
    """Bazı PDF'lerde her satır ayrı bir blok olur. Alt alta duran blokları birleştirir.

    Bir sonraki blok, öncekinin hemen altındaysa (arada boş satır yoksa) ve
    içeri girintili değilse aynı paragrafın devamı sayılır.
    """
    gruplar = []   # her eleman: [x0, y0, x1, y1, metin, satir_sayisi]
    for x0, y0, x1, y1, metin, _blok_no, blok_tipi in bloklar:
        if blok_tipi != 0 or not metin.strip():   # 0 = metin, 1 = resim
            continue
        satir_sayisi = max(1, len(metin.strip().splitlines()))
        if gruplar:
            onceki = gruplar[-1]
            satir_yuksekligi = (onceki[3] - onceki[1]) / onceki[5]
            bosluk = y0 - onceki[3]
            girintili = x0 - onceki[0] > 8
            if 0 <= bosluk < satir_yuksekligi * 0.6 and not girintili and abs(x0 - onceki[0]) < 40:
                onceki[1:4] = [min(onceki[1], y0), max(onceki[2], x1), max(onceki[3], y1)]
                onceki[4] += "\n" + metin
                onceki[5] += satir_sayisi
                continue
        gruplar.append([x0, y0, x1, y1, metin, satir_sayisi])
    return gruplar


def metin_var_mi(bloklar) -> bool:
    return any(b[6] == 0 and b[4].strip() for b in bloklar)


def ocr_ile_oku(sayfa):
    """Resim olan sayfayı Tesseract ile okuyup blok listesi döndürür."""
    textpage = sayfa.get_textpage_ocr(language=OCR_DILI, dpi=300, full=True, tessdata=TESSDATA)
    return sayfa.get_text("blocks", sort=True, textpage=textpage)


def onbellek_yolu(pdf_yolu: str) -> str:
    """OCR sonuçlarının kaydedileceği dosya. Dosya boyutu da isme eklenir,
    böylece aynı adlı farklı bir PDF eski sonuçları kullanmaz."""
    ad = os.path.splitext(os.path.basename(pdf_yolu))[0]
    boyut = os.path.getsize(pdf_yolu)
    return os.path.join(ONBELLEK_KLASORU, f"{ad}_{boyut}.json")


def paragraflari_cikar(pdf_yolu: str, ocr_kullan: bool = True):
    """PDF'teki tüm paragrafları ve metin bulunamayan sayfaları döndürür.

    Metin içermeyen (resim/taranmış) sayfalar ocr_kullan=True ise OCR ile okunur.
    OCR sonuçları .onbellek klasörüne kaydedilir, ikinci çalıştırmada tekrar OCR yapılmaz.
    """
    ocr_kullan = ocr_kullan and os.path.isdir(TESSDATA)
    paragraflar = []
    metinsiz_sayfalar = []

    onbellek_dosyasi = onbellek_yolu(pdf_yolu)
    onbellek = {}
    if os.path.exists(onbellek_dosyasi):
        with open(onbellek_dosyasi, encoding="utf-8") as f:
            onbellek = json.load(f)
    onbellek_degisti = False

    with pymupdf.open(pdf_yolu) as belge:
        for sayfa_index, sayfa in enumerate(belge):
            sayfa_no = sayfa_index + 1
            # sort=True: blokları okuma sırasına (yukarıdan aşağıya, soldan sağa) dizer
            bloklar = sayfa.get_text("blocks", sort=True)
            ocr_sayfasi = False

            if not metin_var_mi(bloklar) and ocr_kullan and sayfa.get_images():
                ocr_sayfasi = True
                anahtar = str(sayfa_no)        # JSON anahtarları metin olmak zorunda
                if anahtar not in onbellek:
                    print(f"OCR: sayfa {sayfa_no}/{len(belge)}", end="\r")
                    onbellek[anahtar] = ocr_ile_oku(sayfa)
                    onbellek_degisti = True
                bloklar = onbellek[anahtar]

            paragraf_no = 0
            for x0, y0, x1, y1, blok_metni, _ in bloklari_paragraflara_birlestir(bloklar):
                metin = satirlari_birlestir(blok_metni)
                if not metin or sayfa_numarasi_mi(metin):
                    continue
                paragraf_no += 1
                paragraflar.append(Paragraf(sayfa_no, paragraf_no, metin, (x0, y0, x1, y1), ocr_sayfasi))

            if paragraf_no == 0:
                metinsiz_sayfalar.append(sayfa_no)

    if onbellek_degisti:
        os.makedirs(ONBELLEK_KLASORU, exist_ok=True)
        with open(onbellek_dosyasi, "w", encoding="utf-8") as f:
            json.dump(onbellek, f, ensure_ascii=False)

    return paragraflar, metinsiz_sayfalar
