"""Test için içinde bilinçli hatalar bulunan küçük bir ders kitabı PDF'i oluşturur.

Çalıştır:  python ornek_pdf_olustur.py   ->  ornekler/ornek_kitap.pdf
"""

import os

import pymupdf

FONT = r"C:\Windows\Fonts\arial.ttf"   # Türkçe karakterler için

SAYFALAR = [
    [
        "1. ÜNİTE: SU DÖNGÜSÜ",
        "Su, doğada sürekli bir döngü içindedir. Güneşin ısıtmasıyla denizlerdeki su "
        "buharlaşır ve atmosfere yükselir. Bu olaya buharlaşma denir.",
        "Yükselen su buharı soğuyarak yoğunlaşır ve bulutları oluşturur. Bulutlardaki "
        "su damlacıkları birleşip ağırlaşınca yağmur, kar veya dolu olarak yeryüzüne "
        "düşer. Bu olaya yağış denir.",
        "Dünyadaki suyun yaklaşık %97'si okyanuslarda bulunur.",   # sonra tutarsızlık
    ],
    [
        "Yağışla yeryüzüne inen suyun bir kısmı toprağa sızar, bir kısmı ise akarsular "
        "aracılığıyla tekrar denizlere ulaşır. Böylece döngü yeniden başlar.",
        "Dünyadaki suyun yaklaşık %87'si okyanuslardadır.",        # tutarsız bilgi
        "Suyun hal değiştirmesi sırasında enerji alış verişi gerçekleşir ve bu enerji "
        "alış verişi, atmosferdeki termodinamik süreçlerin moleküler düzeydeki "
        "etkileşimleri bağlamında değerlendirildiğinde iklim sistemlerinin dinamik "
        "dengesinin sürdürülmesinde belirleyici bir rol üstlenmektedir.",  # yaş seviyesi
        "Herkez suyu tasarruflu kullanmalıdır.",                   # yazım hatası
    ],
]


def olustur(cikti="ornekler/ornek_kitap.pdf"):
    os.makedirs(os.path.dirname(cikti), exist_ok=True)
    belge = pymupdf.open()
    for sayfa_no, paragraflar in enumerate(SAYFALAR, start=1):
        sayfa = belge.new_page()
        sayfa.insert_font(fontname="arial", fontfile=FONT)
        y = 72
        for metin in paragraflar:
            kutu = pymupdf.Rect(72, y, 523, y + 120)
            # insert_textbox kalan boşluğu döndürür; kullanılan yüksekliği hesaplıyoruz
            kalan = sayfa.insert_textbox(kutu, metin, fontname="arial", fontsize=12)
            y += 120 - kalan + 14
        sayfa.insert_text((297, 800), str(sayfa_no), fontname="arial", fontsize=10)
    belge.save(cikti)
    print(f"Oluşturuldu: {cikti}")


if __name__ == "__main__":
    olustur()
