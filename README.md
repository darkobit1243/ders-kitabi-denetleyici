# Ders Kitaplarında İçerik ve Tutarlılık Hatalarının Otomatik Tespiti

PDF formatındaki ders kitaplarından metni çıkarır ve üç kritere göre olası hataları
sayfa/paragraf bilgisiyle gösterir.

## Kriterler
1. **Yazım ve noktalama hataları** – sık yapılan yazım hataları listesi, Türkçe biçimbilim
   çözümleyicisi (zeyrek) ile sözlükte bulunmayan kelimeler, basit noktalama kuralları
2. **Bilgi tutarlılığı** – kitabın farklı yerlerinde farklı sayılarla verilen aynı bilgi
   ("%97'si okyanuslarda" / "%87'si okyanuslarda") ve aynı kelimenin farklı yazılışları
   ("eş kenar" / "eşkenar"). Cümle benzerliği Türkçe için "ilk 5 harf" kök bulma yöntemiyle ölçülür.
3. **Yaş seviyesine uygunluk** – Ateşman okunabilirlik formülü ve sınıf düzeyine göre çok uzun cümleler

## Kurulum
```
pip install -r requirements.txt
```
İnternet bağlantısı yalnızca kurulum sırasında gerekir; program çalışırken internete bağlanmaz.
Taranmış (resim) sayfalar için [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
Türkçe dil paketiyle kurulmalıdır.

## Kullanım

### Arayüz (önerilen)
`baslat.bat` dosyasına çift tıklayın veya:
```
streamlit run arayuz.py
```
Tarayıcıda `http://localhost:8501` açılır. PDF yükleyin (ya da `ornekler` klasöründen seçin),
sınıf düzeyini seçip **Denetle**'ye basın. Tablodan bir bulgu seçildiğinde ilgili sayfa,
paragraf kırmızı kutu ve hatalı kelime sarı vurguyla gösterilir. Rapor CSV olarak indirilebilir.

Program **tamamen yerel** çalışır: sunucu yalnızca `localhost` adresini dinler, Streamlit
kullanım istatistikleri kapalıdır (`.streamlit/config.toml`) ve hiçbir dosya internete gönderilmez.

### Komut satırı
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
| `tutarlilik.py` | Kriter 2: çelişen sayısal bilgiler ve yazım birliği |
| `yas_seviyesi.py` | Kriter 3: Ateşman okunabilirlik ve cümle uzunluğu |
| `denetleyici.py` | Bütün adımları birleştirir |
| `arayuz.py` | Streamlit web arayüzü (yerel) |
| `baslat.bat` | Arayüzü çift tıklayarak başlatır |
| `main.py` | Komut satırı arayüzü, CSV rapor |
| `ek_sozluk.txt` | zeyrek sözlüğünde eksik olan doğru kelimeler |
| `turkce.py`, `hata.py` | Ortak yardımcılar |

## Bilinen sınırlamalar
- Matematik formülleri PDF'ten metin olarak okunamadığı için denetlenmez.
- "Sözlükte bulunamayan kelime" bir *olası* hatadır; terimler ve özel kelimeler için `ek_sozluk.txt` kullanılabilir.
- zeyrek 0.1.3'teki sıraya bağlı çözümleme hatası `yazim_denetimi.zeyrek_hatasini_duzelt()` ile giderilmiştir.
