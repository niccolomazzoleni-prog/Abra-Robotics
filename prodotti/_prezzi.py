# -*- coding: utf-8 -*-
"""Fonte unica prezzi end-user (EUR) + Payment Link Stripe per scheda prodotto.
Prezzi in centesimi. `link` vuoto = Payment Link da generare a Stripe-time
(riempire qui e rigenerare). `prov=True` = prezzo provvisorio non a listino,
da confermare prima del go-live."""

PREZZI = {
  # ── UMANOIDI G1 ──
  "unitree-g1.html":                 dict(cent=2399741, link="", stato="acquista"),                 # G1 Air
  "unitree-g1-edu-standard.html":    dict(cent=3756252, link="", stato="acquista"),                 # G1-U1
  "unitree-g1-edu-plus.html":        dict(cent=4578380, link="", stato="acquista"),                 # G1-U2
  "unitree-g1-edu-ultimate-a.html":  dict(cent=5048993, link="", stato="acquista"),                 # G1-U3
  "unitree-g1-edu-ultimate-b.html":  dict(cent=6222636, link="", stato="acquista"),                 # G1-U4
  "unitree-g1-edu-ultimate-c.html":  dict(cent=6222636, link="", stato="acquista"),                 # G1-U5
  "unitree-g1-edu-ultimate-d.html":  dict(cent=6770721, link="", stato="acquista"),                 # G1-U6
  "unitree-g1-edu-ultimate-e.html":  dict(cent=5674551, link="", stato="acquista"),                 # G1-U7
  "unitree-g1-edu-ultimate-f.html":  dict(cent=6222636, link="", stato="acquista", prov=True),       # U8: nessun match listino (provv. = tier tattile)
  "unitree-g1-comp.html":            dict(cent=4167316, link="", stato="acquista"),                 # G1-COMP
  # ── QUADRUPEDI ──
  "unitree-go2-pro.html":            dict(cent=404376,  link="", stato="acquista"),                 # GO2 PRO PACKAGE
  "unitree-go2-edu.html":            dict(cent=1279948, link="", stato="acquista"),                 # GO2 EDU STANDARD
  "unitree-go2-edu-plus.html":       dict(cent=1545006, link="", stato="acquista"),                 # GO2 EDU SMART
  "unitree-go2-enterprise-u2.html":  dict(cent=2007500, link="", stato="acquista", prov=True),       # non a listino (provv. = tier Ultimate)
  "unitree-a2.html":                 dict(cent=3064848, link="", stato="acquista"),                 # A2 STANDARD
  "unitree-a2-pro.html":             dict(cent=4167316, link="", stato="acquista"),                 # A2 PRO
  "unitree-b2.html":                 dict(cent=7795423, link="", stato="acquista"),                 # B2+LIDAR
  "unitree-r1-edu.html":             dict(cent=3228720, link="", stato="acquista"),                 # R1 / R1-U3
  "unitree-h2.html":                 dict(cent=0,       link="", stato="preventivo"),               # H2 — prezzo EUR mancante a listino (da fornire)
}

def euro(cent):
    """2399741 -> '23.997,41 €' (formato IT)."""
    s = f"{cent/100:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")
    return s + " €"

def schema_price(cent):
    """2399741 -> '23997.41' (per JSON-LD)."""
    return f"{cent/100:.2f}"
