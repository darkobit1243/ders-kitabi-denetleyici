"""Programın dayandığı kurallar ve kaynaklar.

Arayüzdeki "Yöntem, Dayanaklar ve Sınırlamalar" bölümü ve ön inceleme raporundaki "Dayanaklar ve
Kaynaklar" bölümü buradan üretilir; böylece ikisi her zaman aynı bilgiyi gösterir.

Üç tür dayanak ayrı tutulur:
  RESMI      : resmî belge veya kurumların kuralları
  BILIMSEL   : akademik yayınlarla tanımlanmış yöntemler ve kullanılan açık kaynak araçlar
  PROJE      : bu projede belirlenen, resmî bir dayanağı olmayan kurallar (açıkça belirtilir)
"""

# (kriter, neye bakılıyor, dayanak türü, dayanak)
KRITER_DAYANAKLARI = [
    ("Yazım ve noktalama", "Sık yapılan yazım hataları, noktalama işaretinden önce/sonra boşluk, aynı bağlacın tekrarı",
     "Resmî", "Türk Dil Kurumu, Yazım Kılavuzu (yazım ve noktalama kuralları)"),
    ("Yazım ve noktalama", "Türkçe sözlükte bulunmayan kelimeler",
     "Bilimsel", "zeyrek biçimbilim çözümleyicisi (Zemberek-NLP sözlüğü)"),
    ("Bilgi tutarlılığı", "Kitabın farklı yerlerinde farklı sayılarla verilen aynı bilgi",
     "Bilimsel", "Türkçe için ilk 5 harf kök bulma yöntemi (Can ve diğerleri, 2008) ve Jaccard benzerliği"),
    ("Bilgi tutarlılığı", "Aynı kelimenin bitişik/ayrı veya tireli/tiresiz yazılması (yazım birliği)",
     "Resmî", "Türk Dil Kurumu, Yazım Kılavuzu (birleşik kelimelerin yazımı)"),
    ("Yaş seviyesi", "Kitabın genel okunabilirliği",
     "Bilimsel", "Ateşman (1997), Çetinkaya-Uzun (2010), Bezirci-Yılmaz (2010) okunabilirlik formülleri"),
    ("Yaş seviyesi", "Paragraf bazında okunabilirlik eşiği ve en uzun cümle sınırı",
     "Proje", "İlkokul / Ortaokul / Lise için eşikler bu projede belirlenmiştir; resmî bir ölçüt değildir"),
    ("İçerik güvenliği", "4.1 Kişisel veriler (T.C. kimlik no, telefon, e-posta, IBAN)",
     "Resmî", "TTKB 26.05.2025 kriterleri, madde 4.1; 6698 sayılı Kişisel Verilerin Korunması Kanunu"),
    ("İçerik güvenliği", "4.2 Reklam ve ticari yönlendirme",
     "Resmî", "TTKB 26.05.2025 kriterleri, madde 4.2"),
    ("İçerik güvenliği", "4.4 Bağımlılık yapıcı unsurlar, 4.5 Şiddet ve hakaret",
     "Resmî", "TTKB 26.05.2025 kriterleri, madde 4.4 ve 4.5 (taranan kelime listesi projede hazırlanmıştır)"),
    ("Bulguların gruplanması", "Bilimsel Yeterlik, Dil ve Anlatım Yeterliği başlıkları",
     "Resmî", "TTKB taslak ders kitabı başvuru kılavuzunda (2025) sayılan değerlendirme başlıkları"),
    ("Bulguların gruplanması", "Güvenli, Etik ve Çevreci İçerik başlığı ve 27 maddelik kontrol listesi",
     "Resmî", "TTKB 26.05.2025 tarihli ve 133204310 sayılı Kurul Mütalaası ile kabul edilen kriterler"),
]

RESMI_BELGELER = [
    "Talim ve Terbiye Kurulu Başkanlığı (2025). Farklı Okul Türlerinde Kullanılan Ders Kitabı ile Diğer Eğitim "
    "Araç ve Gereçlerinin İncelenmesine Esas Olacak Kriterler. 26.05.2025 tarihli ve 133204310 sayılı Kurul "
    "Mütalaası. (Milletlerarası özel öğretim kurumları, yabancılar tarafından açılmış özel okullar, azınlık "
    "okulları ve UDSP uygulayan ortaöğretim kurumları için.)",
    "Talim ve Terbiye Kurulu Başkanlığı (2024). 2025 Yılı Taslak Ders Kitabı Başvuru Kılavuzu.",
    "Türk Dil Kurumu. Yazım Kılavuzu.",
    "6698 sayılı Kişisel Verilerin Korunması Kanunu.",
]

