# Ders Kitabı Denetleyici

**Ders Kitaplarında İçerik ve Tutarlılık Hatalarının Otomatik Tespiti** · Sürüm 1.0.0

PDF formatındaki ders kitaplarından metni çıkarır, üç kritere göre olası hataları bulur ve her
bulguyu açıklaması, önerisi ve **sayfa/paragraf** bilgisiyle gösterir. Bulunan hata, kitabın ilgili
sayfası üzerinde işaretlenerek görüntülenir.

Millî Eğitim Bakanlığına sunulmak üzere geliştirilmiş öğrenci projesidir. Geliştiren: Efe Talha Mutlu.

> **Yerel çalışma:** Program tamamen bilgisayar üzerinde çalışır. Kitaplar ve sonuçlar hiçbir
> sunucuya veya yapay zekâ servisine gönderilmez. Arayüz yalnızca bu bilgisayardan
> (`localhost`) erişilebilir; Streamlit kullanım istatistikleri kapalıdır. İnternet bağlantısı
> yalnızca ilk kurulumda paketleri indirmek için gerekir (bkz. *Çevrimdışı kurulum*).

## Denetlenen kriterler
1. **Yazım ve noktalama** – Türkçe'de sık yapılan yazım hataları listesi, Türkçe biçimbilim
   çözümleyicisi (zeyrek) ile sözlükte bulunmayan kelimeler, noktalama kuralları.
2. **Bilgi tutarlılığı** – kitabın farklı yerlerinde farklı sayılarla verilen aynı bilgi
   ("%97'si okyanuslarda" / "%87'si okyanuslarda") ve aynı kelimenin farklı yazılışları
   ("eş kenar" / "eşkenar"). Cümle benzerliği Türkçe için "ilk 5 harf" kök bulma yöntemiyle ölçülür.
3. **Yaş seviyesine uygunluk** – Ateşman okunabilirlik puanı (İlkokul en az 70, Ortaokul 50,
   Lise 30) ve sınıf düzeyine göre çok uzun cümleler (İlkokul 12, Ortaokul 18, Lise 25 kelime).
   Kitabın geneli için Türkçe'ye özgü üç formül birlikte raporlanır: Ateşman (1997),
   Çetinkaya-Uzun (2010) ve Bezirci-Yılmaz (2010).

### İnceleme ölçütleriyle eşleştirme
Bulgular, Talim ve Terbiye Kurulu Başkanlığının taslak ders kitabı incelemesinde kullandığı ölçüt
başlıklarından **Bilimsel Yeterlik** (bilgi tutarlılığı) ve **Dil ve Anlatım Yeterliği** (yazım ve
noktalama, yazım birliği, okunabilirlik) altında gruplanır. Program bir **ön inceleme** aracıdır;
resmî incelemenin yerine geçmez ve bu ölçütlerin tamamını kapsamaz.

## Doğruluk ölçümü
`uygulama\degerlendirme.py`, gerçek bir ders kitabının rastgele seçilen paragraflarına türü bilinen
hatalar ekleyip programın bunları bulup bulmadığını ölçer. 9. Sınıf matematik ders kitabında
(her türden 100 örnek):

| Eklenen hata türü | Bulunan |
|---|---|
| Yazım hatası (kelimeden bir harf eksik) | %98 |
| Noktalama (virgülden önce boşluk) | %100 |
| Çelişen sayısal bilgi | %100 |
| Çok uzun cümle | %100 |

Hata eklenmemiş 500 paragrafta 39 yazım/noktalama bulgusu çıkmıştır (bir kısmı kitaptaki gerçek
hatalar, bir kısmı yanlış alarm). Noktalama, çelişki ve uzun cümle testleri kuralların gerçek kitap
metninde çalıştığını gösterir; kitapta doğal olarak bulunabilecek her hatanın bulunacağı anlamına gelmez.
```
.venv\Scripts\python degerlendirme.py ..\ornekler\kitap.pdf --sinif 9
```

## Klasör düzeni
```
DersKitabiDenetleyici/
├── KURULUM.bat     ← ilk kullanımda bir kez çift tıklayın
├── BASLAT.bat      ← programı açar (kurulumdan sonra masaüstü simgesi de kullanılabilir)
├── README.md       ← bu kılavuz
├── ornekler/       ← örnek kitap PDF'leri (buraya eklenen PDF'ler arayüzde listelenir)
└── uygulama/       ← programın kendisi; kullanıcının değiştirmesi gerekmez
```

