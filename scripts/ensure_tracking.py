# -*- coding: utf-8 -*-
"""Garantisce Consent Mode v2 + GTM + GA4 (G-T4ZC7CM8RX) nel <head> di ogni pagina pubblica.

Usa lo stesso schema della home: consent default inline per primo, poi i comandi
in dataLayer subito e gli script esterni (gtm.js, gtag.js) solo dopo il load
(idle) o alla prima interazione. Idempotente: tocca solo le pagine senza tag.
Lanciato anche dal workflow regenerate-site. Uso: python scripts/ensure_tracking.py
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GA4_ID = "G-T4ZC7CM8RX"
SKIP = re.compile(r"backup|preview|zenixa|^scripts/")

CONSENT = """<script>/* abra-consent-default: Consent Mode v2, negato finche' l'utente non sceglie (consent.js) */
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
(function(){var c=null;try{c=JSON.parse(localStorage.getItem('abra_consent')||'null');if(c&&(c.v!==1||Date.now()-c.ts>15552e6))c=null;}catch(e){}window.abraConsent=c;var g=function(v){return v?'granted':'denied';};gtag('consent','default',{ad_storage:g(c&&c.marketing),ad_user_data:g(c&&c.marketing),ad_personalization:g(c&&c.marketing),analytics_storage:g(c&&c.analytics),functionality_storage:'granted',security_storage:'granted',wait_for_update:500});gtag('set','ads_data_redaction',true);gtag('set','url_passthrough',true);})();</script>
<script defer src="{prefix}consent.js"></script>"""

LOADER = """<!-- Google Tag Manager + Google tag (gtag.js): i comandi entrano subito in dataLayer, DOPO il consent default qui sopra;
     gli script esterni (~350 KB) si scaricano solo dopo il load (idle) o alla prima interazione, per non rubare banda a CSS/font/hero su mobile. -->
<script>(function(w,d){w.dataLayer=w.dataLayer||[];w.dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});
  gtag('js',new Date());gtag('config','G-T4ZC7CM8RX');
  var ev=['pointerdown','keydown','touchstart','scroll'],done=0;
  function load(){if(done)return;done=1;ev.forEach(function(e){w.removeEventListener(e,load,true);});
    ['https://www.googletagmanager.com/gtm.js?id=GTM-MNLWZSN7','https://www.googletagmanager.com/gtag/js?id=G-T4ZC7CM8RX'].forEach(function(u){var j=d.createElement('script');j.async=true;j.src=u;d.head.appendChild(j);});}
  ev.forEach(function(e){w.addEventListener(e,load,{capture:true,passive:true});});
  function idle(){w.requestIdleCallback?requestIdleCallback(load,{timeout:3000}):setTimeout(load,1500);}
  if(d.readyState==='complete')idle();else w.addEventListener('load',idle);
})(window,document);</script>
<!-- End Google Tag Manager -->"""


def patch(rel: str, html: str) -> str | None:
    if GA4_ID in html:
        return None
    head = re.search(r"<head[^>]*>", html, re.I)
    if not head:
        return None
    if "abra-consent-default" not in html:
        prefix = "../" * rel.count("/")
        charset = re.compile(r"\s*<meta charset=[^>]*>", re.I).match(html, head.end())
        at = charset.end() if charset else head.end()
        html = html[:at] + "\n" + CONSENT.replace("{prefix}", prefix) + html[at:]
    # il loader va subito dopo il consent default (e dopo consent.js se c'e')
    start = html.index("abra-consent-default")
    end = html.index("</script>", start) + len("</script>")
    cjs = re.compile(r"\s*<script defer src=\"[^\"]*consent\.js\"></script>").match(html, end)
    at = cjs.end() if cjs else end
    return html[:at] + "\n" + LOADER + html[at:]


def main() -> None:
    files = subprocess.check_output(["git", "ls-files", "*.html"], cwd=ROOT, text=True).split()
    fixed = []
    for rel in files:
        if SKIP.search(rel):
            continue
        path = ROOT / rel
        new = patch(rel, path.read_text(encoding="utf-8"))
        if new:
            path.write_text(new, encoding="utf-8")
            fixed.append(rel)
    print(f"tracking aggiunto a {len(fixed)} pagine")
    for rel in fixed:
        print(" ", rel)


if __name__ == "__main__":
    main()
