"""Komut satırından kullanım:  python main.py kitap.pdf"""

import sys

from pdf_okuyucu import paragraflari_cikar


def main():
    if len(sys.argv) < 2:
        print("Kullanım: python main.py <pdf_dosyası>")
        return

    paragraflar, metinsiz_sayfalar = paragraflari_cikar(sys.argv[1])

    for p in paragraflar:
        kisa = p.metin if len(p.metin) <= 100 else p.metin[:100] + "..."
        etiket = " (OCR)" if p.ocr else ""
        print(f"[Sayfa {p.sayfa}, Paragraf {p.paragraf_no}{etiket}] {kisa}")

    ocr_sayisi = sum(p.ocr for p in paragraflar)
    print(f"\nToplam {len(paragraflar)} paragraf bulundu ({ocr_sayisi} tanesi OCR ile okundu).")
    if metinsiz_sayfalar:
        print(f"Uyarı: {metinsiz_sayfalar} numaralı sayfalarda metin bulunamadı "
              "(taranmış/görüntü sayfası olabilir, OCR gerekir).")


if __name__ == "__main__":
    main()
