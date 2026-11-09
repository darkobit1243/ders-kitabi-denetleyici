"""Yazdırılabilir ön inceleme raporu (tek HTML dosyası).

Bulgular, Talim ve Terbiye Kurulu Başkanlığının taslak ders kitabı incelemesinde kullandığı ölçüt
başlıklarına (Bilimsel Yeterlik, Dil ve Anlatım Yeterliği) göre gruplanır. Rapor hiçbir dış kaynak
(yazı tipi, resim, internet adresi) kullanmaz; tarayıcıda açılır, Ctrl+P ile yazdırılabilir veya PDF
olarak kaydedilebilir.
"""

import json
import os
from collections import Counter
from datetime import datetime
from html import escape

from olcutler import ALT_BASLIK_SIRASI, OLCUT_SIRASI, olcut
from surum import ACIKLAMA, GELISTIRICI, SURUM, UYGULAMA_ADI, UZUN_AD
from yas_seviyesi import sinif_adi

DEGERLENDIRME_DOSYASI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "degerlendirme_sonucu.json")

KRITER_SIRASI = ["Yazım", "Tutarlılık", "Yaş Seviyesi"]
KRITER_ACIKLAMALARI = {
    "Yazım": "Sık yapılan yazım hataları, Türkçe sözlükte bulunmayan kelimeler ve noktalama kuralları.",
    "Tutarlılık": "Kitabın farklı yerlerinde farklı sayılarla verilen aynı bilgi ve aynı kelimenin "
                  "farklı yazılışları.",
    "Yaş Seviyesi": "Ateşman, Çetinkaya-Uzun ve Bezirci-Yılmaz okunabilirlik formülleri ve sınıf düzeyine "
                    "göre çok uzun cümleler.",
}

STIL = """
body { font-family: Arial, Helvetica, sans-serif; color: #1a1a1a; margin: 32px auto; padding: 0 16px;
       max-width: 1000px; font-size: 13px; background: #fff; }
td { overflow-wrap: anywhere; }
h1 { font-size: 20px; margin: 0 0 4px; color: #12315f; }
h2 { font-size: 15px; margin: 28px 0 8px; color: #12315f; border-bottom: 2px solid #12315f; padding-bottom: 4px; }
h3 { font-size: 13.5px; margin: 18px 0 6px; color: #1d4a8a; }
.ust { color: #555; font-size: 11px; letter-spacing: .05em; margin-bottom: 6px; }
.alt { color: #555; margin: 0 0 18px; }
table { border-collapse: collapse; width: 100%; margin-bottom: 8px; }
th, td { border: 1px solid #c8c8c8; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #e8eef7; }
.bilgi td:first-child { width: 200px; font-weight: bold; background: #f5f7fa; }
.sayi { text-align: right; width: 60px; }
.uyari { border: 1px solid #d9a400; background: #fff8e1; padding: 10px 12px; margin: 16px 0; }
.not { color: #555; font-size: 12px; }
.alti { color: #666; font-size: 11px; margin-top: 32px; border-top: 1px solid #ccc; padding-top: 8px; }
@media print { body { margin: 12mm; } h2, h3 { break-after: avoid; } tr { break-inside: avoid; } }
"""


def _sayi(x, basamak=1) -> str:
    return f"{x:.{basamak}f}".replace(".", ",")


def _tam(x: int) -> str:
    return f"{x:,}".replace(",", ".")   # Türkçe binlik ayırıcı: 1.393


