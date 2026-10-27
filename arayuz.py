"""Streamlit web arayüzü. Yalnızca bu bilgisayarda (localhost) çalışır, internete bağlanmaz.

Başlatmak için:  streamlit run arayuz.py   (veya baslat.bat dosyasına çift tıklayın)
"""

import hashlib
import os

import pandas as pd
import pymupdf
import streamlit as st

from denetleyici import kitabi_denetle

YUKLEME_KLASORU = ".yuklenenler"   # yüklenen PDF'ler burada tutulur (OCR önbelleği dosya adını kullanıyor)
KRITER_RENKLERI = {"Yazım": (0.85, 0.1, 0.1), "Yaş seviyesi": (0.95, 0.55, 0.0), "Tutarlılık": (0.1, 0.35, 0.85)}

st.set_page_config(page_title="Ders Kitabı Denetleyici", page_icon="📘", layout="wide")


@st.cache_data(show_spinner=False)
def denetle(pdf_baytlari: bytes, dosya_adi: str, sinif: int):
    """Aynı PDF ve sınıf için denetimi bir kez yapar; sonucu Streamlit önbelleğinde saklar."""
    os.makedirs(YUKLEME_KLASORU, exist_ok=True)
    yol = os.path.join(YUKLEME_KLASORU, dosya_adi)
    with open(yol, "wb") as f:
        f.write(pdf_baytlari)
    hatalar, istatistik = kitabi_denetle(yol, sinif)
    return hatalar, istatistik


def sayfa_goruntusu(pdf_baytlari: bytes, hata) -> bytes:
    """Hatanın bulunduğu sayfayı resim olarak çizer; paragrafı ve hatalı kelimeyi işaretler."""
    with pymupdf.open(stream=pdf_baytlari, filetype="pdf") as belge:
        sayfa = belge[hata.sayfa - 1]
        renk = KRITER_RENKLERI.get(hata.kriter, (0.85, 0.1, 0.1))
        if hata.konum:
            kutu = pymupdf.Rect(hata.konum)
            sayfa.draw_rect(kutu, color=renk, width=2)
            # Yazım hatalarında kelimenin kendisini de sarı ile vurgula
            if hata.kriter == "Yazım" and len(hata.alinti) < 40 and not hata.alinti.startswith("..."):
                for r in sayfa.search_for(hata.alinti, clip=kutu):
                    vurgu = sayfa.add_highlight_annot(r)
                    vurgu.update()
        return sayfa.get_pixmap(dpi=110).tobytes("png")


def tabloya_cevir(hatalar) -> pd.DataFrame:
    return pd.DataFrame([{
        "Sayfa": h.sayfa,
        "Paragraf": h.paragraf_no,
        "Kriter": h.kriter,
        "Açıklama": h.aciklama,
        "Alıntı": h.alinti,
        "Öneri": h.oneri,
    } for h in hatalar])


ORNEKLER_KLASORU = "ornekler"

# ---------------- Kenar çubuğu: girişler ----------------
with st.sidebar:
    st.header("📘 Ders Kitabı Denetleyici")
    ornekler = sorted(f for f in os.listdir(ORNEKLER_KLASORU) if f.lower().endswith(".pdf")) \
        if os.path.isdir(ORNEKLER_KLASORU) else []
    kaynak = st.radio("PDF kaynağı", ["Dosya yükle", "ornekler klasöründen seç"], disabled=not ornekler)

    pdf_adi, pdf_baytlari = None, None
    if kaynak == "Dosya yükle":
        yuklenen = st.file_uploader("Ders kitabı PDF dosyası", type=["pdf"])
        if yuklenen is not None:
            pdf_adi, pdf_baytlari = yuklenen.name, yuklenen.getvalue()
    else:
        pdf_adi = st.selectbox("Kitap", ornekler)
        with open(os.path.join(ORNEKLER_KLASORU, pdf_adi), "rb") as f:
            pdf_baytlari = f.read()

    sinif = st.selectbox("Sınıf düzeyi", list(range(1, 13)), index=8, format_func=lambda s: f"{s}. sınıf")
    baslat = st.button("Denetle", type="primary", width="stretch", disabled=pdf_baytlari is None)
    st.caption("Tüm işlemler bu bilgisayarda yapılır; dosyalar internete gönderilmez.")

