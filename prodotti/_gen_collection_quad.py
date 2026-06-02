# -*- coding: utf-8 -*-
"""Genera quadrupedi.html (collezione, livello root)."""
import os
from _gen_quadrupeds import LINEUP, COMPACT
from _prezzi import PREZZI, euro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = {
 "go2-pro":"Unitree Go2 Pro","go2-edu":"Unitree Go2 EDU","go2-edu-plus":"Unitree Go2 EDU+",
 "go2-ent-u2":"Unitree Go2 Enterprise+ U2","a2":"Unitree A2","a2-pro":"Unitree A2 Pro","b2":"Unitree B2",
}
IMG = {
 "go2-pro":"go2-pro/img-01.jpg","go2-edu":"go2-edu/img-01.jpg","go2-edu-plus":"go2-edu/img-02.jpg",
 "go2-ent-u2":"go2-ent-u2/img-01.jpg","a2":"a2/img-01.jpg","a2-pro":"a2-pro/img-01.jpg","b2":"b2/img-01.jpg",
}
CLIMB = {"go2-pro":"40°","go2-edu":"40°","go2-edu-plus":"40°","go2-ent-u2":"40°","a2":"45°","a2-pro":"45°","b2":">45°"}
RUN = {"go2-pro":"1–2 h","go2-edu":"2–4 h","go2-edu-plus":"2–4 h","go2-ent-u2":"1–2 h","a2":">5 h","a2-pro":">5 h","b2":"4–6 h"}

def card(code):
    c = COMPACT[code]; name = NAMES[code]
    pz = PREZZI.get(c['file'])
    price = euro(pz['cent']) if pz and pz['stato'] == 'acquista' else 'Su richiesta'
    return f'''        <article class="robot-card">
          <div class="robot-media">
            <span class="robot-media-tag">{c['tag']}</span>
            <img src="prodotti/assets/variants/{IMG[code]}" alt="{name}, quadrupede Unitree" loading="lazy"
                 onerror="this.parentElement.classList.add('no-img');">
            <div class="robot-media-placeholder">
              <strong>{name}</strong>
              <span>Quadrupede · {c['payload']} carico</span>
            </div>
          </div>
          <div class="robot-body">
            <div>
              <h3>{name}</h3>
              <p class="robot-subtitle">Quadrupede · {c['tag']}</p>
            </div>
            <div class="key-specs">
              <div class="key-spec"><span class="key-spec-label">Carico utile</span><span class="key-spec-value">{c['payload']}</span></div>
              <div class="key-spec"><span class="key-spec-label">Velocità max</span><span class="key-spec-value">{c['speed']}</span></div>
              <div class="key-spec"><span class="key-spec-label">Pendenza max</span><span class="key-spec-value">{CLIMB[code]}</span></div>
              <div class="key-spec"><span class="key-spec-label">Computing</span><span class="key-spec-value">{c['computing']}</span></div>
            </div>
            <ul class="spec-rows">
              <li><span>LiDAR</span><span>{c['lidar']}</span></li>
              <li><span>Protezione</span><span>{c['ip']}</span></li>
              <li><span>Autonomia</span><span>{RUN[code]}</span></li>
              <li><span>Garanzia</span><span>{c['warranty']}</span></li>
            </ul>
            <div class="robot-card-cta" style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
              <span style="font-size:1.05rem;font-weight:900;letter-spacing:-0.02em;">{price}</span>
              <a href="prodotti/{c['file']}" class="btn btn-primary btn-sm">Vedi scheda →</a>
            </div>
          </div>
        </article>'''

def row(code):
    c = COMPACT[code]
    return f'''            <tr>
              <td style="text-align:left;"><a href="prodotti/{c['file']}" style="color:var(--black);font-weight:700;text-decoration:none;">{NAMES[code]}</a></td>
              <td>{c['payload']}</td>
              <td>{c['speed']}</td>
              <td>{c['computing']}</td>
              <td>{c['lidar']}</td>
              <td>{c['ip']}</td>
              <td>{c['warranty']}</td>
              <td style="padding:10px 14px;"><a href="prodotti/{c['file']}" class="btn btn-secondary btn-card">Apri</a></td>
            </tr>'''

cards = "\n\n".join(card(c) for c in LINEUP)
rows = "\n".join(row(c) for c in LINEUP)

_man = open(os.path.join(ROOT, "manifattura-logistica.html"), encoding="utf-8").read()
CARD_CSS = _man[_man.index("/* Robot/Product card grid */"):_man.index("/* KPI box */")].rstrip()

