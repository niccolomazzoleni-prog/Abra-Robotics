# SEO actions — Abra Robotics (audit 24 Jul 2026)

Sources: SE Ranking audit PDF + keyword positions XLSX (`abrarobotics_com_positions_detailed_2026-07-24.xlsx`).

## Repo / access

- GitHub: `niccolomazzoleni-prog/Abra-Robotics`
- Collaborator with push: **VenetoStato**
- Branch: `seo/audit-jul-2026`

## Keyword → page target

| Keyword | Vol. | Pagina target |
|---|---:|---|
| robot umanoide | 5700 | `/umanoidi.html` |
| Unitree G1 | 1000 | `/prodotti/unitree-g1.html` (+ hub umanoidi) |
| humanoid robot | 540 | `/en/umanoidi-en.html` |
| Unitree Go2 | 320 | `/quadrupedi.html` + schede Go2 |
| robot collaborativo | 320 | `/catalogo-cobot.html`, `/manifattura-logistica.html` |
| industrial robotics | 210 | `/manifattura-logistica.html` |
| robot quadrupede | 70 | `/quadrupedi.html` |

## Technical fixes shipped

1. **Legacy 4XX EN paths**: stub redirect `prodotti/*-en.html` → `en/prodotti/*-en.html` (noindex + refresh + canonical).
2. **Dead stubs**: `g1.html`, `h2.html`, `r1.html`, `software-en.html`, `en/index.html` → destinazioni corrette.
3. **Sitemap**: rigenerata (335 URL); esclusi fonts, LC ads, thank-you, offerte-ai, redirect stubs.
4. **Hreflang**: riparati target 404 / return link IT↔EN su pagine pubbliche.
5. **On-page**: title unici IT/EN, title ≤60, description ≤160, multi-H1 collassati.
6. **Assets**: path JS/CSS/immagini `en/prodotti` → `../../prodotti/...` (0 JS 4XX locali rimanenti sulle pagine reali).
7. **Pillar content**: H1/title/desc + FAQ + FAQPage schema su umanoidi, quadrupedi, G1, catalogo cobot.

## Scripts

- `scripts/seo_audit_fix.py` — audit/fix crawl + on-page
- `scripts/seo_keyword_pillars.py` — keyword pillars
- `scripts/genera_sitemap.py` — sitemap (aggiornato exclude list)

## Post-deploy checklist

- [ ] Push + merge branch; attendere GitHub Pages
- [ ] Google Search Console: proprietà `abrarobotics.com` (oggi GSC “No data” nel report posizioni)
- [ ] Inviare sitemap aggiornata in GSC
- [ ] Richiedere re-crawl SE Ranking
- [ ] Monitorare posizioni su: robot umanoide, Unitree G1, Unitree Go2, robot collaborativo

## Note

- Backlinks / Domain Trust restano fuori scope codice (audit: ~1 referring domain).
- Minify CSS/JS globale lasciato fuori (basso ROI vs indexing).
