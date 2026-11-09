"""Kriter 4: İçerik güvenliği.

TTKB'nin inceleme kriterlerindeki "Güvenli, Etik ve Çevreci İçerik" başlığının nesnel olarak
taranabilen maddeleri:
  4.1 Kişisel veriler : T.C. kimlik numarası (resmî doğrulama algoritmasıyla), telefon, e-posta, IBAN
  4.2 Ticari unsurlar : ®/™ işaretleri, resmî olmayan web adresleri, marka listesi, satış çağrıları
  4.4 Bağımlılık      : bağımlılık yapıcı maddelere ilişkin kelimeler
  4.5 Şiddet, hakaret : şiddet ve hakaret içeren kelimeler

4.4 ve 4.5 bulguları hata değil, "kontrol edilmesi önerilen ifade"dir: bir fen kitabında alkolün kimyası
veya bir tarih kitabında savaş anlatılabilir. Kelimeler kökleriyle (zeyrek) karşılaştırılır; böylece
"biraz" kelimesi "bira", "esrarengiz" kelimesi "esrar" sanılmaz.
"""

import os
import re
from functools import lru_cache

from hata import Hata
from turkce import kucuk_harf

KRITER = "İçerik Güvenliği"
KLASOR = os.path.dirname(os.path.abspath(__file__))

# ---------------- 4.1 Kişisel veriler ----------------
TC_ADAYI = re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)")
TELEFON = re.compile(r"(?<!\d)(?:\+90[\s-]?|0)?\(?5\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)"
                     r"|(?<!\d)0\(?[2-4]\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)")
EPOSTA = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")
IBAN = re.compile(r"\bTR\d{2}(?:\s?\d{4}){5}\s?\d{2}\b")
RESMI_ALAN_ADI = re.compile(r"(\.gov\.tr|\.edu\.tr|\.k12\.tr|\.tsk\.tr|\.bel\.tr)$", re.IGNORECASE)


def tc_kimlik_gecerli_mi(no: str) -> bool:
    """T.C. kimlik numarası doğrulama algoritması (10. ve 11. haneler kontrol hanesidir)."""
    if len(no) != 11 or not no.isdigit() or no[0] == "0":
        return False
    d = [int(c) for c in no]
    onuncu = ((d[0] + d[2] + d[4] + d[6] + d[8]) * 7 - (d[1] + d[3] + d[5] + d[7])) % 10
    return d[9] == onuncu and d[10] == sum(d[:10]) % 10


def kisisel_veriler(metin: str):
    for m in TC_ADAYI.finditer(metin):
        if tc_kimlik_gecerli_mi(m.group()):
            yield m.group(), "T.C. kimlik numarası olabilecek 11 haneli sayı (doğrulama algoritmasına uyuyor)."
    for m in TELEFON.finditer(metin):
        yield m.group().strip(), "Telefon numarası."
    for m in EPOSTA.finditer(metin):
        if not RESMI_ALAN_ADI.search(m.group(1)):
            yield m.group(), "Kişisel olabilecek e-posta adresi."
    for m in IBAN.finditer(metin):
        yield m.group(), "IBAN numarası."


# ---------------- 4.2 Ticari unsurlar ----------------
WEB_ADRESI = re.compile(r"\b(?:https?://|www\.)([\w.-]+\.[a-z]{2,})(?:/\S*)?", re.IGNORECASE)
TICARI_ISARET = re.compile(r"[®™]")
SATIS_CAGRISI = re.compile(r"\b(satın alın|hemen alın|sipariş verin|kaçırmayın|stoklarla sınırlı)\b", re.IGNORECASE)


def _liste_oku(dosya_adi: str) -> list:
    yol = os.path.join(KLASOR, dosya_adi)
    if not os.path.exists(yol):
        return []
    with open(yol, encoding="utf-8") as f:
        return [s.strip() for s in f if s.strip() and not s.lstrip().startswith("#")]


