"""Streamlit web arayüzü. Yalnızca bu bilgisayarda (localhost) çalışır, internete bağlanmaz.

Başlatmak için:  BASLAT.bat dosyasına veya masaüstü kısayoluna çift tıklayın  (veya: streamlit run arayuz.py)
"""

import hashlib
import os
from datetime import datetime

import pandas as pd
import pymupdf
import streamlit as st

import stil
from denetleyici import kitabi_denetle
from pdf_okuyucu import TESSDATA
from rapor import KRITER_ACIKLAMALARI, html_rapor
from surum import ACIKLAMA, GELISTIRICI, SURUM, UYGULAMA_ADI

PROJE_KLASORU = os.path.dirname(os.path.abspath(__file__))
YUKLEME_KLASORU = os.path.join(PROJE_KLASORU, ".yuklenenler")  # OCR önbelleği dosya adını kullanıyor
ORNEKLER_KLASORU = os.path.join(os.path.dirname(PROJE_KLASORU), "ornekler")   # program klasörünün yanında
KRITERLER = ["Yazım", "Tutarlılık", "Yaş seviyesi"]
KRITER_RENKLERI_PDF = {"Yazım": (0.78, 0.16, 0.16), "Tutarlılık": (0.12, 0.37, 0.75), "Yaş seviyesi": (0.9, 0.5, 0.0)}

st.set_page_config(page_title=UYGULAMA_ADI, page_icon=os.path.join(PROJE_KLASORU, "simge.png"),
                   layout="wide", initial_sidebar_state="expanded")