def okunabilirlik_bolumu(o: dict, sinif: int) -> list:
    if not o or not o["olculen_paragraf"]:
        return []
    oran = 100 * o["seviye_ustu_paragraf"] / o["olculen_paragraf"]
    kademe = "İlköğretim, 1-8" if sinif <= 8 else "Lise, 9-12"
    return [
        "<h3>Kitabın genel okunabilirliği</h3>",
        "<table><tr><th>Formül</th><th class='sayi'>Değer</th><th>Düzey</th></tr>",
        f"<tr><td>Ateşman (1997)</td><td class='sayi'>{_sayi(o['atesman'])}</td><td>{o['atesman_duzeyi']}</td></tr>",
        f"<tr><td>Çetinkaya-Uzun (2010)</td><td class='sayi'>{_sayi(o['cetinkaya_uzun'])}</td>"
        f"<td>{o['cetinkaya_duzeyi']}</td></tr>",
        f"<tr><td>Bezirci-Yılmaz (2010)</td><td class='sayi'>{_sayi(o['bezirci_yilmaz'])}</td>"
        f"<td>{o['bezirci_duzeyi']}</td></tr></table>",
        f"<p class='not'>Ortalama cümle uzunluğu {_sayi(o['ortalama_cumle'])} kelime, ortalama kelime uzunluğu "
        f"{_sayi(o['ortalama_hece'], 2)} hece. En az 15 kelimelik {o['olculen_paragraf']} paragrafın "
        f"{o['seviye_ustu_paragraf']} tanesi (%{_sayi(oran, 0)}) Bezirci-Yılmaz formülüne göre kitabın kademesinin "
        f"({kademe}) üstündedir. Formüller farklı sonuçlar verebildiği için birlikte yorumlanmalıdır; "
        f"Bezirci-Yılmaz formülü çok heceli terimlere yüksek ağırlık verdiğinden terim yoğun paragraflarda "
        f"yüksek sonuç üretir.</p>",
    ]


def dogruluk_bolumu() -> list:
    if not os.path.exists(DEGERLENDIRME_DOSYASI):
        return []
    with open(DEGERLENDIRME_DOSYASI, encoding="utf-8") as f:
        d = json.load(f)
    satirlar = "".join(f"<tr><td>{escape(tur)}</td><td class='sayi'>{v['bulunan']}/{v['denenen']}</td>"
                       f"<td class='sayi'>%{_sayi(v['oran'], 0)}</td></tr>" for tur, v in d["yakalama"].items())
    return [
        "<h2>Programın Doğruluk Ölçümü</h2>",
        f"<p class='not'>Gerçek bir ders kitabının ({escape(d['kitap'])}, {d['sinif']}. Sınıf) rastgele seçilen "
        f"paragraflarına türü bilinen hatalar eklenmiş ve programın bunları bulup bulmadığı ölçülmüştür "
        f"({d['tarih']}).</p>",
        f"<table><tr><th>Eklenen hata türü</th><th class='sayi'>Bulunan</th><th class='sayi'>Oran</th></tr>"
        f"{satirlar}</table>",
        f"<p class='not'>Hata eklenmemiş {d['temiz_paragraf']} paragrafta {d['temiz_paragraf_yazim_bulgusu']} "
        f"yazım/noktalama bulgusu çıkmıştır (bir kısmı kitaptaki gerçek hatalar, bir kısmı yanlış alarmdır). "
        f"Noktalama, çelişki ve uzun cümle testleri kuralların gerçek kitap metninde çalıştığını gösterir; "
        f"kitapta doğal olarak bulunabilecek her hata türünün bulunacağı anlamına gelmez.</p>",
    ]