st.title("Ders Kitaplarında İçerik ve Tutarlılık Hatalarının Otomatik Tespiti")

if pdf_baytlari is None:
    st.info("Başlamak için soldan bir PDF dosyası yükleyin ve **Denetle** butonuna basın.")
    st.markdown(
        "**Denetlenen kriterler**\n"
        "1. **Yazım ve noktalama** – sık yapılan yazım hataları, Türkçe sözlükte bulunmayan kelimeler, noktalama kuralları\n"
        "2. **Bilgi tutarlılığı** – kitabın farklı yerlerinde farklı sayılarla verilen aynı bilgi, "
        "aynı kelimenin farklı yazılışları\n"
        "3. **Yaş seviyesi** – Ateşman okunabilirlik puanı ve sınıf düzeyine göre çok uzun cümleler"
    )
    st.stop()

anahtar = (hashlib.md5(pdf_baytlari).hexdigest(), sinif)

if baslat:
    with st.spinner("Kitap denetleniyor... (taranmış sayfalar varsa OCR birkaç dakika sürebilir)"):
        st.session_state["sonuc"] = denetle(pdf_baytlari, pdf_adi, sinif)
        st.session_state["anahtar"] = anahtar

if st.session_state.get("anahtar") != anahtar:
    st.info("Dosya veya sınıf değişti. Sonuçları görmek için **Denetle** butonuna basın.")
    st.stop()

hatalar, ist = st.session_state["sonuc"]

# ---------------- Özet ----------------
s1, s2, s3, s4, s5 = st.columns(5)
s1.metric("İncelenen paragraf", ist["incelenen_paragraf"])
s2.metric("Atlanan (formül/tablo)", ist["atlanan_paragraf"])
s3.metric("Yazım", sum(h.kriter == "Yazım" for h in hatalar))
s4.metric("Tutarlılık", sum(h.kriter == "Tutarlılık" for h in hatalar))
s5.metric("Yaş seviyesi", sum(h.kriter == "Yaş seviyesi" for h in hatalar))
if ist["metinsiz_sayfalar"]:
    st.warning(f"Şu sayfalarda metin okunamadı: {ist['metinsiz_sayfalar']}")

if not hatalar:
    st.success("Hiç olası hata bulunamadı.")
    st.stop()

# ---------------- Filtreler ----------------
f1, f2 = st.columns([1, 2])
kriterler = sorted({h.kriter for h in hatalar})
secilen_kriterler = f1.multiselect("Kriter", kriterler, default=kriterler)
arama = f2.text_input("Ara (açıklama veya alıntı içinde)", placeholder="ör. uzun, bulnuz")

gosterilecek = [h for h in hatalar if h.kriter in secilen_kriterler
                and (not arama or arama.lower() in (h.aciklama + " " + h.alinti).lower())]
tablo = tabloya_cevir(gosterilecek)

st.caption(f"{len(gosterilecek)} bulgu gösteriliyor. Sayfada görmek için tablodan bir satır seçin.")
secim = st.dataframe(
    tablo, width="stretch", hide_index=True, height=380,
    on_select="rerun", selection_mode="single-row",
    column_config={
        "Sayfa": st.column_config.NumberColumn(width="small"),
        "Paragraf": st.column_config.NumberColumn(width="small"),
        "Açıklama": st.column_config.TextColumn(width="large"),
        "Alıntı": st.column_config.TextColumn(width="large"),
    },
)

st.download_button(
    "Raporu indir (CSV, Excel ile açılır)",
    tabloya_cevir(hatalar).to_csv(index=False, sep=";").encode("utf-8-sig"),
    file_name=f"rapor_{os.path.splitext(pdf_adi)[0]}.csv",
    mime="text/csv",
)

# ---------------- Seçilen bulgunun sayfası ----------------
secili_satirlar = secim.selection.rows
if secili_satirlar:
    h = gosterilecek[secili_satirlar[0]]
    st.subheader(f"Sayfa {h.sayfa}, Paragraf {h.paragraf_no} – {h.kriter}")
    sol, sag = st.columns([3, 2])
    sol.image(sayfa_goruntusu(pdf_baytlari, h), width="stretch")
    sag.markdown(f"**Açıklama:** {h.aciklama}")
    sag.markdown(f"**Alıntı:** {h.alinti}")
    if h.oneri:
        sag.markdown(f"**Öneri:** {h.oneri}")