BILIMSEL_KAYNAKLAR = [
    "Ateşman, E. (1997). Türkçede okunabilirliğin ölçülmesi. Dil Dergisi, 58.",
    "Bezirci, B. ve Yılmaz, A. E. (2010). Metinlerin okunabilirliğinin ölçülmesi üzerine bir yazılım kütüphanesi "
    "ve Türkçe için yeni bir okunabilirlik ölçütü. DEÜ Mühendislik Fakültesi Fen Bilimleri Dergisi, 12(3), 49-62.",
    "Çetinkaya, G. (2010). Türkçe metinlerin okunabilirlik düzeylerinin tanımlanması ve sınıflandırılması "
    "(Doktora tezi). Ankara Üniversitesi Sosyal Bilimler Enstitüsü. (Literatürde Çetinkaya-Uzun formülü "
    "olarak anılır.)",
    "Can, F., Koçberber, S., Balçık, E., Kaynak, C., Öcalan, H. Ç. ve Vursavaş, O. M. (2008). Information "
    "retrieval on Turkish texts. Journal of the American Society for Information Science and Technology, 59(3).",
]

DOGRULAMA_NOTU = ("Okunabilirlik formüllerinin katsayıları ve düzey tabloları, bu formülleri kullanan iki akademik "
                  "makaleden karşılaştırılarak doğrulanmıştır.")

ARACLAR = [
    "PyMuPDF – PDF'ten metin ve konum bilgisi çıkarma (AGPL-3.0)",
    "Tesseract OCR Türkçe ve İngilizce dil dosyaları – taranmış sayfaların okunması (Apache 2.0)",
    "zeyrek – Türkçe biçimbilim çözümleyicisi, Zemberek-NLP'nin Python uyarlaması (MIT)",
    "Streamlit ve pandas – yerel arayüz ve tablolar (Apache 2.0, BSD-3)",
]

PROJE_KURALLARI = [
    "Yaş seviyesi eşikleri: Ateşman puanı İlkokul en az 70, Ortaokul en az 50, Lise en az 30; en uzun cümle "
    "İlkokul 12, Ortaokul 18, Lise 25 kelime. Ateşman'ın düzey tablosu esas alınarak bu projede belirlenmiştir.",
    "Bezirci-Yılmaz değeri, kitabın kademesinin (İlköğretim 1-8, Lise 9-12) üst sınırını aşan paragraflar "
    "\"kademenin üstünde\" sayılır.",
    "Formül ve tablo parçaları (en az 4 gerçek kelime ve %70 kelime oranı taşımayan paragraflar) denetlenmez.",
    "Çelişki için iki cümlenin kök benzerliği en az 0,6 olmalı; soru, yönerge, başlık, \"bu/şu\" içeren cümleler "
    "ve Görsel/Şekil numaraları karşılaştırılmaz.",
    "Sık yapılan yazım hataları, ek sözlük, hassas ifade ve marka listeleri bu projede hazırlanmıştır ve "
    "düzenlenebilir dosyalarda tutulur.",
]

SINIRLAMALAR = [
    "Bulgular olası hatalardır; her biri bir uzman tarafından kitapta kontrol edilmelidir.",
    "Program bir ön inceleme aracıdır; TTKB'nin resmî incelemesinin yerine geçmez ve inceleme ölçütlerinin "
    "tamamını kapsamaz. Millî güvenlik, eşitlik, millî kültür gibi maddeler bağlam ve uzman yorumu gerektirdiği "
    "için otomatik taranmaz, yalnızca kontrol listesinde yer alır.",
    "Matematik formülleri ve tablolar PDF'ten metin olarak okunamadığı için denetlenmez.",
    "Taranmış sayfalarda OCR kaynaklı okuma hataları olabileceği için sözlük kontrolü yapılmaz.",
    "Kurallar ağırlıklı olarak 9. Sınıf matematik ders kitabı üzerinde ayarlanmıştır; başka derslerin "
    "kitaplarında sonuçlar farklı olabilir.",
]
