"""Streamlit web arayüzü. Yalnızca bu bilgisayarda (localhost) çalışır, internete bağlanmaz.

Başlatmak için:  baslat.bat dosyasına çift tıklayın  (veya: streamlit run arayuz.py)
"""

import hashlib
import os
from datetime import datetime

import pandas as pd
import pymupdf
import streamlit as st

from denetleyici import kitabi_denetle
from pdf_okuyucu import TESSDATA
from rapor import html_rapor
from surum import ACIKLAMA, GELISTIRICI, SURUM, UYGULAMA_ADI, UZUN_AD

PROJE_KLASORU = os.path.dirname(os.path.abspath(__file__))
YUKLEME_KLASORU = os.path.join(PROJE_KLASORU, ".yuklenenler")  # OCR önbelleği dosya adını kullanıyor
ORNEKLER_KLASORU = os.path.join(os.path.dirname(PROJE_KLASORU), "ornekler")   # program klasörünün yanında
KRITER_RENKLERI = {"Yazım": (0.85, 0.1, 0.1), "Yaş seviyesi": (0.95, 0.55, 0.0), "Tutarlılık": (0.1, 0.35, 0.85)}

st.set_page_config(page_title=UYGULAMA_ADI, page_icon="📘", layout="wide")


@st.cache_data(show_spinner=False)
def denetle(pdf_baytlari: bytes, dosya_adi: str, sinif: int):
    """Aynı PDF ve sınıf için denetimi bir kez yapar; sonucu Streamlit önbelleğinde saklar."""
    os.makedirs(YUKLEME_KLASORU, exist_ok=True)
    yol = os.path.join(YUKLEME_KLASORU, os.path.basename(dosya_adi))
    with open(yol, "wb") as f:
        f.write(pdf_baytlari)
    return kitabi_denetle(yol, sinif)


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


def alt_bilgi():
    st.divider()
    st.caption(f"{UYGULAMA_ADI} {SURUM} · Geliştiren: {GELISTIRICI} · {ACIKLAMA} "
               "Tüm işlemler bu bilgisayarda yapılır; dosyalar internete gönderilmez.")


# ---------------- Kenar çubuğu: girişler ----------------
with st.sidebar:
    st.header(f"📘 {UYGULAMA_ADI}")
    ornekler = sorted(f for f in os.listdir(ORNEKLER_KLASORU) if f.lower().endswith(".pdf")) \
        if os.path.isdir(ORNEKLER_KLASORU) else []
    kaynak = st.radio("PDF kaynağı", ["Dosya yükle", "Örnek kitaplardan seç"], disabled=not ornekler)

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

    st.divider()
    st.caption("🔒 Yerel çalışma: dosyalar internete gönderilmez.")
    if TESSDATA:
        st.caption("✔ Taranmış sayfalar için OCR hazır.")
    else:
        st.caption("⚠ OCR dil dosyaları bulunamadı; taranmış (resim) sayfalar okunamaz.")

st.title(UZUN_AD)
st.caption("Ders kitabı PDF dosyalarında yazım, bilgi tutarlılığı ve yaş seviyesine uygunluk denetimi")

with st.expander("Yöntem ve sınırlamalar"):
    st.markdown(
        "**1. Yazım ve noktalama.** Türkçe'de sık yapılan yazım hataları listesi, Türkçe biçimbilim "
        "çözümleyicisi (zeyrek) ile sözlükte bulunmayan kelimeler ve noktalama kuralları "
        "(noktalama işaretinden önce boşluk, virgülden sonra boşluk olmaması vb.).\n\n"
        "**2. Bilgi tutarlılığı.** Kitabın bütünü taranır. Kelime kökleri neredeyse aynı olan ama farklı "
        "sayılar içeren bildirme cümleleri çelişki olarak raporlanır. Aynı kelimenin hem bitişik hem ayrı "
        "yazıldığı durumlar (ör. \"eş kenar\" / \"eşkenar\") da gösterilir.\n\n"
        "**3. Yaş seviyesi.** Her paragrafın Ateşman okunabilirlik puanı hesaplanır ve sınıf düzeyine göre "
        "belirlenen eşikle karşılaştırılır (ilkokul en az 70, ortaokul 50, lise 30). Sınıf düzeyine göre "
        "çok uzun cümleler ayrıca raporlanır (ilkokul 12, ortaokul 18, lise 25 kelime).\n\n"
        "**Sınırlamalar.** Bulgular *olası* hatalardır ve uzman kontrolü gerektirir. Matematik formülleri "
        "ve tablolar PDF'ten metin olarak okunamadığı için denetlenmez. Taranmış sayfalarda OCR kaynaklı "
        "okuma hataları olabileceği için sözlük kontrolü yapılmaz. Kurallar ağırlıklı olarak matematik "
        "ders kitabı üzerinde ayarlanmıştır."
    )

