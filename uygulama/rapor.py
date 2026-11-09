"""Yazdırılabilir denetim raporu (tek HTML dosyası).

Rapor hiçbir dış kaynak (yazı tipi, resim, internet adresi) kullanmaz; tarayıcıda açılır ve
Ctrl+P ile yazdırılabilir veya PDF olarak kaydedilebilir.
"""

from collections import Counter
from datetime import datetime
from html import escape

from surum import ACIKLAMA, GELISTIRICI, SURUM, UYGULAMA_ADI, UZUN_AD
from yas_seviyesi import sinif_adi

KRITER_SIRASI = ["Yazım", "Tutarlılık", "Yaş Seviyesi"]
KRITER_ACIKLAMALARI = {
    "Yazım": "Sık yapılan yazım hataları, Türkçe sözlükte bulunmayan kelimeler ve noktalama kuralları.",
    "Tutarlılık": "Kitabın farklı yerlerinde farklı sayılarla verilen aynı bilgi ve aynı kelimenin "
                  "farklı yazılışları.",
    "Yaş Seviyesi": "Ateşman okunabilirlik puanı ve sınıf düzeyine göre çok uzun cümleler.",
}

STIL = """
body { font-family: Arial, Helvetica, sans-serif; color: #1a1a1a; margin: 32px auto; padding: 0 16px;
       max-width: 1000px; font-size: 13px; background: #fff; }
td { overflow-wrap: anywhere; }
h1 { font-size: 20px; margin: 0 0 4px; color: #12315f; }
h2 { font-size: 15px; margin: 28px 0 8px; color: #12315f; border-bottom: 2px solid #12315f; padding-bottom: 4px; }
.alt { color: #555; margin: 0 0 18px; }
table { border-collapse: collapse; width: 100%; margin-bottom: 8px; }
th, td { border: 1px solid #c8c8c8; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #e8eef7; }
.bilgi td:first-child { width: 180px; font-weight: bold; background: #f5f7fa; }
.sayi { text-align: right; width: 60px; }
.uyari { border: 1px solid #d9a400; background: #fff8e1; padding: 10px 12px; margin: 16px 0; }
.alti { color: #666; font-size: 11px; margin-top: 32px; border-top: 1px solid #ccc; padding-top: 8px; }
@media print { body { margin: 12mm; } h2 { break-after: avoid; } tr { break-inside: avoid; } }
"""


def html_rapor(hatalar, istatistik, kitap_adi: str, sinif: int, tarih: datetime = None) -> str:
    tarih = tarih or datetime.now()
    sayilar = Counter(h.kriter for h in hatalar)
    e = escape

    parcalar = [
        "<!DOCTYPE html><html lang='tr'><head><meta charset='utf-8'>",
        f"<title>Denetim Raporu – {e(kitap_adi)}</title><style>{STIL}</style></head><body>",
        f"<h1>Ders Kitabı Denetim Raporu</h1><p class='alt'>{e(UZUN_AD)}</p>",
        "<table class='bilgi'>",
        f"<tr><td>Kitap dosyası</td><td>{e(kitap_adi)}</td></tr>",
        f"<tr><td>Sınıf düzeyi</td><td>{sinif_adi(sinif, kademe_ile=True)}</td></tr>",
        f"<tr><td>Denetim tarihi</td><td>{tarih:%d.%m.%Y %H:%M}</td></tr>",
        f"<tr><td>İncelenen paragraf</td><td>{istatistik['incelenen_paragraf']} "
        f"(formül/tablo olarak atlanan: {istatistik['atlanan_paragraf']})</td></tr>",
    ]
    if istatistik["metinsiz_sayfalar"]:
        sayfalar = ", ".join(str(s) for s in istatistik["metinsiz_sayfalar"])
        parcalar.append(f"<tr><td>Metin okunamayan sayfalar</td><td>{sayfalar}</td></tr>")
    parcalar.append(f"<tr><td>Program</td><td>{e(UYGULAMA_ADI)} {SURUM}</td></tr></table>")

    parcalar.append("<h2>Özet</h2><table><tr><th>Kriter</th><th>Kapsam</th><th class='sayi'>Bulgu</th></tr>")
    for kriter in KRITER_SIRASI:
        parcalar.append(f"<tr><td>{kriter}</td><td>{KRITER_ACIKLAMALARI[kriter]}</td>"
                        f"<td class='sayi'>{sayilar.get(kriter, 0)}</td></tr>")
    parcalar.append(f"<tr><th colspan='2'>Toplam</th><th class='sayi'>{len(hatalar)}</th></tr></table>")

    parcalar.append(
        "<div class='uyari'><b>Önemli:</b> Bu rapordaki bulgular otomatik olarak üretilmiş <b>olası</b> "
        "hatalardır. Her bulgunun kitapta bir uzman tarafından kontrol edilmesi gerekir. Matematik "
        "formülleri ve tablolar denetlenmez; taranmış sayfalarda OCR kaynaklı okuma hataları olabilir.</div>")

    for kriter in KRITER_SIRASI:
        bulgular = [h for h in hatalar if h.kriter == kriter]
        if not bulgular:
            continue
        parcalar.append(f"<h2>{kriter} ({len(bulgular)})</h2><table><tr><th class='sayi'>Sayfa</th>"
                        "<th class='sayi'>Paragraf</th><th>Açıklama</th><th>Alıntı</th><th>Öneri</th></tr>")
        for h in bulgular:
            parcalar.append(f"<tr><td class='sayi'>{h.sayfa}</td><td class='sayi'>{h.paragraf_no}</td>"
                            f"<td>{e(h.aciklama)}</td><td>{e(h.alinti)}</td><td>{e(h.oneri)}</td></tr>")
        parcalar.append("</table>")

    parcalar.append(f"<p class='alti'>{e(UYGULAMA_ADI)} {SURUM} · Geliştiren: {e(GELISTIRICI)} · "
                    f"{e(ACIKLAMA)} Tüm işlemler bilgisayarda yerel olarak yapılmıştır.</p></body></html>")
    return "".join(parcalar)
