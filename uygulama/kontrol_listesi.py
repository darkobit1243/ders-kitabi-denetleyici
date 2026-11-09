"""İnceleme kontrol listesi.

Kaynak: "Farklı Okul Türlerinde Kullanılan Ders Kitabı ile Diğer Eğitim Araç ve Gereçlerinin
İncelenmesine Esas Olacak Kriterler" (TTKB, 26.05.2025 tarihli ve 133204310 sayılı Kurul Mütalaası).
Belge; milletlerarası özel öğretim kurumları, yabancılar tarafından açılmış özel okullar, azınlık okulları
ve UDSP uygulayan ortaöğretim kurumlarının kitapları için hazırlanmıştır.

Madde metinleri kısaltılarak verilmiştir; resmî metin için belgenin kendisine başvurulmalıdır.
Programın otomatik taradığı maddeler "otomatik" alanında, ilgili bulgu etiketiyle (ör. "4.1") belirtilir.
Diğer maddeler bağlam ve uzman yorumu gerektirdiği için yalnızca kontrol listesinde yer alır.
"""

KAYNAK = ("TTKB, “Farklı Okul Türlerinde Kullanılan Ders Kitabı ile Diğer Eğitim Araç ve Gereçlerinin "
          "İncelenmesine Esas Olacak Kriterler”, 26.05.2025 tarihli ve 133204310 sayılı Kurul Mütalaası")
KAPSAM_NOTU = ("Bu kriterler milletlerarası özel öğretim kurumları, yabancılar tarafından açılmış özel okullar, "
               "azınlık okulları ve UDSP uygulayan ortaöğretim kurumlarının kitapları için hazırlanmıştır.")

# (madde, başlık, kısaltılmış içerik, otomatik tarama var mı)
MADDELER = [
    ("1", "Millî Güvenlik", None, None),
    ("1.1", None, "Millî birliğe ve bütünlüğe zarar veren unsur bulunmamalı.", False),
    ("1.2", None, "Toprak bütünlüğüne yönelik tehditleri meşrulaştıran veya destekleyen ifade, mesaj ya da ima bulunmamalı.", False),
    ("1.3", None, "Türk Bayrağı görseli yer alıyorsa Türk Bayrağı Kanunu'na uygun olmalı.", False),
    ("1.4", None, "Uluslararası itibarı, millî menfaatleri veya devlet kurumlarına saygıyı zedeleyecek ifade bulunmamalı.", False),
    ("1.5", None, "Terör örgütleriyle veya millî güvenliğe karşı faaliyet gösteren yapılarla ilişkili ifade bulunmamalı.", False),
    ("1.6", None, "Uluslararası ilişkilere ve uluslararası alandaki öneme aykırılık bulunmamalı.", False),
    ("2", "Eşitlik ve Kapsayıcılık", None, None),
    ("2.1", None, "Eşitlik ilkesi gözetilmeli, temel hak ve özgürlükler desteklenmeli.", False),
    ("2.2", None, "Hiçbir ayrım gözetilmeksizin insan haklarının herkes için geçerli olduğu ilkesi esas alınmalı.", False),
    ("2.3", None, "Toplumsal huzuru bozan veya toplumu ayrıştıran unsur bulunmamalı.", False),
    ("2.4", None, "Kültürel, etnik, dinî ve mezhepsel özellikler üzerinden olumsuz genelleme yapılmamalı.", False),
    ("2.5", None, "Farklı ülkelerin kültür, inanç ve geleneklerine hassasiyet gösterilmeli.", False),
    ("2.6", None, "Din ve vicdan hürriyeti, düşünce ve ifade özgürlüğü, adalet ve toplumsal barış gözetilmeli.", False),
    ("2.7", None, "Toplumsal kesimleri düşünce, inanç veya siyasi görüşleri nedeniyle küçük düşüren unsur bulunmamalı.", False),
    ("2.8", None, "Bireysel, sosyal ve mesleki kimlikleri küçülten ifade bulunmamalı.", False),
    ("2.9", None, "Sosyal konum veya gelir düzeyine göre bireyi aşağılayan ya da yücelten ifade bulunmamalı.", False),
    ("3", "Millî Kültür ve Değerler", None, None),
    ("3.1", None, "Millî ve manevi değerlere saygı gösterilmeli, din ve vicdan özgürlüğü korunmalı.", False),
    ("3.2", None, "Türk tarihiyle ilgili bilgiler yansız, doğru ve bilimsel olmalı.", False),
    ("3.3", None, "Millî kültüre ve millî bilince zarar veren unsur bulunmamalı.", False),
    ("4", "Güvenli, Etik ve Çevreci İçerik", None, None),
    ("4.1", None, "Kişisel Verilerin Korunması Kanunu'na aykırı unsur bulunmamalı.", True),
    ("4.2", None, "Reklam, ticari tercih veya yönlendirme bulunmamalı.", True),
    ("4.3", None, "Çocuk haklarına aykırı unsur bulunmamalı.", False),
    ("4.4", None, "Bağımlılık yapıcı, müstehcen veya kişilik gelişimini olumsuz etkileyen unsur bulunmamalı.", True),
    ("4.5", None, "Korku, şiddet, hakaret veya aşağılama içeren mesaj bulunmamalı.", True),
    ("4.6", None, "Yaş ve gelişim seviyesine uygun olmayan rol modeli, ürün, sembol veya imge bulunmamalı.", False),
    ("4.7", None, "Fiziksel gelişimi ve beden sağlığını olumsuz etkileyen öge bulunmamalı.", False),
    ("4.8", None, "Hayvan haklarına aykırı unsur bulunmamalı.", False),
    ("4.9", None, "Çevre bilincine ve çevresel sürdürülebilirliğe aykırı unsur bulunmamalı.", False),
]

TARAMA_ACIKLAMASI = {
    "4.1": "T.C. kimlik no (doğrulama algoritmasıyla), telefon, kişisel e-posta, IBAN",
    "4.2": "®/™ işareti, resmî kurum dışı web adresi, marka listesi, satış çağrıları",
    "4.4": "Bağımlılık yapıcı maddelere ilişkin kelimeler (kök eşleştirmesiyle)",
    "4.5": "Şiddet ve hakaret içeren kelimeler (kök eşleştirmesiyle)",
}


def madde_etiketi(hata) -> str:
    """İçerik güvenliği bulgusunun açıklamasındaki "[4.1]" etiketinden madde numarasını çıkarır."""
    if hata.aciklama.startswith("[") and "]" in hata.aciklama:
        return hata.aciklama[1:hata.aciklama.index("]")]
    return ""


def durumlar(hatalar) -> list:
    """Her madde için (madde, başlık, içerik, durum metni, bulgu sayısı) listesi."""
    sayilar = {}
    for h in hatalar:
        etiket = madde_etiketi(h)
        if etiket:
            sayilar[etiket] = sayilar.get(etiket, 0) + 1
    sonuc = []
    for madde, baslik, icerik, otomatik in MADDELER:
        if baslik:
            sonuc.append((madde, baslik, None, None, None))
        elif otomatik:
            n = sayilar.get(madde, 0)
            sonuc.append((madde, None, icerik, f"Otomatik tarandı: {TARAMA_ACIKLAMASI[madde]}", n))
        else:
            sonuc.append((madde, None, icerik, "Uzman değerlendirmesi gerekir", None))
    return sonuc
