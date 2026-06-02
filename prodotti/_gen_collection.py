# -*- coding: utf-8 -*-
"""Genera la pagina collezione Umanoidi (umanoidi.html, livello root)."""
import os
from _gen_variants import LINEUP, COMPACT, V
from _prezzi import PREZZI, euro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root

NAMES = {
 "g1":"Unitree G1 Air","g1-u1":"Unitree G1 EDU Standard","g1-u2":"Unitree G1 EDU Plus",
 "g1-u3":"Unitree G1 EDU Ultimate A","g1-u4":"Unitree G1 EDU Ultimate B","g1-u5":"Unitree G1 EDU Ultimate C",
 "g1-u6":"Unitree G1 EDU Ultimate D","g1-u7":"Unitree G1 EDU Ultimate E","g1-u8":"Unitree G1 EDU Ultimate F",
 "g1-comp":"Unitree G1 Comp",
}
UNUM = {"g1":"Base","g1-comp":"Comp","g1-u1":"U1","g1-u2":"U2","g1-u3":"U3","g1-u4":"U4","g1-u5":"U5","g1-u6":"U6","g1-u7":"U7","g1-u8":"U8"}

def img(code):
    if code == "g1":
        return "prodotti/assets/images/g1-01.jpg"
    return f"prodotti/assets/variants/{code}/img-01.jpg"

def speed(code):
    return ">2 m/s" if code == "g1-comp" else "2 m/s"

def card(code):
    c = COMPACT[code]
    name = NAMES[code]
    href = f"prodotti/{c['file']}"
    pz = PREZZI.get(c['file'])
    price = euro(pz['cent']) if pz and pz['stato'] == 'acquista' else 'Su richiesta'
    return f'''        <article class="robot-card">
          <div class="robot-media">
            <span class="robot-media-tag">{UNUM[code]} · {c['tag']}</span>
            <img src="{img(code)}" alt="{name}, robot umanoide Unitree" loading="lazy"
                 onerror="this.parentElement.classList.add('no-img');">
            <div class="robot-media-placeholder">
              <strong>{name}</strong>
              <span>Umanoide · {c['dof']} DoF</span>
            </div>
          </div>
          <div class="robot-body">
            <div>
              <h3>{name}</h3>
              <p class="robot-subtitle">Robot umanoide · {c['hands']}</p>
            </div>

            <div class="key-specs">
              <div class="key-spec"><span class="key-spec-label">Gradi di libertà</span><span class="key-spec-value">{c['dof']}</span></div>
              <div class="key-spec"><span class="key-spec-label">Velocità max</span><span class="key-spec-value">{speed(code)}</span></div>
              <div class="key-spec"><span class="key-spec-label">Coppia ginocchio</span><span class="key-spec-value">{c['knee']}</span></div>
              <div class="key-spec"><span class="key-spec-label">Computing</span><span class="key-spec-value">{c['computing']}</span></div>
            </div>

            <ul class="spec-rows">
              <li><span>Mani</span><span>{c['hands']}</span></li>
              <li><span>Sensori tattili</span><span>{c['tactile']}</span></li>
              <li><span>Percezione</span><span>LiDAR 3D MID-360 · RealSense</span></li>
              <li><span>Garanzia</span><span>{c['warranty']}</span></li>
            </ul>

            <div class="robot-card-cta" style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
              <span style="font-size:1.05rem;font-weight:900;letter-spacing:-0.02em;">{price}</span>
              <a href="{href}" class="btn btn-primary btn-sm">Vedi scheda →</a>
            </div>
          </div>
        </article>'''

def matrix_row(code):
    c = COMPACT[code]
    return f'''            <tr>
              <td style="text-align:left;"><a href="prodotti/{c['file']}" style="color:var(--black);font-weight:700;text-decoration:none;">{NAMES[code]}</a></td>
              <td>{UNUM[code]}</td>
              <td>{c['dof']}</td>
              <td>{c['hands']}</td>
              <td>{c['tactile']}</td>
              <td>{c['computing']}</td>
              <td>{c['knee']}</td>
              <td>{c['warranty']}</td>
              <td style="padding:10px 14px;"><a href="prodotti/{c['file']}" class="btn btn-secondary btn-card">Apri</a></td>
            </tr>'''

cards = "\n\n".join(card(c) for c in LINEUP)
rows = "\n".join(matrix_row(c) for c in LINEUP)

# Estrai il CSS del componente robot-card (definito inline in manifattura-logistica.html)
_man = open(os.path.join(ROOT, "manifattura-logistica.html"), encoding="utf-8").read()
_a = _man.index("/* Robot/Product card grid */")
_b = _man.index("/* KPI box */")
CARD_CSS = _man[_a:_b].rstrip()

