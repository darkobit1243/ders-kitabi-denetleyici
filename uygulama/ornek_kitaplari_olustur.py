"""Programı denemek için içinde bilinçli hatalar bulunan örnek ders kitapları ve cevap anahtarı oluşturur.

Çalıştır:  python ornek_kitaplari_olustur.py
Çıktı:     ../ornekler/Örnek Kitap - *.pdf  ve  ../ornekler/cevap_anahtari/Örnek Kitaplar - Cevap Anahtarı.pdf

Kitaplar gerçek bir yayın değildir; her sayfada deneme amaçlı olduğu yazar. Cevap anahtarındaki her satır,
programın bulması beklenen bir hatayı gösterir (sayfa, kriter, ifade).
"""

import os

import pymupdf

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORNEKLER = os.path.join(KOK, "ornekler")
CEVAP_KLASORU = os.path.join(ORNEKLER, "cevap_anahtari")
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_KALIN = r"C:\Windows\Fonts\arialbd.ttf"
LACIVERT = (0.07, 0.19, 0.37)
ALT_NOT = "Deneme amaçlı örnek kitaptır; içinde programı denemek için bilinçli hatalar vardır."

# Her kitap: dosya adı, ders, sınıf, kapak alt başlığı, sayfalar ve beklenen hatalar.
# Sayfa içeriği: ("baslik", metin) veya ("paragraf", metin). Kapak 1. sayfadır, içerik 2. sayfadan başlar.
# Beklenen hata: (sayfa, kriter, cevap anahtarında gösterilen ifade, bulguda aranacak metin, açıklama).
KITAPLAR = [
    {
        "dosya": "Örnek Kitap - Fen Bilimleri 5. Sınıf.pdf",
        "ders": "FEN BİLİMLERİ", "sinif": 5, "konu": "1. Ünite: Güneş, Dünya ve Ay",
        "sayfalar": [
            [
                ("baslik", "1. ÜNİTE: GÜNEŞ, DÜNYA VE AY"),
                ("baslik", "Güneş'in Yapısı ve Özellikleri"),
                ("paragraf", "Güneş, Dünya'ya en yakın yıldızdır. Kendi ısısını ve ışığını üreten dev bir gaz "
                             "kütlesidir. Güneş'ten gelen ışık ve ısı, Dünya'daki canlıların yaşamını sürdürmesi "
                             "için gereklidir."),
                ("paragraf", "Güneş'in Dünya etrafında döndüğünü düşünmek yalnış bir bilgidir. Aslında Dünya, "
                             "Güneş'in çevresinde dolanır."),
                ("paragraf", "Dünya , kendi ekseni etrafında dönerek gece ve gündüzü oluşturur. Dünya'nın Güneş'e "
                             "bakan yüzünde gündüz, diğer yüzünde gece yaşanır."),
                ("paragraf", "Dünya, Güneş'in çevresindeki bir turunu yaklaşık 365 günde tamamlar."),
            ],
            [
                ("baslik", "Ay'ın Hareketleri ve Evreleri"),
                ("paragraf", "Ay, Dünya'nın tek doğal uydusudur. Kendi ışığı yoktur; Güneş'ten aldığı ışığı yansıtır."),
                ("paragraf", "Ay'ı gece gökyüzünde gözlemledğimiz zaman her gece farklı bir şekilde görürüz. "
                             "Bu görünümlere Ay'ın evreleri denir."),
                ("paragraf", "Ay'ın Dünya etrafında dolanırken Güneş'ten aldığı ışığı yansıtan yüzeyinin Dünya'dan "
                             "görülebilen kısmının sürekli değişmesi sonucunda gözlemcinin bulunduğu konuma ve "
                             "zamana bağlı olarak farklı biçimlerde algılanan görünümler ortaya çıkmaktadır."),
                ("paragraf", "Dünya, Güneş'in çevresindeki bir turunu yaklaşık 356 günde tamamlar."),
                ("paragraf", "Etkinlik: Ay'ın evrelerini sınıfta canlandıralım. Bunun için bir el feneri ve "
                             "Ülker bisküvi paketi kullanabilirsiniz."),
            ],
            [
                ("baslik", "Ünite Değerlendirme"),
                ("paragraf", "1. Gece ve gündüz nasıl oluşur? Açıklayınız."),
                ("paragraf", "2. Ay'ın kendi ışığı var mıdır? Nedenini yazınız."),
                ("paragraf", "Etkinlik sonuçlarınızı ve sorularınızı fen.ogretmeni.ahmet@gmail.com adresine "
                             "gönderebilirsiniz."),
            ],
        ],
        "hatalar": [
            (2, "Yazım", "yalnış", "yalnış", "Doğrusu: yanlış (sık yapılan yazım hatası)"),
            (2, "Yazım", "Dünya ,", "önce boşluk", "Noktalama işaretinden önce boşluk bırakılmaz"),
            (3, "Yazım", "gözlemledğimiz", "gözlemledğimiz", "Doğrusu: gözlemlediğimiz (harf eksik)"),
            (3, "Yaş Seviyesi", "Ay'ın Dünya etrafında dolanırken ...", "Cümle çok uzun",
             "5. Sınıf için çok uzun cümle (31 kelime)"),
            (3, "Yaş Seviyesi", "Ay'ın Dünya etrafında dolanırken ...", "Ateşman",
             "Aynı paragrafın okunabilirliği 5. Sınıf için düşük"),
            (3, "Tutarlılık", "365 gün / 356 gün", "356", "Aynı bilgi 2. sayfada 365, 3. sayfada 356 gün olarak verilmiş"),
            (3, "İçerik Güvenliği", "Ülker", "Ülker", "4.2 Marka adı (ticari yönlendirme olabilir)"),
            (4, "İçerik Güvenliği", "fen.ogretmeni.ahmet@gmail.com", "gmail.com", "4.1 Kişisel e-posta adresi"),
        ],
    },
    {
        "dosya": "Örnek Kitap - Türkçe 3. Sınıf.pdf",
        "ders": "TÜRKÇE", "sinif": 3, "konu": "Okuma Metinleri",
        "sayfalar": [
            [
                ("baslik", "1. TEMA: OKUMA KÜLTÜRÜ"),
                ("baslik", "Benim Küçük Bahçem"),
                ("paragraf", "Evimizin arkasında küçük bir bahçe var. Bahçede domates, biber ve fasulye yetiştiriyoruz."),
                ("paragraf", "Her sabah erkenden kalkıyorum. Annemle birlikte bitkileri suluyoruz."),
                ("paragraf", "Şuan domatesler kızarmaya başladı. Bahçemizde hiç bir bitki kurumadı."),
                ("paragraf", "Babam kuşlar için bir yuva yaptı ve ve ağaca astı."),
            ],
            [
                ("baslik", "Sınıfımızın Kitaplığı"),
                ("paragraf", "Sınıfımızda küçük bir kitaplık kurduk. Ali, Ayşe,Zeynep ve ben evden kitap getirdik."),
                ("paragraf", "Öğretmenimiz, okuduğumuz kitapları defterimize yazmamızı ve her hafta sonunda en çok "
                             "beğendiğimiz kitabı arkadaşlarımıza anlatmamızı istedi."),
                ("paragraf", "Kitap okumak hiçbir zaman sıkıcı değildir. Her kitaptan yeni birşey öğreniriz."),
                ("paragraf", "Teneffüste arkadaşına aptal diyen Can, sonra çok üzüldü ve arkadaşından özür diledi."),
            ],
        ],
        "hatalar": [
            (2, "Yazım", "Şuan", "Şuan", "Doğrusu: şu an"),
            (2, "Yazım", "ve ve", "bağlaç", "Aynı bağlaç arka arkaya iki kez yazılmış"),
            (2, "Tutarlılık", "hiç bir / hiçbir", "hiç bir", "Kitapta hem ayrı hem bitişik yazılmış (doğrusu: hiçbir)"),
            (3, "Yazım", "Ayşe,Zeynep", "sonra boşluk", "Virgülden sonra boşluk bırakılmalı"),
            (3, "Yazım", "birşey", "birşey", "Doğrusu: bir şey"),
            (3, "Yaş Seviyesi", "Öğretmenimiz, okuduğumuz kitapları ...", "Cümle çok uzun",
             "3. Sınıf için çok uzun cümle (16 kelime)"),
            (3, "Yaş Seviyesi", "Öğretmenimiz, okuduğumuz kitapları ...", "Ateşman",
             "Aynı paragrafın okunabilirliği 3. Sınıf için düşük"),
            (3, "İçerik Güvenliği", "aptal", "aptal", "4.5 Hakaret içerebilecek ifade (bağlamı kontrol edilmeli)"),
        ],
    },
    {
        "dosya": "Örnek Kitap - Sosyal Bilgiler 7. Sınıf.pdf",
        "ders": "SOSYAL BİLGİLER", "sinif": 7, "konu": "2. Ünite: Kültür ve Miras",
        "sayfalar": [
            [
                ("baslik", "2. ÜNİTE: KÜLTÜR VE MİRAS"),
                ("baslik", "Osmanlı Devleti'nde Şehirler"),
                ("paragraf", "Osmanlılar İstanbul'u 1453 yılında fethetmiş ve şehri devletin yeni başkenti yapmıştır."),
                ("paragraf", "Şehirlerde camiler, medreseler, çarşılar ve hanlar kurulmuştur. Bu yapılar şehirlerin "
                             "ticari ve kültürel hayatını canlandırmıştır."),
                ("paragraf", "Eskiden kahvehanelerde insanlar sohbet eder, tütün ve nargile içerdi."),
                ("paragraf", "Müzede eski İstanbul haritasının orjinal hâli sergilenmektedir."),
            ],
            [
                ("baslik", "Kültürel Mirasımızı Koruyalım"),
                ("paragraf", "Osmanlılar İstanbul'u 1435 yılında fethetmiş ve şehri devletin yeni başkenti yapmıştır."),
                ("paragraf", "Geçmişten günümüze ulaşan tarihî eserlerin, el sanatlarının ve geleneklerin gelecek "
                             "kuşaklara aktarılabilmesi için toplumun bütün kesimlerinin bilinçli bir şekilde "
                             "sorumluluk alması ve koruma çalışmalarına katkı sağlaması gerekmektedir."),
                ("paragraf", "Örnek nüfus cüzdanında Ahmet Yılmaz adına 10000000146 numarası yazılıdır."),
                ("paragraf", "Ayrıntılı bilgi için www.tarihkitapevi.com adresini ziyaret edin ve serinin diğer "
                             "kitaplarını hemen satın alın."),
            ],
        ],
        "hatalar": [
            (2, "İçerik Güvenliği", "tütün", "tütün", "4.4 Bağımlılık yapıcı madde (bağlamı kontrol edilmeli)"),
            (2, "İçerik Güvenliği", "nargile", "nargile", "4.4 Bağımlılık yapıcı madde (bağlamı kontrol edilmeli)"),
            (2, "Yazım", "orjinal", "orjinal", "Doğrusu: orijinal"),
            (3, "Tutarlılık", "1453 / 1435", "1435",
             "İstanbul'un fetih yılı 2. sayfada 1453, 3. sayfada 1435 olarak verilmiş"),
            (3, "Yaş Seviyesi", "Geçmişten günümüze ulaşan ...", "Cümle çok uzun",
             "7. Sınıf için çok uzun cümle (27 kelime)"),
            (3, "Yaş Seviyesi", "Geçmişten günümüze ulaşan ...", "Ateşman",
             "Aynı paragrafın okunabilirliği 7. Sınıf için düşük"),
            (3, "İçerik Güvenliği", "10000000146", "10000000146",
             "4.1 T.C. kimlik numarası (doğrulama algoritmasına uyuyor)"),
            (3, "İçerik Güvenliği", "www.tarihkitapevi.com", "tarihkitapevi", "4.2 Resmî kurum dışı web adresi"),
            (3, "İçerik Güvenliği", "satın alın", "satın alın", "4.2 Satışa yönlendiren ifade"),
        ],
    },
]


