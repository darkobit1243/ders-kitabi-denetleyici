"""Kriter 2: Bilgi tutarlılığı.

Diğer kriterlerden farkı, paragrafları tek tek değil bütün kitabı birlikte incelemesidir.
İki tür tutarsızlık aranır:

  1. Çelişen sayısal bilgiler: aynı bilgi kitabın iki yerinde farklı sayılarla verilmiş.
     "Dünyadaki suyun yaklaşık %97'si okyanuslarda bulunur." <-> "... %87'si okyanuslardadır."
  2. Yazım birliği: aynı kelime kitap içinde farklı biçimlerde yazılmış
     ("hiçbir" / "hiç bir", "e-posta" / "eposta").
"""

import re
from collections import Counter, defaultdict

from hata import Hata
from turkce import cumlelere_bol, kucuk_harf

KRITER = "Tutarlılık"

KOK_UZUNLUGU = 5          # Türkçe için "ilk 5 harf" kök bulma yöntemi (F5)
EN_AZ_ORTAK_KOK = 3       # iki cümlenin benzer sayılması için en az ortak kök
EN_AZ_BENZERLIK = 0.6     # Jaccard benzerliği: ortak kökler / toplam farklı kökler

ETKISIZ_KELIMELER = {
    "ve", "ile", "bir", "bu", "şu", "o", "da", "de", "ki", "mi", "için", "olarak", "olan",
    "gibi", "daha", "en", "çok", "her", "ya", "veya", "ise", "ama", "fakat", "kadar",
}

SAYI_DESENI = re.compile(r"%\s?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?")
# Alıştırma yönergeleri: "bulunuz", "hesaplayınız", "gösteriniz", "yazınız" ...
EMIR_KIPI = re.compile(r"(ınız|iniz|unuz|ünüz)\W*$")


def kokler(cumle: str) -> set:
    kelimeler = re.findall(r"[^\W\d_]+", kucuk_harf(cumle))
    return {k[:KOK_UZUNLUGU] for k in kelimeler if len(k) > 1 and k not in ETKISIZ_KELIMELER}


# "Görsel 1", "Şekil 2", "Tablo 3": bunlar bilgi değil gönderme numarasıdır, karşılaştırılmaz
GONDERME = re.compile(r"\b(görsel|şekil|tablo|grafik|sayfa|ünite|bölüm|örnek|soru|etkinlik)\s*\d+(?:[.,]\d+)*",
                      re.IGNORECASE)


def sayilar(cumle: str) -> tuple:
    cumle = GONDERME.sub(" ", cumle)
    return tuple(sorted(s.replace(" ", "").replace(",", ".") for s in SAYI_DESENI.findall(cumle)))


FORMUL_SEMBOLLERI = re.compile(r"[#$=_<>]")
EN_FAZLA_SAYI = 3   # daha fazla sayı içeren cümle büyük olasılıkla formül veya tablo parçasıdır
# "bu bölümde", "bu nokta": cümle bulunduğu yere işaret ediyor; her bölümde farklı sayı olabilir
ISARET_SIFATLARI = re.compile(r"\b(bu|şu|bunlar|bunun|buna|burada)\b", re.IGNORECASE)
OLUMSUZLUK = re.compile(r"(mamakta|memekte|maz|mez|madı|medi|mıyor|miyor|muyor|müyor|değil)\w*", re.IGNORECASE)


def bilgi_cumlesi_mi(cumle: str) -> bool:
    """Soru, alıştırma yönergesi, başlık veya formül olmayan, nokta ile biten bildirme cümlesi mi?"""
    cumle = cumle.strip()
    if not cumle.endswith(".") or EMIR_KIPI.search(cumle) or FORMUL_SEMBOLLERI.search(cumle):
        return False
    if len(SAYI_DESENI.findall(cumle)) > EN_FAZLA_SAYI or ISARET_SIFATLARI.search(cumle):
        return False
    kelimeler = re.findall(r"[^\W\d_]+", cumle)
    buyuk_harfli = sum(1 for k in kelimeler if k[0].isupper())
    return buyuk_harfli <= len(kelimeler) / 2          # başlıkları ("MUTLAK DEĞER FONKSİYONU 2.2.") ele


def tek_harfli_isimler(cumle: str) -> set:
    """Matematikte nesneleri ayıran harfler: "A firması", "f fonksiyonu", "B şehri"."""
    return set(re.findall(r"(?<![^\W\d_])[^\W\d_](?![^\W\d_])", cumle))