HTML = f'''<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Robot Quadrupedi Unitree — Tutta la gamma | Abra Robotics</title>
  <meta name="description" content="Tutti i robot quadrupedi Unitree distribuiti in Italia da Abra Robotics: Go2 Pro, Go2 EDU, Go2 EDU+, Go2 Enterprise+ U2, A2, A2 Pro e B2. Specifiche, confronto e schede tecniche.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://niccolomazzoleni-prog.github.io/Abra-Robotics/quadrupedi.html">
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <style>
    /* ── Componente robot-card (estratto da manifattura-logistica) ── */
{CARD_CSS}

    /* ── Pagina collezione ── */
    .collection-hero {{ padding: calc(40px + 72px + 64px) 0 56px; background: var(--white); }}
    .collection-hero .label {{ margin-bottom: 16px; }}
    .collection-hero h1 {{ font-size: clamp(2.2rem, 5vw, 3.6rem); font-weight: 900; letter-spacing: -0.04em; line-height: 1.05; margin-bottom: 20px; }}
    .collection-hero p.lead {{ font-size: 1.15rem; color: var(--gray-600); line-height: 1.7; max-width: 760px; }}
    .collection-hero .hero-meta {{ display:flex; gap:28px; flex-wrap:wrap; margin-top:28px; }}
    .collection-hero .hero-meta div {{ display:flex; flex-direction:column; }}
    .collection-hero .hero-meta strong {{ font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; }}
    .collection-hero .hero-meta span {{ font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; color:var(--gray-400); font-weight:600; }}
    .matrix-wrap {{ border:1px solid var(--gray-200); border-radius: var(--radius); overflow:auto; -webkit-overflow-scrolling:touch; }}
    .matrix {{ width:100%; border-collapse:collapse; min-width: 880px; }}
    .matrix thead td {{ background: var(--black); color:#fff; font-size:0.7rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; padding:14px 16px; text-align:center; }}
    .matrix thead td:first-child {{ text-align:left; }}
    .matrix tbody td {{ padding:14px 16px; font-family:var(--font); font-size:0.86rem; color:var(--gray-700); border-bottom:1px solid var(--gray-100); text-align:center; vertical-align:middle; }}
    .matrix tbody tr:hover td {{ background: rgba(0,0,0,0.025); }}
    .matrix tbody tr:last-child td {{ border-bottom:none; }}
    @media (max-width: 900px) {{ .robot-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>

  <div class="top-bar">
    <p>Distributore ufficiale Unitree in Italia. <a href="assessment.html">Trova il modello giusto →</a></p>
  </div>

  <nav class="navbar">
    <div class="container navbar-inner">
      <a href="index.html" class="logo"><img src="images/logo.png" alt="Abra Robotics" class="logo-img"></a>
      <div class="nav-links">
        <div class="nav-item-dropdown">
          <button class="nav-dropdown-trigger" type="button">Prodotti <span class="nav-caret">▾</span></button>
          <div class="nav-dropdown-panel">
            <a href="manifattura-logistica.html#cobot">Cobot</a>
            <a href="manifattura-logistica.html#amr">AMR</a>
            <a href="quadrupedi.html">Quadrupedi</a>
            <a href="umanoidi.html">Umanoidi</a>
            <a href="accessori.html">Accessori</a>
          </div>
        </div>
        <a href="assessment.html">Trova il robot giusto</a>
        <a href="finanziamenti.html">Finanziamenti</a>
        <div class="nav-item-dropdown">
          <button class="nav-dropdown-trigger" type="button">Per chi <span class="nav-caret">▾</span></button>
          <div class="nav-dropdown-panel">
            <a href="manifattura-logistica.html">Manifattura e Logistica</a>
            <a href="universita-ricerca.html">Università e Ricerca</a>
          </div>
        </div>
        <a href="index.html#chi-siamo">Chi siamo</a>
      </div>
      <a href="index.html#cta-finale" class="btn btn-primary btn-sm">Prenota una chiamata</a>
      <button class="menu-toggle" aria-label="Menu"><span></span><span></span></button>
    </div>
  </nav>

  <div class="mobile-menu">
    <div class="mobile-dropdown">
      <button class="mobile-dropdown-trigger" type="button">Prodotti <span class="nav-caret">▾</span></button>
      <div class="mobile-dropdown-panel">
        <a href="manifattura-logistica.html#cobot">Cobot</a>
        <a href="manifattura-logistica.html#amr">AMR</a>
        <a href="quadrupedi.html">Quadrupedi</a>
        <a href="umanoidi.html">Umanoidi</a>
        <a href="accessori.html">Accessori</a>
      </div>
    </div>
    <a href="assessment.html">Trova il robot giusto</a>
    <a href="finanziamenti.html">Finanziamenti</a>
    <div class="mobile-dropdown">
      <button class="mobile-dropdown-trigger" type="button">Per chi <span class="nav-caret">▾</span></button>
      <div class="mobile-dropdown-panel">
        <a href="manifattura-logistica.html">Manifattura e Logistica</a>
        <a href="universita-ricerca.html">Università e Ricerca</a>
      </div>
    </div>
    <a href="index.html#chi-siamo">Chi siamo</a>
    <a href="index.html#cta-finale" class="btn btn-primary">Prenota una chiamata</a>
  </div>

  <section class="collection-hero">
    <div class="container">
      <p class="label">Robot Quadrupedi</p>
      <h1>Quadrupedi Unitree — tutta la gamma</h1>
      <p class="lead">Dal Go2 agile per education e ispezione leggera fino al B2 industriale pesante IP67: la gamma completa di robot quadrupedi Unitree, distribuita in Italia da Abra Robotics. Una scheda tecnica dedicata per ciascun modello.</p>
      <div class="hero-meta">
        <div><strong>7</strong><span>Modelli</span></div>
        <div><strong>10–120 kg</strong><span>Carico utile</span></div>
        <div><strong>IP67</strong><span>Fino a (A2 Pro / B2)</span></div>
        <div><strong>Italia</strong><span>Distributore ufficiale</span></div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:24px;">
    <div class="container">
      <div class="robot-grid">

{cards}

      </div>
    </div>
  </section>

  <section class="section section-dark">
    <div class="container">
      <div class="section-header" style="text-align:left;max-width:100%;">
        <p class="label label-light">Confronto</p>
        <h2>Tutta la gamma quadrupedi a confronto</h2>
        <p class="section-sub" style="margin-left:0;">Carico, velocità, computing, LiDAR e protezione dei sette modelli. Scorri in orizzontale su mobile.</p>
      </div>
      <div class="matrix-wrap">
        <table class="matrix">
          <thead>
            <tr><td>Modello</td><td>Carico</td><td>Velocità</td><td>Computing</td><td>LiDAR</td><td>IP</td><td>Garanzia</td><td></td></tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="section section-cta">
    <div class="container">
      <div class="cta-content">
        <h2>Non sai quale quadrupede scegliere?</h2>
        <p class="cta-subtitle">Dalla didattica all'ispezione industriale: raccontaci il tuo caso d'uso e ti aiutiamo a scegliere il modello giusto. Risposta entro 12 ore.</p>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:8px;">
          <a href="assessment.html" class="btn btn-primary">Trova il robot giusto</a>
          <a href="index.html#cta-finale" class="btn btn-secondary">Prenota una chiamata</a>
        </div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="logo"><img src="images/logo.png" alt="Abra Robotics" class="logo-img"></a>
        <p class="footer-desc">Robotica applicata per aziende, università e istituti di ricerca. Hardware, software su misura, formazione e supporto tecnico dedicato.</p>
      </div>
      <div class="footer-nav">
        <span class="footer-heading">Navigazione</span>
        <a href="manifattura-logistica.html">Manifattura e Logistica</a>
        <a href="universita-ricerca.html">Università e Ricerca</a>
        <a href="assessment.html">Trova il robot giusto</a>
        <a href="finanziamenti.html">Finanziamenti</a>
      </div>
      <div class="footer-nav">
        <span class="footer-heading">Prodotti</span>
        <a href="manifattura-logistica.html#cobot">Cobot</a>
        <a href="manifattura-logistica.html#amr">AMR</a>
        <a href="quadrupedi.html">Quadrupedi</a>
        <a href="umanoidi.html">Umanoidi</a>
        <a href="accessori.html">Accessori</a>
      </div>
      <div class="footer-contact">
        <span class="footer-heading">Contatti</span>
        <a href="mailto:info@abrarobotics.com">info@abrarobotics.com</a>
        <p>Italia</p>
        <a href="index.html#cta-finale" class="btn btn-primary btn-sm">Prenota una chiamata</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <p class="footer-copy">&copy; 2026 Abra Robotics. Tutti i diritti riservati.</p>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>
'''
open(os.path.join(ROOT, "quadrupedi.html"), "w", encoding="utf-8").write(HTML)
print("written quadrupedi.html", len(HTML), "chars")
