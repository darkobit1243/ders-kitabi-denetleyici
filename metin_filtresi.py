"""Denetlenecek paragrafları seçer.

Matematik formülleri ve tablolar PDF'ten "2 1 2 1 $ $ = c m" gibi anlamsız
parçalar hâlinde çıkıyor. Bunlar denetime girerse yüzlerce sahte hata bulunur.
Bu yüzden yalnızca gerçek cümle gibi görünen paragrafları denetliyoruz.
"""

import re

KELIME_DESENI = re.compile(r"[^\W\d_]+")   # yalnızca harflerden oluşan parçalar

EN_AZ_KELIME = 4        # bundan az gerçek kelime varsa paragraf denetlenmez
EN_AZ_KELIME_ORANI = 0.7  # parçaların en az %70'i gerçek kelime olmalı


def incelenebilir_mi(metin: str) -> bool:
    parcalar = metin.split()
    if not parcalar:
        return False
    # 2 harften kısa parçalar (a, n, x gibi değişkenler) kelime sayılmaz
    kelimeler = [k for k in KELIME_DESENI.findall(metin) if len(k) >= 2]
    if len(kelimeler) < EN_AZ_KELIME:
        return False
    return len(kelimeler) / len(parcalar) >= EN_AZ_KELIME_ORANI