st.markdown(stil.CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def denetle(pdf_baytlari: bytes, dosya_adi: str, sinif: int):
    """Aynı PDF ve sınıf için denetimi bir kez yapar; sonucu Streamlit önbelleğinde saklar."""
    os.makedirs(YUKLEME_KLASORU, exist_ok=True)
    yol = os.path.join(YUKLEME_KLASORU, os.path.basename(dosya_adi))
    with open(yol, "wb") as f:
        f.write(pdf_baytlari)
    hatalar, ist = kitabi_denetle(yol, sinif)
    with pymupdf.open(yol) as belge:
        ist["sayfa_sayisi"] = len(belge)
    return hatalar, ist


def sayfa_goruntusu(pdf_baytlari: bytes, hata) -> bytes:
    """Hatanın bulunduğu sayfayı resim olarak çizer; paragrafı ve hatalı kelimeyi işaretler."""
    with pymupdf.open(stream=pdf_baytlari, filetype="pdf") as belge:
        sayfa = belge[hata.sayfa - 1]
        if hata.konum:
            kutu = pymupdf.Rect(hata.konum) + (-3, -3, 3, 3)
            sayfa.draw_rect(kutu, color=KRITER_RENKLERI_PDF.get(hata.kriter), width=2.5)
            # Yazım hatalarında kelimenin kendisini de sarı ile vurgula
            if hata.kriter == "Yazım" and len(hata.alinti) < 40 and not hata.alinti.startswith("..."):
                for r in sayfa.search_for(hata.alinti, clip=kutu):
                    vurgu = sayfa.add_highlight_annot(r)
                    vurgu.update()
        return sayfa.get_pixmap(dpi=120).tobytes("png")


def tabloya_cevir(hatalar) -> pd.DataFrame:
    return pd.DataFrame([{
        "Sayfa": h.sayfa,
        "Paragraf": h.paragraf_no,
        "Kriter": h.kriter,
        "Açıklama": h.aciklama,
        "Alıntı": h.alinti,
        "Öneri": h.oneri,
    } for h in hatalar], columns=["Sayfa", "Paragraf", "Kriter", "Açıklama", "Alıntı", "Öneri"])


def alt_bilgi():
    st.markdown(f'<div class="alt-bilgi">{UYGULAMA_ADI} {SURUM} · Geliştiren: {GELISTIRICI} · {ACIKLAMA}<br>'
                'Tüm işlemler bu bilgisayarda yapılır; dosyalar internete gönderilmez.</div>',
                unsafe_allow_html=True)


def karsilama():
    st.markdown('<div class="bolum-baslik">Nasıl kullanılır?</div>', unsafe_allow_html=True)
    for sutun, (no, baslik, metin) in zip(st.columns(3), [
        (1, "Kitabı seçin", "Soldaki panelden ders kitabının PDF dosyasını yükleyin veya örnek kitaplardan birini seçin."),
        (2, "Sınıf düzeyini belirleyin", "Yaş seviyesi denetimi, kitabın hitap ettiği sınıfa göre farklı ölçütler kullanır."),
        (3, "Denetimi başlatın", "Denetle butonuna basın. Bulgular sayfa ve paragraf bilgisiyle listelenir; "
                                 "bir bulgu seçildiğinde kitabın ilgili sayfası işaretlenmiş olarak gösterilir."),
    ]):
        sutun.markdown(stil.adim_karti(no, baslik, metin), unsafe_allow_html=True)

    st.markdown('<div class="bolum-baslik">Denetlenen kriterler</div>', unsafe_allow_html=True)
    for sutun, kriter in zip(st.columns(3), KRITERLER):
        sutun.markdown(stil.kriter_karti(kriter, KRITER_ACIKLAMALARI[kriter]), unsafe_allow_html=True)

    st.write("")
    with st.expander("Yöntem ve sınırlamalar"):
        st.markdown(
            "**Yazım ve noktalama.** Türkçe'de sık yapılan yazım hataları listesi, Türkçe biçimbilim "
            "çözümleyicisi (zeyrek) ile sözlükte bulunmayan kelimeler ve noktalama kuralları.\n\n"
            "**Bilgi tutarlılığı.** Kitabın bütünü taranır. Kelime kökleri neredeyse aynı olan ama farklı "
            "sayılar içeren bildirme cümleleri çelişki olarak raporlanır. Aynı kelimenin hem bitişik hem ayrı "
            "yazıldığı durumlar (ör. \"eş kenar\" / \"eşkenar\") da gösterilir.\n\n"
            "**Yaş seviyesi.** Her paragrafın Ateşman okunabilirlik puanı hesaplanır ve sınıf düzeyine göre "
            "belirlenen eşikle karşılaştırılır (ilkokul en az 70, ortaokul 50, lise 30). Sınıf düzeyine göre "
            "çok uzun cümleler ayrıca raporlanır (ilkokul 12, ortaokul 18, lise 25 kelime).\n\n"
            "**Sınırlamalar.** Bulgular *olası* hatalardır ve uzman kontrolü gerektirir. Matematik formülleri "
            "ve tablolar PDF'ten metin olarak okunamadığı için denetlenmez. Taranmış sayfalarda OCR kaynaklı "
            "okuma hataları olabileceği için sözlük kontrolü yapılmaz. Kurallar ağırlıklı olarak matematik "
            "ders kitabı üzerinde ayarlanmıştır."
        )


# ---------------- Kenar çubuğu: adım adım girişler ----------------
with st.sidebar:
    st.markdown(stil.kenar_baslik(), unsafe_allow_html=True)

    st.markdown(stil.kenar_adim(1, "Kitabı seçin"), unsafe_allow_html=True)
    ornekler = sorted(f for f in os.listdir(ORNEKLER_KLASORU) if f.lower().endswith(".pdf")) \
        if os.path.isdir(ORNEKLER_KLASORU) else []
    kaynak = st.radio("PDF kaynağı", ["Bilgisayardan yükle", "Örnek kitaplardan seç"],
                      disabled=not ornekler, label_visibility="collapsed")

    pdf_adi, pdf_baytlari = None, None
    if kaynak == "Bilgisayardan yükle":
        yuklenen = st.file_uploader("Ders kitabı PDF dosyası", type=["pdf"], label_visibility="collapsed")
        if yuklenen is not None:
            pdf_adi, pdf_baytlari = yuklenen.name, yuklenen.getvalue()
    else:
        pdf_adi = st.selectbox("Kitap", ornekler, label_visibility="collapsed")
        with open(os.path.join(ORNEKLER_KLASORU, pdf_adi), "rb") as f:
            pdf_baytlari = f.read()

    st.markdown(stil.kenar_adim(2, "Sınıf düzeyini belirleyin"), unsafe_allow_html=True)
    sinif = st.selectbox("Sınıf düzeyi", list(range(1, 13)), index=8, label_visibility="collapsed",
                         format_func=lambda s: f"{s}. sınıf  ({'ilkokul' if s <= 4 else 'ortaokul' if s <= 8 else 'lise'})")

    st.markdown(stil.kenar_adim(3, "Denetimi başlatın"), unsafe_allow_html=True)
    baslat = st.button("Denetle", type="primary", width="stretch", disabled=pdf_baytlari is None)

    ocr = "✔ Taranmış sayfalar için OCR hazır" if TESSDATA else "⚠ OCR dil dosyaları bulunamadı"
    st.markdown(f'<div class="durum">🔒 Yerel çalışma: dosyalar internete gönderilmez<br>{ocr}</div>',
                unsafe_allow_html=True)

# ---------------- Ana bölüm ----------------
st.markdown(stil.ust_bant(), unsafe_allow_html=True)

anahtar = (hashlib.md5(pdf_baytlari).hexdigest(), sinif) if pdf_baytlari else None

if baslat:
    with st.spinner("Kitap denetleniyor... Taranmış sayfalar varsa OCR birkaç dakika sürebilir."):
        try:
            st.session_state["sonuc"] = denetle(pdf_baytlari, pdf_adi, sinif)
            st.session_state["anahtar"] = anahtar
            st.session_state["tarih"] = datetime.now()
        except Exception as hata:   # bozuk veya şifreli PDF gibi durumlarda program çökmesin
            st.session_state.pop("anahtar", None)
            st.error("Dosya denetlenemedi. PDF dosyası bozuk, şifreli veya desteklenmeyen biçimde olabilir.\n\n"
                     f"Teknik ayrıntı: {hata}")

if anahtar is None or st.session_state.get("anahtar") != anahtar:
    if pdf_baytlari is not None:
        st.info(f"**{pdf_adi}** seçildi. Denetimi başlatmak için soldaki **Denetle** butonuna basın.")
    karsilama()
    alt_bilgi()
    st.stop()

hatalar, ist = st.session_state["sonuc"]
sayilar = {k: sum(h.kriter == k for h in hatalar) for k in KRITERLER}

# ---------------- Özet ----------------
tarih = st.session_state.get("tarih")
st.markdown(f'<div class="kitap-bilgi">📘 <b>{pdf_adi}</b> &nbsp;·&nbsp; {sinif}. sınıf &nbsp;·&nbsp; '
            f'{ist["sayfa_sayisi"]} sayfa &nbsp;·&nbsp; Denetim: {tarih:%d.%m.%Y %H:%M}</div>',
            unsafe_allow_html=True)

kartlar = [(ist["incelenen_paragraf"], "İncelenen paragraf", stil.LACIVERT),
           (ist["atlanan_paragraf"], "Atlanan formül/tablo", "#8a94a6")]
kartlar += [(sayilar[k], f"{k} bulgusu", stil.KRITER_RENKLERI_HEX[k]) for k in KRITERLER]
kartlar.append((len(hatalar), "Toplam olası hata", "#2e7d32"))
for sutun, (deger, etiket, renk) in zip(st.columns(len(kartlar)), kartlar):
    sutun.markdown(stil.ozet_karti(deger, etiket, renk), unsafe_allow_html=True)

if ist["metinsiz_sayfalar"]:
    st.warning(f"Şu sayfalarda metin okunamadı: {', '.join(map(str, ist['metinsiz_sayfalar']))}")

st.write("")
ad = os.path.splitext(pdf_adi)[0]
i1, i2, _ = st.columns([1, 1, 2])
i1.download_button("📄 Denetim raporu", html_rapor(hatalar, ist, pdf_adi, sinif, tarih).encode("utf-8"),
                   file_name=f"denetim_raporu_{ad}.html", mime="text/html", width="stretch",
                   help="Yazdırılabilir rapor; tarayıcıda açıp Ctrl+P ile PDF olarak kaydedebilirsiniz.")
i2.download_button("📊 Excel tablosu",
                   tabloya_cevir(hatalar).to_csv(index=False, sep=";").encode("utf-8-sig"),
                   file_name=f"bulgular_{ad}.csv", mime="text/csv", width="stretch", disabled=not hatalar,
                   help="Bütün bulgular; Excel ile açılabilen CSV dosyası.")

if not hatalar:
    st.success("Bu kitapta olası hata bulunamadı.")
    alt_bilgi()
    st.stop()

# ---------------- Bulgular ve sayfa önizleme ----------------
st.markdown('<div class="bolum-baslik">Bulgular</div>', unsafe_allow_html=True)
f1, f2 = st.columns([2, 1])
secenekler = ["Tümü"] + [k for k in KRITERLER if sayilar[k]]
secilen = f1.segmented_control(
    "Kriter", secenekler, default="Tümü", label_visibility="collapsed",
    format_func=lambda k: f"Tümü ({len(hatalar)})" if k == "Tümü" else f"{stil.KRITER_SIMGELERI[k]} {k} ({sayilar[k]})",
) or "Tümü"
arama = f2.text_input("Ara", placeholder="🔍 Bulgularda ara (ör. bulnuz, uzun)", label_visibility="collapsed")

gosterilecek = [h for h in hatalar if (secilen == "Tümü" or h.kriter == secilen)
                and (not arama or arama.lower() in (h.aciklama + " " + h.alinti).lower())]

sol, sag = st.columns([3, 2], gap="large")
with sol:
    st.caption(f"{len(gosterilecek)} bulgu · Kitabın ilgili sayfasını görmek için bir satır seçin.")
    secim = st.dataframe(
        tabloya_cevir(gosterilecek), width="stretch", hide_index=True, height=560,
        on_select="rerun", selection_mode="single-row",
        column_config={
            "Sayfa": st.column_config.NumberColumn(width="small"),
            "Paragraf": st.column_config.NumberColumn("Prg.", width="small"),
            "Kriter": st.column_config.TextColumn(width="small"),
            "Açıklama": st.column_config.TextColumn(width="large"),
            "Alıntı": st.column_config.TextColumn(width="medium"),
            "Öneri": st.column_config.TextColumn(width="medium"),
        },
    )

with sag:
    secili = secim.selection.rows
    if secili and secili[0] < len(gosterilecek):
        h = gosterilecek[secili[0]]
        renk = stil.KRITER_RENKLERI_HEX[h.kriter]
        st.markdown(f'<div class="bolum-baslik" style="margin-top:0">Sayfa {h.sayfa} · Paragraf {h.paragraf_no}'
                    f' · <span style="color:{renk}">{h.kriter}</span></div>', unsafe_allow_html=True)
        st.markdown(stil.ayrinti_karti("Açıklama", h.aciklama, renk), unsafe_allow_html=True)
        st.markdown(stil.ayrinti_karti("Alıntı", h.alinti, renk), unsafe_allow_html=True)
        if h.oneri:
            st.markdown(stil.ayrinti_karti("Öneri", h.oneri, renk), unsafe_allow_html=True)
        st.image(sayfa_goruntusu(pdf_baytlari, h), width="stretch")
    else:
        st.markdown('<div class="bos-onizleme">📄<br><br>Soldaki tablodan bir bulgu seçtiğinizde<br>'
                    'kitabın ilgili sayfası burada,<br>hatalı bölüm işaretlenmiş olarak gösterilir.</div>',
                    unsafe_allow_html=True)

alt_bilgi()
