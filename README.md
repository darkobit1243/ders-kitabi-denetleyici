# Ders Kitaplarında İçerik ve Tutarlılık Hatalarının Otomatik Tespiti

PDF formatındaki ders kitaplarından metni çıkarır ve üç kritere göre olası hataları
sayfa/paragraf bilgisiyle gösterir.

## Kriterler
1. **Yazım ve noktalama hataları** – sık yapılan yazım hataları listesi, Türkçe biçimbilim
   çözümleyicisi (zeyrek) ile sözlükte bulunmayan kelimeler, basit noktalama kuralları
2. **Bilgi tutarsızlıkları** – aynı bilginin kitabın farklı yerlerinde farklı verilmesi *(7. hafta)*
3. **Yaş seviyesine uygunluk** – Ateşman okunabilirlik formülü ve sınıf düzeyine göre çok uzun cümleler

## Kurulum
```
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt_tab')"
```
Taranmış (resim) sayfalar için [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
Türkçe dil paketiyle kurulmalıdır.

## Kullanım
```
python ornek_pdf_olustur.py                         # test PDF'i oluşturur
python main.py ornekler/ornek_kitap.pdf --sinif 4   # hataları bulur, rapor_<kitap>.csv oluşturur
python main.py kitap.pdf --paragraflar              # yalnızca çıkarılan paragrafları listeler
```

## Dosyalar
| Dosya | Görevi |
|---|---|
| `pdf_okuyucu.py` | PDF'ten metni sayfa/paragraf bilgisiyle çıkarır, gerekirse OCR yapar |
| `metin_filtresi.py` | Formül ve tablo parçalarını denetim dışında bırakır |
| `yazim_denetimi.py` | Kriter 1: yazım ve noktalama |
| `yas_seviyesi.py` | Kriter 3: Ateşman okunabilirlik ve cümle uzunluğu |
| `denetleyici.py` | Bütün adımları birleştirir |
| `main.py` | Komut satırı arayüzü, CSV rapor |
| `ek_sozluk.txt` | zeyrek sözlüğünde eksik olan doğru kelimeler |
| `turkce.py`, `hata.py` | Ortak yardımcılar |

## Bilinen sınırlamalar
- Matematik formülleri PDF'ten metin olarak okunamadığı için denetlenmez.
- "Sözlükte bulunamayan kelime" bir *olası* hatadır; terimler ve özel kelimeler için `ek_sozluk.txt` kullanılabilir.
- zeyrek 0.1.3'teki sıraya bağlı çözümleme hatası `yazim_denetimi.zeyrek_hatasini_duzelt()` ile giderilmiştir.
