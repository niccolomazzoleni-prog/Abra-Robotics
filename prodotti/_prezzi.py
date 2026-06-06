# -*- coding: utf-8 -*-
"""Fonte unica prezzi end-user (EUR) + Payment Link Stripe per scheda prodotto.
Prezzi in centesimi. `link` vuoto = Payment Link da generare a Stripe-time
(riempire qui e rigenerare). `prov=True` = prezzo provvisorio non a listino,
da confermare prima del go-live."""

PREZZI = {
  "unitree-a2-pro.html":             dict(cent=3958950, link="", stato="acquista"),# 39.589,50 €
  "unitree-a2.html":                 dict(cent=2911606, link="", stato="acquista"),# 29.116,06 €
  "unitree-b2.html":                 dict(cent=7405652, link="", stato="acquista"),# 74.056,52 €
  "unitree-g1-comp.html":            dict(cent=3958950, link="", stato="acquista"),# 39.589,50 €
  "unitree-g1-edu-plus.html":        dict(cent=4349461, link="", stato="acquista"),# 43.494,61 €
  "unitree-g1-edu-standard.html":    dict(cent=3568439, link="", stato="acquista"),# 35.684,39 €
  "unitree-g1-edu-ultimate-a.html":  dict(cent=4796543, link="", stato="acquista"),# 47.965,43 €
  "unitree-g1-edu-ultimate-b.html":  dict(cent=5911504, link="", stato="acquista"),# 59.115,04 €
  "unitree-g1-edu-ultimate-c.html":  dict(cent=5911504, link="", stato="acquista"),# 59.115,04 €
  "unitree-g1-edu-ultimate-d.html":  dict(cent=6432185, link="", stato="acquista"),# 64.321,85 €
  "unitree-g1-edu-ultimate-e.html":  dict(cent=5390823, link="", stato="acquista"),# 53.908,23 €
  "unitree-g1-edu-ultimate-f.html":  dict(cent=0, link="", stato="preventivo"),# (vuoto)
  "unitree-g1.html":                 dict(cent=2279754, link="", stato="acquista"),# 22.797,54 €
  "unitree-go2-edu-plus.html":       dict(cent=1467756, link="", stato="acquista"),# 14.677,56 €
  "unitree-go2-edu.html":            dict(cent=1215951, link="", stato="acquista"),# 12.159,51 €
  "unitree-go2-enterprise-u2.html":  dict(cent=0, link="", stato="preventivo"),# (vuoto)
  "unitree-go2-pro.html":            dict(cent=384157, link="", stato="acquista"),# 3.841,57 €
  "unitree-h2.html":                 dict(cent=0, link="", stato="preventivo"),# Prezzo su richiesta
  "unitree-r1-edu.html":             dict(cent=3067284, link="", stato="acquista"),# 30.672,84 €
}

def euro(cent):
    """2399741 -> '23.997,41 €' (formato IT)."""
    s = f"{cent/100:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")
    return s + " €"

def schema_price(cent):
    """2399741 -> '23997.41' (per JSON-LD)."""
    return f"{cent/100:.2f}"
