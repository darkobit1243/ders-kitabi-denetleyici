"""Komut satırından kullanım:

    python main.py kitap.pdf --sinif 9            # hataları bulur, CSV rapor oluşturur
    python main.py kitap.pdf --paragraflar         # yalnızca çıkarılan paragrafları listeler
"""

import argparse
import csv
import os
import sys
from collections import Counter

from denetleyici import kitabi_denetle
from pdf_okuyucu import paragraflari_cikar

ORNEK_SAYISI = 10   # ekranda her kriterden kaç örnek gösterilsin


def paragraflari_listele(pdf_yolu):
    paragraflar, metinsiz_sayfalar = paragraflari_cikar(pdf_yolu)
    for p in paragraflar:
        kisa = p.metin if len(p.metin) <= 100 else p.metin[:100] + "..."
        etiket = " (OCR)" if p.ocr else ""
        print(f"[Sayfa {p.sayfa}, Paragraf {p.paragraf_no}{etiket}] {kisa}")
    ocr_sayisi = sum(p.ocr for p in paragraflar)
    print(f"\nToplam {len(paragraflar)} paragraf bulundu ({ocr_sayisi} tanesi OCR ile okundu).")
    if metinsiz_sayfalar:
        print(f"Uyarı: {metinsiz_sayfalar} numaralı sayfalarda metin bulunamadı.")


def csv_kaydet(hatalar, pdf_yolu):
    ad = os.path.splitext(os.path.basename(pdf_yolu))[0]
    cikti = f"rapor_{ad}.csv"
    # utf-8-sig: Excel'in Türkçe karakterleri doğru göstermesi için
    with open(cikti, "w", newline="", encoding="utf-8-sig") as f:
        yazici = csv.writer(f, delimiter=";")
        yazici.writerow(["Sayfa", "Paragraf", "Kriter", "Açıklama", "Alıntı", "Öneri"])
        for h in hatalar:
            yazici.writerow([h.sayfa, h.paragraf_no, h.kriter, h.aciklama, h.alinti, h.oneri])
    return cikti


def main():
    # Bazı Windows konsolları Türkçe karakterleri bozuk gösteriyor; çıktıyı UTF-8 yapıyoruz
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ayrac = argparse.ArgumentParser(description="Ders kitabı PDF'lerinde hata tespiti")
    ayrac.add_argument("pdf", help="incelenecek PDF dosyası")
    ayrac.add_argument("--sinif", type=int, default=9, help="kitabın sınıf düzeyi (1-12), varsayılan 9")
    ayrac.add_argument("--paragraflar", action="store_true", help="yalnızca paragrafları listele")
    secenekler = ayrac.parse_args()

    if secenekler.paragraflar:
        paragraflari_listele(secenekler.pdf)
        return

    hatalar, ist = kitabi_denetle(secenekler.pdf, secenekler.sinif)

    print(f"{ist['toplam_paragraf']} paragraftan {ist['incelenen_paragraf']} tanesi incelendi "
          f"({ist['atlanan_paragraf']} formül/tablo parçası atlandı).\n")

    for kriter, sayi in Counter(h.kriter for h in hatalar).items():
        print(f"=== {kriter}: {sayi} olası hata ===")
        for h in [h for h in hatalar if h.kriter == kriter][:ORNEK_SAYISI]:
            oneri = f"  -> Öneri: {h.oneri}" if h.oneri else ""
            print(f"[Sayfa {h.sayfa}, Paragraf {h.paragraf_no}] {h.aciklama}\n    \"{h.alinti}\"{oneri}")
        print()

    print(f"Tüm hatalar kaydedildi: {csv_kaydet(hatalar, secenekler.pdf)}")


if __name__ == "__main__":
    main()