def sayisal_celiskiler(paragraflar) -> list:
    # Sayı içeren bilgi cümlelerini topla
    cumleler = []   # (paragraf, cümle, kökler, sayılar)
    for p in paragraflar:
        for c in cumlelere_bol(p.metin):
            s = sayilar(c)
            k = kokler(c)
            if s and len(k) >= EN_AZ_ORTAK_KOK + 1 and bilgi_cumlesi_mi(c):
                cumleler.append((p, c, k, s))

    # Ters dizin: her kökün hangi cümlelerde geçtiği. Böylece her cümle çifti değil,
    # yalnızca ortak kökü olan çiftler karşılaştırılır.
    dizin = defaultdict(list)
    for i, (_, _, k, _) in enumerate(cumleler):
        for kok in k:
            dizin[kok].append(i)

    hatalar = []
    for i, (p1, c1, k1, s1) in enumerate(cumleler):
        adaylar = Counter(j for kok in k1 for j in dizin[kok] if j > i)
        for j, ortak in adaylar.items():
            if ortak < EN_AZ_ORTAK_KOK:
                continue
            p2, c2, k2, s2 = cumleler[j]
            benzerlik = ortak / len(k1 | k2)
            # Farklı kökler çok azsa iki cümle aynı bilgiden söz ediyordur.
            # "Resim kursu 10.00'da" ile "Bale kursu 11.00'de" farklı şeylerden söz eder (2 farklı kök).
            farkli_kok = len(k1 ^ k2)
            ayni_konu = farkli_kok <= max(1, int(0.15 * len(k1 | k2)))
            ayni_nesne = tek_harfli_isimler(c1) == tek_harfli_isimler(c2)
            # "kalkış yapmaktadır" / "kalkış yapmamaktadır": biri olumlu biri olumsuzsa çelişki değil
            ayni_olumluluk = bool(OLUMSUZLUK.search(c1)) == bool(OLUMSUZLUK.search(c2))
            if (benzerlik >= EN_AZ_BENZERLIK and ayni_konu and ayni_nesne and ayni_olumluluk
                    and s1 != s2 and c1 != c2):
                hatalar.append(Hata(
                    p2.sayfa, p2.paragraf_no, KRITER,
                    f"Bu bilgi kitabın başka bir yerinde (Sayfa {p1.sayfa}, Paragraf {p1.paragraf_no}) "
                    f"farklı sayılarla verilmiş: \"{c1}\"",
                    c2, "İki ifadeden hangisinin doğru olduğunu kontrol edin.", p2.konum))
    return hatalar


def yazim_birligi(paragraflar) -> list:
    """Aynı kelimenin kitapta hem bitişik hem ayrı (veya tireli/tiresiz) yazıldığı yerleri bulur."""
    tekil = Counter()          # kelime -> kaç kez geçti
    ikili = defaultdict(list)  # "hiç bir" -> [paragraflar]
    tireli = defaultdict(list) # "e-posta" -> [paragraflar]

    for p in paragraflar:
        kelimeler = re.findall(r"[^\W\d_]+(?:-[^\W\d_]+)?", kucuk_harf(p.metin))
        for i, k in enumerate(kelimeler):
            if "-" in k:
                tireli[k].append(p)
            else:
                tekil[k] += 1
                if i + 1 < len(kelimeler) and "-" not in kelimeler[i + 1]:
                    ikili[k + " " + kelimeler[i + 1]].append(p)

    hatalar = []
    for ayri, yerler in ikili.items():
        bitisik = ayri.replace(" ", "")
        if tekil[bitisik] and gercek_kelimeler_mi(ayri.split()):
            hatalar += _birlik_hatalari(ayri, bitisik, yerler, tekil[bitisik])
    for tirelisi, yerler in tireli.items():
        tiresiz = tirelisi.replace("-", "")
        # tireli yazımda parçalar en az 3 harf olmalı: "şe-kilde" satır sonu bölmesinden kalmıştır
        if tekil[tiresiz] and gercek_kelimeler_mi(tirelisi.split("-"), en_az_harf=3):
            hatalar += _birlik_hatalari(tirelisi, tiresiz, yerler, tekil[tiresiz])
    return hatalar


# İkinci parça bunlardan biriyse "ayrı yazım" büyük olasılıkla PDF'in kelimeyi bölmesidir
# ("dünya nın") veya doğru bir bağlaçtır ("Şekil de bunu gösteriyor"); yazım birliği hatası sayılmaz.
EKLER_VE_BAGLACLAR = {
    "de", "da", "te", "ta", "ki", "deki", "daki", "teki", "taki", "den", "dan", "ten", "tan",
    "nın", "nin", "nun", "nün", "ın", "in", "un", "ün", "ya", "ye", "yı", "yi", "yu", "yü",
    "a", "e", "ı", "i", "u", "ü", "la", "le", "yla", "yle", "dır", "dir", "tır", "tir", "mi", "mı",
    "ve", "ile", "ama", "veya",
}


def gercek_kelimeler_mi(parcalar, en_az_harf=2) -> bool:
    """Parçaların her biri tek başına geçerli bir Türkçe kelime mi? ("eş" + "kenar" evet, "şe" + "kilde" hayır)"""
    from yazim_denetimi import sozlukte_var_mi
    return all(len(p) >= en_az_harf and p not in EKLER_VE_BAGLACLAR and sozlukte_var_mi(p) for p in parcalar)


def _birlik_hatalari(bicim, diger_bicim, yerler, diger_sayisi) -> list:
    """"bicim"in geçtiği her paragraf için, kitapta "diger_bicim"in de kullanıldığını bildirir."""
    aciklama = (f"Yazım birliği yok: kitapta hem \"{bicim}\" ({len(yerler)} kez) hem "
                f"\"{diger_bicim}\" ({diger_sayisi} kez) yazımı kullanılmış.")
    tekrarsiz = {id(p): p for p in yerler}.values()   # aynı paragrafı bir kez raporla
    return [Hata(p.sayfa, p.paragraf_no, KRITER, aciklama, bicim,
                 "Kitap boyunca tek bir yazım kullanın (TDK'ye göre kontrol edin).", p.konum)
            for p in tekrarsiz]


def denetle(paragraflar) -> list:
    return sayisal_celiskiler(paragraflar) + yazim_birligi(paragraflar)