if pdf_baytlari is None:
    st.info("Başlamak için soldan bir PDF dosyası yükleyin veya örnek kitaplardan birini seçin, "
            "sınıf düzeyini belirleyip **Denetle** butonuna basın.")
    alt_bilgi()
    st.stop()

anahtar = (hashlib.md5(pdf_baytlari).hexdigest(), sinif)

if baslat:
    with st.spinner("Kitap denetleniyor... (taranmış sayfalar varsa OCR birkaç dakika sürebilir)"):
        try:
            st.session_state["sonuc"] = denetle(pdf_baytlari, pdf_adi, sinif)
            st.session_state["anahtar"] = anahtar
            st.session_state["tarih"] = datetime.now()
        except Exception as hata:   # bozuk veya şifreli PDF gibi durumlarda program çökmesin
            st.session_state.pop("anahtar", None)
            st.error(f"Dosya denetlenemedi. PDF dosyası bozuk, şifreli veya desteklenmeyen biçimde olabilir.\n\n"
                     f"Teknik ayrıntı: {hata}")
            alt_bilgi()
            st.stop()

if st.session_state.get("anahtar") != anahtar:
    st.info("Sonuçları görmek için **Denetle** butonuna basın.")
    alt_bilgi()
    st.stop()

hatalar, ist = st.session_state["sonuc"]

# ---------------- Özet ----------------
st.subheader(f"Denetim sonucu: {pdf_adi} ({sinif}. sınıf)")
s1, s2, s3, s4, s5 = st.columns(5)
s1.metric("İncelenen paragraf", ist["incelenen_paragraf"])
s2.metric("Atlanan (formül/tablo)", ist["atlanan_paragraf"])
s3.metric("Yazım", sum(h.kriter == "Yazım" for h in hatalar))
s4.metric("Tutarlılık", sum(h.kriter == "Tutarlılık" for h in hatalar))
s5.metric("Yaş seviyesi", sum(h.kriter == "Yaş seviyesi" for h in hatalar))
if ist["metinsiz_sayfalar"]:
    st.warning(f"Şu sayfalarda metin okunamadı: {', '.join(map(str, ist['metinsiz_sayfalar']))}")

ad = os.path.splitext(pdf_adi)[0]
i1, i2, _ = st.columns([1, 1, 2])
i1.download_button(
    "📄 Denetim raporunu indir (yazdırılabilir)",
    html_rapor(hatalar, ist, pdf_adi, sinif, st.session_state.get("tarih")).encode("utf-8"),
    file_name=f"denetim_raporu_{ad}.html", mime="text/html", width="stretch",
)
i2.download_button(
    "📊 Bulgu tablosunu indir (Excel/CSV)",
    tabloya_cevir(hatalar).to_csv(index=False, sep=";").encode("utf-8-sig") if hatalar else b"",
    file_name=f"bulgular_{ad}.csv", mime="text/csv", width="stretch", disabled=not hatalar,
)

if not hatalar:
    st.success("Hiç olası hata bulunamadı.")
    alt_bilgi()
    st.stop()

# ---------------- Filtreler ----------------
f1, f2 = st.columns([1, 2])
kriterler = [k for k in ["Yazım", "Tutarlılık", "Yaş seviyesi"] if any(h.kriter == k for h in hatalar)]
secilen_kriterler = f1.multiselect("Kriter", kriterler, default=kriterler)
arama = f2.text_input("Ara (açıklama veya alıntı içinde)", placeholder="ör. uzun, bulnuz")

gosterilecek = [h for h in hatalar if h.kriter in secilen_kriterler
                and (not arama or arama.lower() in (h.aciklama + " " + h.alinti).lower())]

st.caption(f"{len(gosterilecek)} bulgu gösteriliyor. Sayfada görmek için tablodan bir satır seçin.")
secim = st.dataframe(
    tabloya_cevir(gosterilecek), width="stretch", hide_index=True, height=380,
    on_select="rerun", selection_mode="single-row",
    column_config={
        "Sayfa": st.column_config.NumberColumn(width="small"),
        "Paragraf": st.column_config.NumberColumn(width="small"),
        "Açıklama": st.column_config.TextColumn(width="large"),
        "Alıntı": st.column_config.TextColumn(width="large"),
    },
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

alt_bilgi()
