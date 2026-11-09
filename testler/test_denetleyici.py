"""Otomatik testler. Çalıştırmak için proje klasöründe:

    python -m unittest discover -s testler -v
"""

import os
import sys
import unittest

PROJE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJE)

import tutarlilik                                    # noqa: E402
import yas_seviyesi                                  # noqa: E402
import yazim_denetimi                                # noqa: E402
from denetleyici import kitabi_denetle               # noqa: E402
from metin_filtresi import incelenebilir_mi          # noqa: E402
from pdf_okuyucu import Paragraf, satirlari_birlestir  # noqa: E402
from turkce import cumlelere_bol, hece_sayisi, kucuk_harf  # noqa: E402

ORNEK_PDF = os.path.join(PROJE, "ornekler", "ornek_kitap.pdf")


def paragraf(metin, sayfa=1, no=1):
    return Paragraf(sayfa, no, metin, (0, 0, 100, 100))


class TurkceYardimcilari(unittest.TestCase):
    def test_kucuk_harf_turkce_i(self):
        self.assertEqual(kucuk_harf("IŞIK İzmir"), "ışık izmir")

    def test_hece_sayisi_unlulerden(self):
        self.assertEqual(hece_sayisi("kitaplarımızdan"), 6)
        self.assertEqual(hece_sayisi("su"), 1)

    def test_madde_isareti_cumle_ayirir(self):
        self.assertEqual(len(cumlelere_bol("• eğim • fonksiyon • değer")), 3)


class PdfOkuma(unittest.TestCase):
    def test_tireli_kelime_birlestirilir(self):
        self.assertEqual(satirlari_birlestir("öğren-\nciler okula"), "öğrenciler okula")

    def test_yumusak_tire_temizlenir(self):
        self.assertEqual(satirlari_birlestir("yö\xad\nnelik"), "yönelik")


class MetinFiltresi(unittest.TestCase):
    def test_formul_parcasi_atlanir(self):
        self.assertFalse(incelenebilir_mi("2 1 2 1 $ $ = c m"))

    def test_gercek_cumle_incelenir(self):
        self.assertTrue(incelenebilir_mi("Su doğada sürekli bir döngü içindedir."))


class YazimDenetimi(unittest.TestCase):
    def test_bilinen_yazim_hatasi_ve_oneri(self):
        hatalar = yazim_denetimi.denetle(paragraf("Herkez suyu tasarruflu kullanmalıdır."))
        self.assertEqual([(h.alinti, h.oneri) for h in hatalar], [("Herkez", "herkes")])

    def test_dogru_cumlede_hata_yok(self):
        self.assertEqual(yazim_denetimi.denetle(paragraf("Öğrenciler kitaplarını okula getirdi.")), [])

    def test_sozlukte_olmayan_kelime(self):
        hatalar = yazim_denetimi.denetle(paragraf("Sonucu tabloya yazarak bulnuz lütfen."))
        self.assertIn("bulnuz", [h.alinti for h in hatalar])

    def test_zeyrek_sira_hatasi_duzeltildi(self):
        # zeyrek 0.1.3'te "olacak" çözümlendikten sonra "olup" tanınmıyordu
        for kelime in ["olup", "olacak", "olup", "gösteren", "olup"]:
            self.assertTrue(yazim_denetimi.sozlukte_var_mi(kelime), kelime)

    def test_internet_verisi_gerekmez(self):
        # zeyrek'in NLTK ile kelime bölmesi devre dışı; çözümleme veri dosyası olmadan çalışmalı
        import zeyrek.morphology
        yazim_denetimi.cozumleyici()
        self.assertEqual(zeyrek.morphology._tokenize_text("kitap okul"), ["kitap", "okul"])

    def test_noktalama_virgulden_once_bosluk(self):
        hatalar = yazim_denetimi.denetle(paragraf("Elma , armut ve kiraz meyvedir."))
        self.assertTrue(any("önce boşluk" in h.aciklama for h in hatalar))


class YasSeviyesi(unittest.TestCase):
    def test_atesman_kisa_cumle_kolay(self):
        self.assertGreater(yas_seviyesi.atesman_puani("Ali top at. Ayşe ip atla."), 90)

    def test_uzun_cumle_ilkokulda_raporlanir(self):
        cumle = "Bu " + "uzun " * 15 + "cümle okunur."
        hatalar = yas_seviyesi.denetle(paragraf(cumle), sinif=3)
        self.assertTrue(any("Cümle çok uzun" in h.aciklama for h in hatalar))

    def test_ayni_cumle_lisede_raporlanmaz(self):
        cumle = "Bu " + "uzun " * 15 + "cümle okunur."
        hatalar = yas_seviyesi.denetle(paragraf(cumle), sinif=11)
        self.assertFalse(any("Cümle çok uzun" in h.aciklama for h in hatalar))


class Tutarlilik(unittest.TestCase):
    def test_celisen_sayilar_bulunur(self):
        ps = [paragraf("Dünyadaki suyun yaklaşık %97'si okyanuslarda bulunur.", 1),
              paragraf("Dünyadaki suyun yaklaşık %87'si okyanuslardadır.", 2)]
        self.assertEqual(len(tutarlilik.sayisal_celiskiler(ps)), 1)

    def test_farkli_nesneler_celiski_sayilmaz(self):
        ps = [paragraf("Resim kursu saat 10.00'da başlayıp 14.00'te bitmektedir.", 1),
              paragraf("Bale kursu saat 11.00'de başlayıp 13.00'te bitmektedir.", 2)]
        self.assertEqual(tutarlilik.sayisal_celiskiler(ps), [])

    def test_gorsel_numarasi_celiski_sayilmaz(self):
        ps = [paragraf("Pembe taburelerin yüksekliği ve aradaki mesafe Görsel 1'de verilmiştir.", 1),
              paragraf("Pembe taburelerin yüksekliği ve aradaki mesafe Görsel 2'de verilmiştir.", 2)]
        self.assertEqual(tutarlilik.sayisal_celiskiler(ps), [])

    def test_yazim_birligi(self):
        ps = [paragraf("Bir eş kenar üçgen çizelim.", 1), paragraf("Eşkenar üçgenin açıları eşittir.", 2)]
        self.assertEqual([h.alinti for h in tutarlilik.yazim_birligi(ps)], ["eş kenar"])


@unittest.skipUnless(os.path.exists(ORNEK_PDF), "ornek_kitap.pdf bulunamadı")
class UctanUca(unittest.TestCase):
    """Bilinçli hatalar içeren test PDF'inde üç kriterin de hatasını bulmalı."""

    def test_ornek_kitap(self):
        hatalar, ist = kitabi_denetle(ORNEK_PDF, sinif=4)
        kriterler = {h.kriter for h in hatalar}
        self.assertEqual(kriterler, {"Yazım", "Tutarlılık", "Yaş seviyesi"})
        self.assertIn("Herkez", [h.alinti for h in hatalar])
        for h in hatalar:
            self.assertIsNotNone(h.konum, "her bulgunun sayfadaki konumu olmalı")


if __name__ == "__main__":
    unittest.main()
