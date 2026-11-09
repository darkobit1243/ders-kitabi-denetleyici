"""Bulguların, Talim ve Terbiye Kurulu Başkanlığının (TTKB) ders kitabı incelemesinde kullandığı
ölçüt başlıklarıyla eşleştirilmesi.

- "Bilimsel Yeterlik" ve "Dil ve Anlatım Yeterliği": TTKB'nin taslak ders kitabı inceleme ölçütleri.
- "Güvenli, Etik ve Çevreci İçerik": TTKB'nin 26.05.2025 tarihli Kurul Mütalaası ile kabul edilen kriterler
  (bkz. kontrol_listesi.py).

Bu program yalnızca bu başlıklarla ilgili bazı konuları otomatik olarak tarayan bir ön inceleme aracıdır;
resmî incelemenin yerine geçmez.
"""

from kontrol_listesi import madde_etiketi

BILIMSEL = "Bilimsel Yeterlik"
DIL_ANLATIM = "Dil ve Anlatım Yeterliği"
GUVENLI = "Güvenli, Etik ve Çevreci İçerik"
OLCUT_SIRASI = [BILIMSEL, DIL_ANLATIM, GUVENLI]

GUVENLI_ALT_BASLIKLAR = {
    "4.1": "4.1 Kişisel verilerin korunması",
    "4.2": "4.2 Reklam ve ticari yönlendirme",
    "4.4": "4.4 Bağımlılık yapıcı unsurlar",
    "4.5": "4.5 Şiddet, hakaret ve aşağılama",
}

ALT_BASLIK_SIRASI = [
    "Bilgi tutarlılığı",
    "Yazım ve noktalama",
    "Yazım birliği",
    "Seviyeye uygunluk ve okunabilirlik",
] + list(GUVENLI_ALT_BASLIKLAR.values())


def olcut(hata) -> tuple:
    """Bir bulgunun (ölçüt, alt başlık) karşılığını döndürür."""
    if hata.kriter == "İçerik Güvenliği":
        return GUVENLI, GUVENLI_ALT_BASLIKLAR.get(madde_etiketi(hata), "Diğer")
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
