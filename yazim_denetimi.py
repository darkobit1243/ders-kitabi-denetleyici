"""Kriter 1: Yazım ve noktalama hataları.

Üç tür kontrol yapılır:
  1. Sık yapılan yazım hataları listesi (ör. "herkez" -> "herkes")
  2. Türkçe sözlükte bulunmayan kelimeler (zeyrek biçimbilim çözümleyicisi ile)
  3. Basit noktalama kuralları (virgülden önce boşluk, virgülden sonra boşluk yok vb.)
"""

import logging
import os
import re
from functools import lru_cache

from hata import Hata
from turkce import kucuk_harf

KRITER = "Yazım"

# TDK'ye göre sık yapılan yazım hataları: yanlış -> doğru
BILINEN_HATALAR = {
    "herkez": "herkes",
    "yalnış": "yanlış",
    "yanlız": "yalnız",
    "birşey": "bir şey",
    "herşey": "her şey",
    "hiçbirşey": "hiçbir şey",
    "şuan": "şu an",
    "malesef": "maalesef",
    "orjinal": "orijinal",
    "yada": "ya da",
    "tabiki": "tabii ki",
    "herhangibir": "herhangi bir",
    "pekçok": "pek çok",
    "deyil": "değil",
    "süpriz": "sürpriz",
    "makina": "makine",
    "traş": "tıraş",
}

# zeyrek sözlüğünde eksik olan ama doğru yazılmış kelimeler (ek_sozluk.txt, her satıra bir kelime)
EK_SOZLUK_DOSYASI = os.path.join(os.path.dirname(__file__), "ek_sozluk.txt")
EK_SOZLUK = set()
if os.path.exists(EK_SOZLUK_DOSYASI):
    with open(EK_SOZLUK_DOSYASI, encoding="utf-8") as f:
        EK_SOZLUK = {kucuk_harf(s.strip()) for s in f if s.strip() and not s.startswith("#")}

# Noktalama kuralları: (desen, açıklama)
NOKTALAMA_KURALLARI = [
    # İki tarafında da gerçek kelime olmalı; aksi hâlde formül parçalarında ("A x ,x ,x") sahte hata çıkıyor
    (re.compile(r"[^\W\d_]{2,}\s+[,;:!?](?=\s+[^\W\d_]{2,})"), "Noktalama işaretinden önce boşluk bırakılmaz."),
    (re.compile(r"[^\W\d_][,;][^\W\d_\s]"), "Virgül veya noktalı virgülden sonra boşluk bırakılmalıdır."),
    (re.compile(r"\b(ve|ile|için|ama|fakat)\s+\1\b", re.IGNORECASE), "Aynı bağlaç arka arkaya iki kez yazılmış."),
]

_cozumleyici = None


def zeyrek_hatasini_duzelt():
    """zeyrek 0.1.3'teki bir hatayı giderir.

    zeyrek, kelimeleri çözümlerken ortak kullanılan "ses özellikleri" kümelerini
    (set) kopyalamadan değiştiriyor. Bu yüzden bir kelimenin çözümlenmesi sonraki
    kelimelerin sonucunu bozuyordu: "olacak" çözümlendikten sonra "olup" kelimesi
    tanınmaz hâle geliyordu. Kümelerin değiştirildiği iki yer var:
      1. calculate_phonetic_attributes: lru_cache ile saklanan set'i döndürüyor
      2. SearchPath.initial: kökün kendi set'ini kopyalamadan kullanıyor
    Çözüm: iki yerde de set'in bir kopyasını vermek.
    """
    import zeyrek.attributes
    import zeyrek.morphotactics
    import zeyrek.rulebasedanalyzer

    orijinal_hesapla = zeyrek.attributes.calculate_phonetic_attributes

    def kopya_dondur(*args, **kwargs):
        return set(orijinal_hesapla(*args, **kwargs))

    zeyrek.morphotactics.calculate_phonetic_attributes = kopya_dondur
    zeyrek.rulebasedanalyzer.calculate_phonetic_attributes = kopya_dondur

    arama_yolu = zeyrek.morphotactics.SearchPath
    orijinal_baslangic = arama_yolu.initial.__func__

    def baslangic_kopyali(cls, stem_transition, tail):
        yol = orijinal_baslangic(cls, stem_transition, tail)
        yol.phonetic_attributes = set(yol.phonetic_attributes)
        return yol

    arama_yolu.initial = classmethod(baslangic_kopyali)


def cozumleyici():
    """zeyrek'in yüklenmesi birkaç saniye sürdüğü için yalnızca ilk ihtiyaçta yüklenir."""
    global _cozumleyici
    if _cozumleyici is None:
        logging.getLogger("zeyrek").setLevel(logging.ERROR)
        import zeyrek
        zeyrek_hatasini_duzelt()
        _cozumleyici = zeyrek.MorphAnalyzer()
    return _cozumleyici


