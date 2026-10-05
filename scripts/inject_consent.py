#!/usr/bin/env python3
"""Consenso cookie su tutte le pagine con tracciamenti (idempotente).
- snippet Consent Mode v2 subito dopo <head> (prima di Tag Manager/gtag)
- consent.js (banner) in defer
- Meta Pixel: fbq('consent', ...) prima di fbq('init')
- via il pixel <noscript> (traccia senza poter chiedere il consenso)"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = "abra-consent-default"
SNIPPET = (
    "<script>/* " + MARK + ": Consent Mode v2, negato finche' l'utente non sceglie (consent.js) */\n"
    "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}\n"
    "(function(){var c=null;try{c=JSON.parse(localStorage.getItem('abra_consent')||'null');"
    "if(c&&(c.v!==1||Date.now()-c.ts>15552e6))c=null;}catch(e){}window.abraConsent=c;"
    "var g=function(v){return v?'granted':'denied';};"
    "gtag('consent','default',{ad_storage:g(c&&c.marketing),ad_user_data:g(c&&c.marketing),"
    "ad_personalization:g(c&&c.marketing),analytics_storage:g(c&&c.analytics),"
    "functionality_storage:'granted',security_storage:'granted',wait_for_update:500});"
    "gtag('set','ads_data_redaction',true);gtag('set','url_passthrough',true);})();</script>\n"
)
FB_INIT = re.compile(r"""fbq\((["'])init\1""")
FB_NOSCRIPT = re.compile(r'\s*<noscript>\s*<img[^>]*facebook\.com/tr\?[^>]*>\s*</noscript>', re.I)
TRACKERS = ("googletagmanager.com", "fbevents.js", "fbq(", "ads-tracking.js")

done = 0
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT)
    if rel.parts[0] in (".claude", "node_modules", "admin"):
        continue
    s = o = f.read_text(encoding="utf-8")
    if not any(t in s for t in TRACKERS):
        continue
    depth = len(rel.parts) - 1
    prefix = "../" * depth
    if MARK not in s:
        s = re.sub(r"(<head[^>]*>)", lambda m: m.group(1) + "\n" + SNIPPET + f'<script defer src="{prefix}consent.js"></script>', s, count=1)
    s = FB_NOSCRIPT.sub("", s)
    if "fbq(\"consent\"" not in s and "fbq('consent'" not in s:
        s = FB_INIT.sub(lambda m: 'fbq("consent",window.abraConsent&&window.abraConsent.marketing?"grant":"revoke");fbq(' + m.group(1) + "init" + m.group(1), s, count=1)
    if s != o:
        f.write_text(s, encoding="utf-8"); done += 1
print("pagine aggiornate:", done)
