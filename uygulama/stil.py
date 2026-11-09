"""Arayüzün görsel tasarımı: renkler, CSS ve HTML parçaları.

Hiçbir dış kaynak (yazı tipi, CDN, internet adresi) kullanılmaz; simge base64 olarak sayfaya gömülür.
"""

import base64
import os
from html import escape

from surum import SURUM, UYGULAMA_ADI, UZUN_AD

LACIVERT = "#12315f"
KRITER_RENKLERI_HEX = {"Yazım": "#c62828", "Tutarlılık": "#1f5fbf", "Yaş Seviyesi": "#e67e00"}
KRITER_SIMGELERI = {"Yazım": "✎", "Tutarlılık": "⇄", "Yaş Seviyesi": "◔"}

_SIMGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simge.png")
with open(_SIMGE, "rb") as f:
    SIMGE_BASE64 = base64.b64encode(f.read()).decode()

CSS = f"""
<style>
/* Streamlit'in geliştirici menüsünü, Deploy butonunu ve üst renk şeridini gizle */
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
#MainMenu, footer {{ display: none !important; }}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1400px; }}

/* Üst bant */
.ust-bant {{ background: linear-gradient(135deg, {LACIVERT} 0%, #1d4a8a 100%); color: #fff;
  border-radius: 14px; padding: 22px 28px; display: flex; align-items: center; gap: 22px;
  margin-bottom: 18px; box-shadow: 0 4px 14px rgba(18, 49, 95, .18); }}
.ust-bant img {{ width: 68px; height: 68px; border-radius: 14px; background: #fff; padding: 4px; }}
.ust-bant h1 {{ color: #fff; font-size: 1.65rem; line-height: 1.25; margin: 0; padding: 0; font-weight: 700; }}
.ust-bant p {{ color: #d7e2f3; margin: 4px 0 0; font-size: .95rem; }}
.ust-satir {{ color: #b9c9e4; font-size: .78rem; letter-spacing: .06em; margin-bottom: 4px; font-weight: 600; }}
.rozetler {{ margin-left: auto; display: flex; flex-direction: column; gap: 6px; align-items: flex-end; }}
.rozet {{ background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.35); color: #fff;
  border-radius: 999px; padding: 3px 12px; font-size: .8rem; white-space: nowrap; }}

/* Kartlar */
.kart {{ background: #fff; border: 1px solid #e1e6ee; border-radius: 12px; padding: 16px 18px; height: 100%; }}
.kart h4 {{ margin: 0 0 6px; font-size: 1.02rem; color: {LACIVERT}; }}
.kart p {{ margin: 0; color: #4a5568; font-size: .9rem; line-height: 1.45; }}
.adim-no {{ display: inline-flex; width: 28px; height: 28px; border-radius: 50%; background: {LACIVERT};
  color: #fff; align-items: center; justify-content: center; font-weight: 700; margin-bottom: 8px; }}
.kriter-kart {{ border-left: 5px solid var(--renk); }}
.kriter-simge {{ font-size: 1.4rem; color: var(--renk); }}

/* Özet sayıları */
.ozet {{ background: #fff; border: 1px solid #e1e6ee; border-radius: 12px; padding: 14px 16px;
  border-top: 4px solid var(--renk, {LACIVERT}); }}
.ozet .deger {{ font-size: clamp(1.25rem, 2vw, 1.9rem); font-weight: 700; color: #1a202c; line-height: 1.1;
  white-space: nowrap; }}
.ozet .etiket {{ color: #5a6577; font-size: .85rem; margin-top: 2px; }}

/* Başlıklar ve bilgi kutuları */
.bolum-baslik {{ font-size: 1.1rem; font-weight: 700; color: {LACIVERT}; margin: 18px 0 8px; }}
.kitap-bilgi {{ background: #eef3fa; border: 1px solid #d3deee; border-radius: 10px; padding: 10px 14px;
  color: #1a202c; margin-bottom: 12px; }}
.bos-onizleme {{ border: 2px dashed #c9d3e2; border-radius: 12px; padding: 40px 20px; text-align: center;
  color: #6b778a; background: #fafbfd; }}
.ayrinti {{ background: #fff; border: 1px solid #e1e6ee; border-left: 5px solid var(--renk);
  border-radius: 10px; padding: 12px 14px; margin-bottom: 10px; font-size: .92rem; }}
.ayrinti b {{ color: {LACIVERT}; }}
.alt-bilgi {{ color: #6b778a; font-size: .8rem; text-align: center; margin-top: 28px;
  padding-top: 12px; border-top: 1px solid #e1e6ee; }}

/* Kenar çubuğu */
section[data-testid="stSidebar"] {{ background: #fff; border-right: 1px solid #e1e6ee; }}
.kenar-baslik {{ display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }}
.kenar-baslik img {{ width: 38px; height: 38px; border-radius: 8px; }}
.kenar-baslik span {{ font-weight: 700; color: {LACIVERT}; font-size: 1.05rem; line-height: 1.2; }}
.kenar-adim {{ font-weight: 700; color: {LACIVERT}; font-size: .9rem; margin: 14px 0 2px; }}
.durum {{ font-size: .82rem; color: #4a5568; background: #f4f6fa; border-radius: 8px; padding: 8px 10px;
  margin-top: 6px; line-height: 1.5; }}

/* Dosya yükleme alanını Türkçeleştir (Streamlit bu metinleri İngilizce gösteriyor) */
[data-testid="stFileUploaderDropzone"] button [data-testid="stMarkdownContainer"],
[data-testid="stFileUploaderDropzone"] button [data-testid="stIconMaterial"] {{ display: none !important; }}
[data-testid="stFileUploaderDropzone"] button::after {{ content: "📂  PDF dosyası seç"; font-size: .9rem; }}
[data-testid="stFileUploaderDropzoneInstructions"] span {{ display: none !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] > div::after {{ content: "veya dosyayı buraya sürükleyin (en fazla 500 MB)";
  font-size: .8rem; color: #6b778a; }}
</style>
"""


