"""Sistemin doğruluğunu ölçer.

Yöntem (hata ekleme / "error injection"):
  Gerçek bir ders kitabının denetlenebilir paragraflarından rastgele örnekler seçilir ve her birine
  türü bilinen TEK bir hata eklenir. Sistemin eklenen hatayı bulup bulmadığı kontrol edilir.
  Böylece doğru cevabı bildiğimiz bir test seti oluşur ve "yakalama oranı" hesaplanabilir.

  Hata türleri:
    1. Yazım hatası    : 6+ harfli bir kelimeden bir harf düşürülür ("fonksiyon" -> "fonksyon");
                         ortaya çıkan kelime sözlükte yoksa kullanılır.
    2. Noktalama hatası: iki kelime arasındaki virgülden önce boşluk eklenir ("elma, armut" -> "elma , armut").
    3. Çelişen bilgi   : sayı içeren bir bilgi cümlesinin sayısı değiştirilip kitabın başka bir yerine eklenir.
    4. Uzun cümle      : bir paragrafın cümleleri virgülle birleştirilerek tek uzun cümle yapılır.

  Ayrıca hata eklenmemiş paragraflarda sistemin kaç bulgu verdiği de sayılır. Bu bulguların bir kısmı
  kitaptaki gerçek hatalar, bir kısmı yanlış alarmdır; inceleyicinin bakması gereken ek iş yükünü gösterir.

Kullanım:  python degerlendirme.py ..\\ornekler\\kitap.pdf --sinif 9
Sonuç degerlendirme_sonucu.json dosyasına yazılır ve arayüz/raporda gösterilir.
"""

import argparse
import copy
import json
import os
import random
import re
import sys
from datetime import datetime

import icerik_guvenligi
import tutarlilik
import yas_seviyesi
import yazim_denetimi
from metin_filtresi import incelenebilir_mi
from pdf_okuyucu import paragraflari_cikar
from turkce import cumlelere_bol, kelimeler, kucuk_harf

SONUC_DOSYASI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "degerlendirme_sonucu.json")
ORNEK_SAYISI = 100
TOHUM = 2026   # aynı sonuçların tekrar elde edilebilmesi için sabit rastgelelik tohumu


def harf_dusur(p, rnd):
    adaylar = [k for k in re.findall(r"(?<![^\W\d_])[a-zçğıöşü]{6,}(?![^\W\d_])", p.metin)]
    rnd.shuffle(adaylar)
    for kelime in adaylar:
        i = rnd.randrange(1, len(kelime) - 1)
        bozuk = kelime[:i] + kelime[i + 1:]
        if not yazim_denetimi.sozlukte_var_mi(kucuk_harf(bozuk)):
            yeni = copy.copy(p)
            yeni.metin = re.sub(rf"(?<![^\W\d_]){kelime}(?![^\W\d_])", bozuk, p.metin, count=1)
            return yeni, bozuk
    return None, None


def virgul_bosluk(p, rnd):
    yerler = [m.start() for m in re.finditer(r"(?<=[^\W\d_]{2}), (?=[^\W\d_]{2})", p.metin)]
    if not yerler:
        return None, None
    i = rnd.choice(yerler)
    yeni = copy.copy(p)
    yeni.metin = p.metin[:i] + " ," + p.metin[i + 1:]
    return yeni, None


def uzun_cumle(p, rnd, sinif):
    cumleler = cumlelere_bol(p.metin)
    sinir = yas_seviyesi.esikler(sinif)[1]
    if len(cumleler) < 2:
        return None, None
    birlesik = ", ".join(c.rstrip(".!?") for c in cumleler) + "."
    if len(kelimeler(birlesik)) <= sinir or yas_seviyesi.isim_listesi_mi(kelimeler(birlesik)):
        return None, None
    yeni = copy.copy(p)
    yeni.metin = birlesik
    return yeni, None