MARKALAR = _liste_oku("marka_listesi.txt")
MARKA_DESENI = re.compile(r"(?<![^\W_])(" + "|".join(re.escape(m) for m in MARKALAR) + r")(?![^\W_])") \
    if MARKALAR else None


def ticari_unsurlar(metin: str):
    for m in WEB_ADRESI.finditer(metin):
        if not RESMI_ALAN_ADI.search(m.group(1)):
            yield m.group(), "Resmî kurum dışı web adresi (ticari yönlendirme olabilir)."
    for m in TICARI_ISARET.finditer(metin):
        yield metin[max(0, m.start() - 20):m.end()].strip(), "Tescilli marka işareti (® / ™)."
    if MARKA_DESENI:
        for m in MARKA_DESENI.finditer(metin):
            yield m.group(), "Marka adı (ticari tercih veya yönlendirme olabilir)."
    for m in SATIS_CAGRISI.finditer(metin):
        yield m.group(), "Satışa yönlendiren ifade."


# ---------------- 4.4 / 4.5 Hassas ifadeler ----------------
def _hassas_sozluk() -> dict:
    """hassas_ifadeler.txt: her satırda "madde kök" (ör. "4.4 sigara"). Kökler zeyrek'in verdiği köklerdir."""
    sozluk = {}
    for satir in _liste_oku("hassas_ifadeler.txt"):
        madde, _, kok = satir.partition(" ")
        if kok:
            sozluk[kucuk_harf(kok.strip())] = madde
    return sozluk


HASSAS = _hassas_sozluk()
HASSAS_ACIKLAMA = {
    "4.4": "Bağımlılık yapıcı maddeye ilişkin ifade; yaş düzeyine ve bağlama uygunluğu kontrol edilmeli.",
    "4.5": "Şiddet veya hakaret içerebilecek ifade; bağlama uygunluğu kontrol edilmeli.",
}


@lru_cache(maxsize=None)
def kokler(kelime: str) -> frozenset:
    from yazim_denetimi import cozumleyici
    analiz = cozumleyici().analyze(kelime)
    return frozenset(kucuk_harf(p.lemma) for p in (analiz[0] if analiz else []) if p.lemma != "Unk")


def hassas_ifadeler(metin: str):
    for kelime in set(re.findall(r"[^\W\d_]{3,}", metin)):
        kucuk = kucuk_harf(kelime)
        if kucuk in HASSAS:
            yield HASSAS[kucuk], kelime
            continue
        bulunan_kokler = kokler(kucuk)
        # Kelimenin kendisi sözlükte ayrı bir kökse ("içkin"), başka bir kökten türetilmiş sayılmaz ("içki"+n)
        if kucuk in bulunan_kokler:
            continue
        madde = next((HASSAS[k] for k in bulunan_kokler if k in HASSAS), None)
        if madde:
            yield madde, kelime


# ---------------- Denetim ----------------
def denetle(paragraf) -> list:
    hatalar = []
    for alinti, aciklama in kisisel_veriler(paragraf.metin):
        hatalar.append(Hata(paragraf.sayfa, paragraf.paragraf_no, KRITER, "[4.1] " + aciklama, alinti,
                            "Kişisel veri içermemesi için gerçek olmayan bir örnekle değiştirin."))
    for alinti, aciklama in ticari_unsurlar(paragraf.metin):
        hatalar.append(Hata(paragraf.sayfa, paragraf.paragraf_no, KRITER, "[4.2] " + aciklama, alinti,
                            "Ticari tercih veya yönlendirme oluşturmadığını kontrol edin."))
    for madde, kelime in hassas_ifadeler(paragraf.metin):
        hatalar.append(Hata(paragraf.sayfa, paragraf.paragraf_no, KRITER, f"[{madde}] {HASSAS_ACIKLAMA[madde]}",
                            kelime, "İfadenin bağlamını kontrol edin."))
    return hatalar