def ust_bant() -> str:
    return f"""
<div class="ust-bant">
  <img src="data:image/png;base64,{SIMGE_BASE64}" alt="">
  <div>
    <div class="ust-satir">MİLLÎ EĞİTİM BAKANLIĞINA SUNULMAK ÜZERE HAZIRLANMIŞ ÖĞRENCİ PROJESİ</div>
    <h1>{escape(UZUN_AD)}</h1>
    <p>Ders kitabı PDF dosyalarında yazım, bilgi tutarlılığı ve yaş seviyesine uygunluk denetimi</p>
  </div>
  <div class="rozetler">
    <span class="rozet">Sürüm {SURUM}</span>
    <span class="rozet">🔒 Çevrimdışı çalışır</span>
  </div>
</div>"""


def kenar_baslik() -> str:
    return (f'<div class="kenar-baslik"><img src="data:image/png;base64,{SIMGE_BASE64}" alt="">'
            f'<span>{escape(UYGULAMA_ADI)}</span></div>')


def kenar_adim(no: int, metin: str) -> str:
    return f'<div class="kenar-adim">{no}. {escape(metin)}</div>'


def adim_karti(no: int, baslik: str, metin: str) -> str:
    return f'<div class="kart"><div class="adim-no">{no}</div><h4>{escape(baslik)}</h4><p>{escape(metin)}</p></div>'


def kriter_karti(kriter: str, aciklama: str) -> str:
    renk = KRITER_RENKLERI_HEX[kriter]
    return (f'<div class="kart kriter-kart" style="--renk:{renk}"><div class="kriter-simge">'
            f'{KRITER_SIMGELERI[kriter]}</div><h4>{escape(kriter)}</h4><p>{escape(aciklama)}</p></div>')


def ozet_karti(deger: int, etiket: str, renk: str = LACIVERT) -> str:
    deger = f"{deger:,}".replace(",", ".")    # Türkçe binlik ayırıcı: 1.393
    return (f'<div class="ozet" style="--renk:{renk}"><div class="deger">{deger}</div>'
            f'<div class="etiket">{escape(etiket)}</div></div>')


def ayrinti_karti(baslik: str, metin: str, renk: str) -> str:
    return f'<div class="ayrinti" style="--renk:{renk}"><b>{escape(baslik)}</b><br>{escape(metin)}</div>'