def _yaz(sayfa, kutu, metin, boyut, kalin=False, renk=(0, 0, 0), hiza=0):
    """Metni kutuya yazar, kullanılan yüksekliği döndürür."""
    kalan = sayfa.insert_textbox(kutu, metin, fontname="kalin" if kalin else "normal", fontsize=boyut,
                                 color=renk, align=hiza)
    return kutu.height - kalan


def _yeni_sayfa(belge, ders, sinif, no):
    sayfa = belge.new_page()
    sayfa.insert_font(fontname="normal", fontfile=FONT)
    sayfa.insert_font(fontname="kalin", fontfile=FONT_KALIN)
    sayfa.draw_line((60, 50), (535, 50), color=LACIVERT, width=0.8)
    sayfa.insert_text((60, 44), f"{ders} {sinif}. SINIF", fontname="kalin", fontsize=8, color=LACIVERT)
    sayfa.draw_line((60, 790), (535, 790), color=(0.7, 0.7, 0.7), width=0.5)
    sayfa.insert_text((60, 803), ALT_NOT, fontname="normal", fontsize=7, color=(0.45, 0.45, 0.45))
    sayfa.insert_text((525, 803), str(no), fontname="normal", fontsize=9)
    return sayfa


def kitap_olustur(k):
    belge = pymupdf.open()
    # Kapak
    kapak = belge.new_page()
    kapak.insert_font(fontname="normal", fontfile=FONT)
    kapak.insert_font(fontname="kalin", fontfile=FONT_KALIN)
    kapak.draw_rect(pymupdf.Rect(0, 0, 595, 842), color=None, fill=LACIVERT)
    kapak.draw_rect(pymupdf.Rect(60, 470, 535, 560), color=None, fill=(1, 0.97, 0.88))
    _yaz(kapak, pymupdf.Rect(60, 230, 535, 300), k["ders"], 34, kalin=True, renk=(1, 1, 1), hiza=1)
    _yaz(kapak, pymupdf.Rect(60, 300, 535, 340), f"{k['sinif']}. SINIF", 24, kalin=True, renk=(1, 1, 1), hiza=1)
    _yaz(kapak, pymupdf.Rect(60, 350, 535, 380), k["konu"], 14, renk=(0.85, 0.9, 1), hiza=1)
    _yaz(kapak, pymupdf.Rect(75, 482, 520, 552),
         "DENEME AMAÇLI ÖRNEK KİTAP\nBu kitap gerçek bir yayın değildir. Ders Kitabı Denetleyici programını "
         "denemek için hazırlanmıştır ve içinde bilinçli olarak yerleştirilmiş hatalar vardır. Beklenen hatalar "
         "cevap anahtarında listelenmiştir.", 10, renk=(0.35, 0.25, 0), hiza=1)

    for no, icerik in enumerate(k["sayfalar"], start=2):
        sayfa = _yeni_sayfa(belge, k["ders"], k["sinif"], no)
        y = 80
        for tur, metin in icerik:
            if tur == "baslik":
                buyuk = metin.isupper()
                y += _yaz(sayfa, pymupdf.Rect(60, y, 535, y + 40), metin, 15 if buyuk else 12.5, kalin=True,
                          renk=LACIVERT) + (14 if buyuk else 8)
            else:
                y += _yaz(sayfa, pymupdf.Rect(60, y, 535, y + 200), metin, 11) + 14
    yol = os.path.join(ORNEKLER, k["dosya"])
    belge.save(yol)
    return yol