def olc(pdf_yolu: str, sinif: int) -> dict:
    rnd = random.Random(TOHUM)
    paragraflar, _ = paragraflari_cikar(pdf_yolu)
    havuz = [p for p in paragraflar if incelenebilir_mi(p.metin)]
    sonuc = {}

    # 1) Yazım hatası
    bulunan = denenen = 0
    for p in rnd.sample(havuz, len(havuz)):
        if denenen == ORNEK_SAYISI:
            break
        yeni, bozuk = harf_dusur(p, rnd)
        if not yeni:
            continue
        denenen += 1
        bulunan += any(h.alinti == bozuk for h in yazim_denetimi.denetle(yeni))
    sonuc["Yazım hatası (harf eksik)"] = (bulunan, denenen)

    # 2) Noktalama
    bulunan = denenen = 0
    for p in rnd.sample(havuz, len(havuz)):
        if denenen == ORNEK_SAYISI:
            break
        yeni, _ = virgul_bosluk(p, rnd)
        if not yeni:
            continue
        denenen += 1
        bulunan += any("önce boşluk" in h.aciklama for h in yazim_denetimi.denetle(yeni))
    sonuc["Noktalama (virgülden önce boşluk)"] = (bulunan, denenen)

    # 3) Çelişen sayısal bilgi: cümlenin sayısı değiştirilmiş kopyası ayrı bir paragraf olarak eklenir
    bilgi_cumleleri = [(p, c) for p in havuz for c in cumlelere_bol(p.metin)
                       if tutarlilik.sayilar(c) and tutarlilik.bilgi_cumlesi_mi(c)
                       and len(tutarlilik.kokler(c)) >= tutarlilik.EN_AZ_ORTAK_KOK + 1]
    bulunan = denenen = 0
    for p, c in rnd.sample(bilgi_cumleleri, min(ORNEK_SAYISI, len(bilgi_cumleleri))):
        sayi = tutarlilik.SAYI_DESENI.findall(tutarlilik.GONDERME.sub(" ", c))[0]
        # Sayının son rakam grubu değiştirilir ("5,8" -> "5,15", "%97" -> "%104"); ondalıklı sayılar da bozulmaz
        degisik = re.sub(r"\d+(?!.*\d)", lambda m: str(int(m.group()) + 7), sayi)
        assert degisik != sayi
        kopya = copy.copy(p)
        kopya.sayfa, kopya.paragraf_no = 9999, 1
        kopya.metin = c.replace(sayi, degisik, 1)
        denenen += 1
        bulgular = tutarlilik.sayisal_celiskiler([p, kopya])
        bulunan += any(h.sayfa == 9999 for h in bulgular)
    sonuc["Çelişen sayısal bilgi"] = (bulunan, denenen)

    # 4) Uzun cümle
    bulunan = denenen = 0
    for p in rnd.sample(havuz, len(havuz)):
        if denenen == ORNEK_SAYISI:
            break
        yeni, _ = uzun_cumle(p, rnd, sinif)
        if not yeni:
            continue
        denenen += 1
        bulunan += any("Cümle çok uzun" in h.aciklama for h in yas_seviyesi.denetle(yeni, sinif))
    sonuc["Çok uzun cümle"] = (bulunan, denenen)

    # 5-7) İçerik güvenliği: kişisel veri, marka ve çekimli hassas kelime eklenir
    def icerik_testi(ad, uret):
        bulunan = 0
        for p in rnd.sample(havuz, ORNEK_SAYISI):
            eklenen = uret()
            yeni = copy.copy(p)
            kelimeler_ = p.metin.split()
            i = rnd.randrange(len(kelimeler_) + 1)
            yeni.metin = " ".join(kelimeler_[:i] + [eklenen] + kelimeler_[i:])
            bulunan += any(eklenen.startswith(h.alinti) or h.alinti == eklenen.strip(".,")
                           for h in icerik_guvenligi.denetle(yeni))
        sonuc[ad] = (bulunan, ORNEK_SAYISI)

    def tc_uret():
        d = [rnd.randint(1, 9)] + [rnd.randint(0, 9) for _ in range(8)]
        d.append(((d[0] + d[2] + d[4] + d[6] + d[8]) * 7 - (d[1] + d[3] + d[5] + d[7])) % 10)
        d.append(sum(d) % 10)
        return "".join(map(str, d))

    def telefon_uret():
        return f"05{rnd.randint(30, 59)} {rnd.randint(100, 999)} {rnd.randint(10, 99)} {rnd.randint(10, 99)}"

    icerik_testi("Kişisel veri (T.C. kimlik no / telefon)", lambda: rnd.choice([tc_uret, telefon_uret])())
    icerik_testi("Marka adı", lambda: rnd.choice(icerik_guvenligi.MARKALAR))
    icerik_testi("Hassas ifade (çekimli)", lambda: rnd.choice(
        ["sigarasını", "alkollü", "kumara", "uyuşturucunun", "kavgaya", "öldürdüler", "dövüldü", "aptallar"]))

    # Hata eklenmemiş paragraflarda bulgu sayısı
    temiz = rnd.sample(havuz, min(500, len(havuz)))
    ek_bulgu = sum(len(yazim_denetimi.denetle(p)) for p in temiz)
    ek_icerik_bulgusu = sum(len(icerik_guvenligi.denetle(p)) for p in temiz)

    return {
        "kitap": os.path.basename(pdf_yolu),
        "sinif": sinif,
        "tarih": datetime.now().strftime("%d.%m.%Y"),
        "yakalama": {tur: {"bulunan": b, "denenen": d, "oran": round(100 * b / d, 1) if d else None}
                     for tur, (b, d) in sonuc.items()},
        "temiz_paragraf": len(temiz),
        "temiz_paragraf_yazim_bulgusu": ek_bulgu,
        "temiz_paragraf_icerik_bulgusu": ek_icerik_bulgusu,
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ayrac = argparse.ArgumentParser(description="Sistemin doğruluğunu hata ekleme yöntemiyle ölçer")
    ayrac.add_argument("pdf")
    ayrac.add_argument("--sinif", type=int, default=9)
    s = ayrac.parse_args()

    sonuc = olc(s.pdf, s.sinif)
    with open(SONUC_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=2)

    print(f"Kitap: {sonuc['kitap']} ({s.sinif}. Sınıf)\n")
    print(f"{'Eklenen hata türü':38} {'Bulunan':>8} {'Denenen':>8} {'Oran':>7}")
    for tur, d in sonuc["yakalama"].items():
        print(f"{tur:38} {d['bulunan']:>8} {d['denenen']:>8} {('%' + str(d['oran'])):>7}")
    print(f"\nHata eklenmemiş {sonuc['temiz_paragraf']} paragrafta yazım/noktalama bulgusu: "
          f"{sonuc['temiz_paragraf_yazim_bulgusu']}, içerik güvenliği bulgusu: "
          f"{sonuc['temiz_paragraf_icerik_bulgusu']}")
    print(f"Sonuç kaydedildi: {SONUC_DOSYASI}")


if __name__ == "__main__":
    main()