def html_rapor(hatalar, istatistik, kitap_adi: str, sinif: int, tarih: datetime = None) -> str:
    tarih = tarih or datetime.now()
    e = escape
    ana_sayilar = Counter(olcut(h)[0] for h in hatalar)
    alt_sayilar = Counter(olcut(h) for h in hatalar)

    parcalar = [
        "<!DOCTYPE html><html lang='tr'><head><meta charset='utf-8'>",
        f"<title>Ön İnceleme Raporu – {e(kitap_adi)}</title><style>{STIL}</style></head><body>",
        "<div class='ust'>MİLLÎ EĞİTİM BAKANLIĞINA SUNULMAK ÜZERE HAZIRLANMIŞ ÖĞRENCİ PROJESİ</div>",
        f"<h1>Ders Kitabı Ön İnceleme Raporu</h1><p class='alt'>{e(UZUN_AD)}</p>",
        "<table class='bilgi'>",
        f"<tr><td>Kitap dosyası</td><td>{e(kitap_adi)}</td></tr>",
        f"<tr><td>Sınıf düzeyi</td><td>{sinif_adi(sinif, kademe_ile=True)}</td></tr>",
        f"<tr><td>Denetim tarihi</td><td>{tarih:%d.%m.%Y %H:%M}</td></tr>",
    ]
    if "sayfa_sayisi" in istatistik:
        parcalar.append(f"<tr><td>Sayfa sayısı</td><td>{istatistik['sayfa_sayisi']}</td></tr>")
    parcalar.append(f"<tr><td>İncelenen paragraf</td><td>{_tam(istatistik['incelenen_paragraf'])} "
                    f"(formül/tablo olarak atlanan: {_tam(istatistik['atlanan_paragraf'])})</td></tr>")
    if istatistik["metinsiz_sayfalar"]:
        sayfalar = ", ".join(str(s) for s in istatistik["metinsiz_sayfalar"])
        parcalar.append(f"<tr><td>Metin okunamayan sayfalar</td><td>{sayfalar}</td></tr>")
    parcalar.append(f"<tr><td>Program</td><td>{e(UYGULAMA_ADI)} {SURUM}</td></tr></table>")

    parcalar.append(
        "<div class='uyari'><b>Önemli:</b> Bu rapor bir <b>ön inceleme</b> raporudur. Bulgular otomatik olarak "
        "üretilmiş <b>olası</b> hatalardır ve her birinin kitapta bir uzman tarafından kontrol edilmesi gerekir. "
        "Bulgular, Talim ve Terbiye Kurulu Başkanlığının taslak ders kitabı incelemesinde kullandığı ölçüt "
        "başlıklarından <i>Bilimsel Yeterlik</i> ve <i>Dil ve Anlatım Yeterliği</i> altında gruplanmıştır; "
        "rapor resmî incelemenin yerine geçmez ve bu ölçütlerin tamamını kapsamaz. Matematik formülleri ve "
        "tablolar denetlenmez; taranmış sayfalarda OCR kaynaklı okuma hataları olabilir.</div>")

    # Özet: ölçüt -> alt başlık -> bulgu sayısı
    parcalar.append("<h2>Özet</h2><table><tr><th>İnceleme ölçütü</th><th>Alt başlık</th>"
                    "<th class='sayi'>Bulgu</th></tr>")
    for ana in OLCUT_SIRASI:
        for alt in ALT_BASLIK_SIRASI:
            if alt_sayilar.get((ana, alt)):
                parcalar.append(f"<tr><td>{ana}</td><td>{alt}</td><td class='sayi'>{alt_sayilar[(ana, alt)]}</td></tr>")
    parcalar.append(f"<tr><th colspan='2'>Toplam</th><th class='sayi'>{len(hatalar)}</th></tr></table>")

    # Bulgular: ölçüt başlıkları altında
    for ana in OLCUT_SIRASI:
        parcalar.append(f"<h2>{ana} ({ana_sayilar.get(ana, 0)})</h2>")
        if ana == "Dil ve Anlatım Yeterliği":
            parcalar += okunabilirlik_bolumu(istatistik.get("okunabilirlik"), sinif)
        if not ana_sayilar.get(ana):
            parcalar.append("<p class='not'>Bu başlık altında olası hata bulunamadı.</p>")
        for alt in ALT_BASLIK_SIRASI:
            bulgular = [h for h in hatalar if olcut(h) == (ana, alt)]
            if not bulgular:
                continue
            parcalar.append(f"<h3>{alt} ({len(bulgular)})</h3><table><tr><th class='sayi'>Sayfa</th>"
                            "<th class='sayi'>Paragraf</th><th>Açıklama</th><th>Alıntı</th><th>Öneri</th></tr>")
            for h in bulgular:
                parcalar.append(f"<tr><td class='sayi'>{h.sayfa}</td><td class='sayi'>{h.paragraf_no}</td>"
                                f"<td>{e(h.aciklama)}</td><td>{e(h.alinti)}</td><td>{e(h.oneri)}</td></tr>")
            parcalar.append("</table>")

    parcalar += dogruluk_bolumu()

    parcalar.append(f"<p class='alti'>{e(UYGULAMA_ADI)} {SURUM} · Geliştiren: {e(GELISTIRICI)} · "
                    f"{e(ACIKLAMA)} Tüm işlemler bilgisayarda yerel olarak yapılmıştır.</p></body></html>")
    return "".join(parcalar)