## Kurulum (Windows)
1. [Python](https://www.python.org/downloads/) **3.11 veya üstünü** kurun. Kurulumda
   **"Add python.exe to PATH"** seçeneğini işaretleyin.
2. **`KURULUM.bat`** dosyasına çift tıklayın. Kurulum:
   - gerekli paketleri `uygulama\.venv` sanal ortamına kurar (bilgisayardaki diğer programlar etkilenmez),
   - masaüstüne ve Başlat menüsüne **"Ders Kitabı Denetleyici"** kısayolu ekler.

Taranmış (resim) sayfaları okumak için gereken Türkçe/İngilizce OCR dil dosyaları programla birlikte
gelir (`uygulama\tessdata`); ayrıca Tesseract kurmaya gerek yoktur.

**Kaldırma:** `uygulama\kaldir.bat` kısayolları ve kurulan paketleri siler; ardından klasör silinebilir.

### Çevrimdışı kurulum (internet bağlantısı olmayan bilgisayar)
1. İnternet bağlantısı olan bir bilgisayarda `uygulama\paketleri_hazirla.bat` dosyasını çalıştırın.
   Paketler `uygulama\paketler` klasörüne indirilir.
2. Program klasörünün tamamını hedef bilgisayara kopyalayıp `KURULUM.bat` dosyasını çalıştırın.
   Paketler internete bağlanmadan bu klasörden kurulur.

İki bilgisayarda Python sürümü ve Windows mimarisi (64 bit) aynı olmalıdır.

## Kullanım
1. Masaüstündeki **Ders Kitabı Denetleyici** simgesine veya **`BASLAT.bat`** dosyasına çift tıklayın.
   Tarayıcıda `http://localhost:8501` adresi açılır. Açılan siyah pencere program çalıştığı sürece
   kapatılmamalıdır; programı kapatmak için bu pencereyi kapatın.
2. Soldan PDF dosyasını yükleyin veya örnek kitaplardan birini seçin, sınıf düzeyini belirleyin
   ve **Denetle** butonuna basın.
3. Bulgular tabloda listelenir; kritere göre süzülebilir ve aranabilir. Tablodan bir satır
   seçildiğinde kitabın ilgili sayfası açılır: paragraf renkli bir kutuyla, yazım hatası olan
   kelime sarıyla işaretlenir.
4. **Denetim raporu** (yazdırılabilir HTML, tarayıcıda Ctrl+P ile PDF olarak kaydedilebilir) ve
   **bulgu tablosu** (Excel ile açılan CSV) indirilebilir.

### Komut satırı (`uygulama` klasöründe)
```
.venv\Scripts\python main.py ..\ornekler\kitap.pdf --sinif 9   # bulguları listeler, CSV ve HTML rapor oluşturur
.venv\Scripts\python main.py ..\ornekler\kitap.pdf --paragraflar
.venv\Scripts\python ornek_pdf_olustur.py                       # bilinçli hatalar içeren test PDF'i oluşturur
```

## Testler (`uygulama` klasöründe)
```
.venv\Scripts\python -m unittest discover -s testler -v
```
26 test; Türkçe yardımcı fonksiyonlar, PDF okuma, formül filtresi, üç kriterin her biri, üç
okunabilirlik formülü (elle hesaplanmış değerlerle), inceleme ölçütü eşleştirmesi, zeyrek düzeltmesi,
internetsiz çalışma, test PDF'i üzerinde uçtan uca denetim ve ön inceleme raporunu kapsar.

## `uygulama` klasöründeki dosyalar
| Dosya | Görevi |
|---|---|
| `arayuz.py` | Yerel web arayüzü (Streamlit) |
| `denetleyici.py` | Bütün adımları birleştirir |
| `pdf_okuyucu.py` | PDF'ten metni sayfa/paragraf bilgisiyle çıkarır, gerekirse OCR yapar |
| `metin_filtresi.py` | Formül ve tablo parçalarını denetim dışında bırakır |
| `yazim_denetimi.py` | Kriter 1: yazım ve noktalama |
| `tutarlilik.py` | Kriter 2: çelişen sayısal bilgiler ve yazım birliği |
| `yas_seviyesi.py` | Kriter 3: Ateşman okunabilirlik ve cümle uzunluğu |
| `okunabilirlik.py` | Ateşman, Çetinkaya-Uzun ve Bezirci-Yılmaz formülleri |
| `olcutler.py` | Bulguların TTKB inceleme ölçütü başlıklarıyla eşleştirilmesi |
| `degerlendirme.py`, `degerlendirme_sonucu.json` | Doğruluk ölçümü ve sonucu |
| `rapor.py` | Yazdırılabilir ön inceleme raporu |
| `main.py` | Komut satırı kullanımı |
| `ek_sozluk.txt` | Sözlükte eksik olan doğru kelimeler (her satıra bir kelime eklenebilir) |
| `turkce.py`, `hata.py`, `surum.py` | Ortak yardımcılar ve uygulama bilgileri |
| `stil.py`, `simge.png`, `simge.ico` | Arayüz tasarımı ve program simgesi |
| `kisayol.ps1`, `kaldir.bat`, `paketleri_hazirla.bat` | Kısayol, kaldırma, çevrimdışı paket hazırlama |
| `tessdata/` | OCR dil dosyaları (Tesseract, Apache 2.0) |
| `testler/` | Otomatik testler |

## Bilinen sınırlamalar
- Bulgular **olası** hatalardır; her bulgunun bir uzman tarafından kitapta kontrol edilmesi gerekir.
- Matematik formülleri ve tablolar PDF'ten metin olarak okunamadığı için denetlenmez.
- Taranmış sayfalarda OCR okuma hataları olabileceğinden sözlük kontrolü yapılmaz. Düşük
  çözünürlüklü taramalarda OCR kalitesi düşer.
- Kurallar ağırlıklı olarak 9. sınıf matematik ders kitabı üzerinde ayarlanmıştır; başka derslerin
  kitaplarında sahte bulgu oranı farklı olabilir.
- zeyrek 0.1.3'teki sıraya bağlı çözümleme hatası `yazim_denetimi.zeyrek_hatasini_duzelt()` ile
  giderilmiştir; bu nedenle zeyrek sürümü değiştirilmemelidir.

## Kullanılan açık kaynak bileşenler
PyMuPDF (AGPL-3.0), zeyrek (MIT), Streamlit (Apache 2.0), pandas (BSD-3), Tesseract OCR dil
dosyaları (Apache 2.0).
