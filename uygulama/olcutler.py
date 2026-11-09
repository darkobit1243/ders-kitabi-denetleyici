"""Bulguların, Talim ve Terbiye Kurulu Başkanlığının (TTKB) taslak ders kitabı incelemesinde kullandığı
ölçüt başlıklarıyla eşleştirilmesi.

TTKB'nin yayımladığı inceleme ölçütlerinde, diğerlerinin yanında "bilimsel yeterlik" ve "dil ve anlatım
yeterliği" başlıkları yer alır. Bu program yalnızca bu iki başlıkla ilgili bazı konuları otomatik olarak
tarayan bir ön inceleme aracıdır; resmî incelemenin yerine geçmez.
"""

BILIMSEL = "Bilimsel Yeterlik"
DIL_ANLATIM = "Dil ve Anlatım Yeterliği"
OLCUT_SIRASI = [BILIMSEL, DIL_ANLATIM]

ALT_BASLIK_SIRASI = [
    "Bilgi tutarlılığı",
    "Yazım ve noktalama",
    "Yazım birliği",
    "Seviyeye uygunluk ve okunabilirlik",
]


def olcut(hata) -> tuple:
    """Bir bulgunun (ölçüt, alt başlık) karşılığını döndürür."""
    if hata.kriter == "Tutarlılık":
        if hata.aciklama.startswith("Yazım birliği"):
            return DIL_ANLATIM, "Yazım birliği"
        return BILIMSEL, "Bilgi tutarlılığı"
    if hata.kriter == "Yazım":
        return DIL_ANLATIM, "Yazım ve noktalama"
    return DIL_ANLATIM, "Seviyeye uygunluk ve okunabilirlik"


def olcut_etiketi(hata) -> str:
    ana, alt = olcut(hata)
    return f"{ana} – {alt}"