def cevap_anahtari_olustur():
    os.makedirs(CEVAP_KLASORU, exist_ok=True)
    belge = pymupdf.open()
    sayfa = belge.new_page()
    sayfa.insert_font(fontname="normal", fontfile=FONT)
    sayfa.insert_font(fontname="kalin", fontfile=FONT_KALIN)
    y = 50
    y += _yaz(sayfa, pymupdf.Rect(50, y, 545, y + 30), "Örnek Kitaplar – Cevap Anahtarı", 16, kalin=True,
              renk=LACIVERT) + 4
    y += _yaz(sayfa, pymupdf.Rect(50, y, 545, y + 60),
              "Aşağıdaki hatalar örnek kitaplara bilinçli olarak yerleştirilmiştir. Program, kitap kendi sınıf "
              "düzeyi seçilerek denetlendiğinde bu hataları bulmalıdır. Sayfa numaraları kitap sayfalarının "
              "altındaki numaralardır (kapak 1. sayfadır).", 9.5) + 10
    for k in KITAPLAR:
        if y > 700:
            sayfa = belge.new_page()
            sayfa.insert_font(fontname="normal", fontfile=FONT)
            sayfa.insert_font(fontname="kalin", fontfile=FONT_KALIN)
            y = 50
        y += _yaz(sayfa, pymupdf.Rect(50, y, 545, y + 22), f"{k['dosya'][:-4]}  (sınıf düzeyi: {k['sinif']}. Sınıf)",
                  11.5, kalin=True, renk=LACIVERT) + 4
        for s, kriter, ifade, _, aciklama in k["hatalar"]:
            satir = f"Sayfa {s}  ·  {kriter}  ·  \u201c{ifade}\u201d  –  {aciklama}"
            y += _yaz(sayfa, pymupdf.Rect(62, y, 545, y + 30), satir, 9.5) + 3
        y += 12
    yol = os.path.join(CEVAP_KLASORU, "Örnek Kitaplar - Cevap Anahtarı.pdf")
    belge.save(yol)
    return yol


if __name__ == "__main__":
    for kitap in KITAPLAR:
        print("Oluşturuldu:", kitap_olustur(kitap))
    print("Oluşturuldu:", cevap_anahtari_olustur())