HTML = f'''<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Robot Umanoidi Unitree G1 — Tutta la gamma | Abra Robotics</title>
  <meta name="description" content="Tutti i modelli di robot umanoide Unitree G1 distribuiti in Italia da Abra Robotics: G1 Base, EDU Standard, EDU Plus, EDU Ultimate A-F e G1 Comp. Specifiche, confronto e schede tecniche.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://niccolomazzoleni-prog.github.io/Abra-Robotics/umanoidi.html">

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

    /* Full comparison matrix */
    .matrix-wrap {{ border:1px solid var(--gray-200); border-radius: var(--radius); overflow:auto; -webkit-overflow-scrolling:touch; }}
    .matrix {{ width:100%; border-collapse:collapse; min-width: 900px; }}
    .matrix thead td {{ background: var(--black); color:#fff; font-size:0.7rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; padding:14px 16px; text-align:center; }}
    .matrix thead td:first-child {{ text-align:left; }}
    .matrix tbody td {{ padding:14px 16px; font-family:var(--font); font-size:0.86rem; color:var(--gray-700); border-bottom:1px solid var(--gray-100); text-align:center; vertical-align:middle; }}
    .matrix tbody tr:hover td {{ background: rgba(0,0,0,0.025); }}
    .matrix tbody tr:last-child td {{ border-bottom:none; }}

    @media (max-width: 900px) {{ .robot-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>

  <!-- Top Bar -->
  <div class="top-bar">
    <p>Distributore ufficiale Unitree in Italia. <a href="assessment.html">Trova il modello giusto →</a></p>
  </div>

  <!-- Navbar -->
  <nav class="navbar">
    <div class="container navbar-inner">
      <a href="index.html" class="logo"><img src="images/logo.png" alt="Abra Robotics" class="logo-img"></a>
      <div class="nav-links">
        <div class="nav-item-dropdown">
          <button class="nav-dropdown-trigger" type="button">Prodotti <span class="nav-caret">▾</span></button>
          <div class="nav-dropdown-panel">
            <a href="manifattura-logistica.html#cobot">Cobot</a>
            <a href="manifattura-logistica.html#amr">AMR</a>
            <a href="manifattura-logistica.html#quadrupedi">Quadrupedi</a>
            <a href="umanoidi.html">Umanoidi</a>
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

  <!-- Mobile Menu -->
  <div class="mobile-menu">
    <div class="mobile-dropdown">
      <button class="mobile-dropdown-trigger" type="button">Prodotti <span class="nav-caret">▾</span></button>
      <div class="mobile-dropdown-panel">
        <a href="manifattura-logistica.html#cobot">Cobot</a>
        <a href="manifattura-logistica.html#amr">AMR</a>
        <a href="manifattura-logistica.html#quadrupedi">Quadrupedi</a>
        <a href="umanoidi.html">Umanoidi</a>
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

  <!-- HERO -->
  <section class="collection-hero">
    <div class="container">
      <p class="label">Robot Umanoidi</p>
      <h1>Unitree G1 — tutta la gamma</h1>
      <p class="lead">La famiglia di robot umanoidi Unitree G1, distribuita in Italia da Abra Robotics. Dal modello base alle configurazioni EDU per la ricerca, fino alla versione atletica Comp: dieci modelli, una sola piattaforma, una scheda tecnica dedicata per ciascuno.</p>
      <div class="hero-meta">
        <div><strong>10</strong><span>Modelli G1</span></div>
        <div><strong>23–42</strong><span>Gradi di libertà</span></div>
        <div><strong>100 TOPS</strong><span>Computing Jetson Orin NX</span></div>
        <div><strong>Italia</strong><span>Distributore ufficiale</span></div>
      </div>
    </div>
  </section>

  <!-- GRID -->
  <section class="section" style="padding-top:24px;">
    <div class="container">
      <div class="robot-grid">

{cards}

      </div>
    </div>
  </section>

  <!-- MATRICE COMPARATIVA -->
  <section class="section section-dark">
    <div class="container">
      <div class="section-header" style="text-align:left;max-width:100%;">
        <p class="label label-light">Confronto</p>
        <h2>Tutta la gamma G1 a confronto</h2>
        <p class="section-sub" style="margin-left:0;">Le differenze chiave tra i dieci modelli: gradi di libertà, mani, computing e garanzia. Scorri in orizzontale su mobile.</p>
      </div>
      <div class="matrix-wrap">
        <table class="matrix">
          <thead>
            <tr><td>Modello</td><td>Config</td><td>DoF</td><td>Mani</td><td>Tattile</td><td>Computing</td><td>Coppia</td><td>Garanzia</td><td></td></tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="section section-cta">
    <div class="container">
      <div class="cta-content">
        <h2>Non sai quale G1 scegliere?</h2>
        <p class="cta-subtitle">Raccontaci il tuo caso d'uso: ti aiutiamo a scegliere la configurazione giusta tra mani, computing e sensori. Risposta entro 12 ore.</p>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:8px;">
          <a href="assessment.html" class="btn btn-primary">Trova il robot giusto</a>
          <a href="index.html#cta-finale" class="btn btn-secondary">Prenota una chiamata</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
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
        <a href="manifattura-logistica.html#quadrupedi">Quadrupedi</a>
        <a href="umanoidi.html">Umanoidi</a>
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

out = os.path.join(ROOT, "umanoidi.html")
open(out, "w", encoding="utf-8").write(HTML)
print("written", out, len(HTML), "chars")
