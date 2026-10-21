# Ders Kitaplarında İçerik ve Tutarlılık Hatalarının Otomatik Tespiti

PDF formatındaki ders kitaplarından metni çıkarır ve üç kritere göre olası hataları
sayfa/paragraf bilgisiyle gösterir.

## Kriterler (planlanan)
1. **Yazım ve noktalama hataları**
2. **Bilgi tutarsızlıkları** (aynı bilginin kitabın farklı yerlerinde farklı verilmesi)
3. **Yaş seviyesine uygunluk** (Ateşman okunabilirlik formülü, çok uzun cümleler)

## Kurulum
```
pip install -r requirements.txt
```

## Kullanım
```
python ornek_pdf_olustur.py              # test PDF'i oluşturur
python main.py ornekler/ornek_kitap.pdf  # paragrafları listeler
```

## Dosyalar
- `pdf_okuyucu.py` – PDF'ten metni sayfa ve paragraf bilgisiyle çıkarır
- `main.py` – komut satırı arayüzü
- `ornek_pdf_olustur.py` – içinde bilinçli hatalar olan test PDF'i üretir