@lru_cache(maxsize=None)
def sozlukte_var_mi(kelime: str) -> bool:
    """Aynı kelime kitapta yüzlerce kez geçebilir; lru_cache sonucu hatırlar."""
    sonuc = cozumleyici().analyze(kelime)
    return bool(sonuc and sonuc[0]) and sonuc[0][0].pos != "Unk"


def kontrol_edilecek_mi(kelime: str) -> bool:
    """Sözlük kontrolünde yanlış alarm verebilecek kelimeleri atlar."""
    if len(kelime) < 3:
        return False                      # a, b, x gibi değişkenler
    if kelime[0].isupper():
        return False                      # özel isimler, cümle başı, kısaltmalar
    if any(harf in "qwx" for harf in kelime.lower()):
        return False                      # Türkçe'de olmayan harfler: yabancı kelime
    return True


KESME_ISARETLERI = "'’ʼ"   # kitaplarda üç farklı kesme işareti karakteri kullanılabiliyor


def kelimeleri_ayir(metin: str):
    """Metni boşluklardan böler; her parça için (önceki parça, kelime, sonraki parça) döndürür.

    Kesme işaretinden sonraki ek atılır: "Ankara'da" -> "Ankara".
    """
    parcalar = metin.split()
    for i, parca in enumerate(parcalar):
        if parca.endswith("-"):
            continue        # paragraf sonunda yarım kalmış kelime ("prob-")
        if re.search("[-]", parca):
            continue        # PDF fontunun özel karakteri: harf doğru okunamamış ("bedhahlarn")
        kelime = re.split(f"[{KESME_ISARETLERI}]", parca)[0]
        kelime = re.sub(r"^[^\w]+|[^\w]+$", "", kelime)      # baştaki/sondaki noktalamayı at
        if not kelime or not re.fullmatch(r"[^\W\d_]+", kelime):
            continue
        onceki = parcalar[i - 1] if i > 0 else ""
        sonraki = re.sub(r"[^\w]+$", "", parcalar[i + 1]) if i + 1 < len(parcalar) else ""
        yield onceki, kelime, sonraki


def sahte_hata_mi(onceki: str, kelime: str, sonraki: str) -> bool:
    """PDF'ten metin çıkarılırken oluşan, kitapta gerçekte olmayan "hataları" ayıklar."""
    # Matematikte değişkene veya sayıya eklenen ek: "b nin", "x ten", "3 ün"
    if len(onceki) == 1 or (onceki and onceki[-1].isdigit()):
        return True
    # Satır sonunda tiresi kaybolmuş bölünmüş kelime: "fonk siyonların", "yü rütebilmeniz"
    if onceki.isalpha() and sozlukte_var_mi(kucuk_harf(onceki + kelime)):
        return True
    if sonraki.isalpha() and sozlukte_var_mi(kucuk_harf(kelime + sonraki)):
        return True
    return False


INGILIZCE_KELIMELER = {"the", "of", "and", "in", "to", "for", "with", "on", "is", "from"}


def ingilizce_mi(metin: str) -> bool:
    """Kaynakça gibi İngilizce bölümleri Türkçe sözlükle denetlememek için."""
    kelimeler = re.findall(r"[a-z]+", metin.lower())
    return sum(1 for k in kelimeler if k in INGILIZCE_KELIMELER) >= 2


def denetle(paragraf) -> list:
    hatalar = []
    metin = paragraf.metin
    # OCR ile okunan sayfalarda harfler yanlış okunabildiği için sözlük kontrolü yapılmaz
    sozluk_kontrolu = not paragraf.ocr and not ingilizce_mi(metin)

    for onceki, kelime, sonraki in kelimeleri_ayir(metin):
        kucuk = kucuk_harf(kelime)
        if kucuk in BILINEN_HATALAR:
            hatalar.append(Hata(paragraf.sayfa, paragraf.paragraf_no, KRITER,
                                "Yanlış yazılmış kelime.", kelime, BILINEN_HATALAR[kucuk]))
        elif (sozluk_kontrolu and kontrol_edilecek_mi(kelime) and kucuk not in EK_SOZLUK
              and not sozlukte_var_mi(kucuk) and not sahte_hata_mi(onceki, kelime, sonraki)):
            hatalar.append(Hata(paragraf.sayfa, paragraf.paragraf_no, KRITER,
                                "Türkçe sözlükte bulunamayan kelime (olası yazım hatası).", kelime))

    for desen, aciklama in NOKTALAMA_KURALLARI:
        for eslesme in desen.finditer(metin):
            bas, son = max(0, eslesme.start() - 15), eslesme.end() + 15
            hatalar.append(Hata(paragraf.sayfa, paragraf.paragraf_no, KRITER,
                                aciklama, "..." + metin[bas:son] + "..."))
    return hatalar
