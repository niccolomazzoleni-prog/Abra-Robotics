# -*- coding: utf-8 -*-
"""Genera accessori.html (catalogo accessori Unitree).
Immagini: solo file ufficiali dei produttori in images/official/ (vedi
data/immagini-ufficiali.json e scripts/immagini_ufficiali.py); nessun download
da rivenditori terzi. Prezzi tenuti in commento HTML (convenzione sito)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from site_nav import render_site_nav

SITE_NAV_HTML = render_site_nav("")
IMGDIR = os.path.join(ROOT, "images")

# (slug, nome, descrizione, spec, prezzo_usd, immagine relativa a images/)
ACC = {
 "Mani e gripper": [
  ("dex3-1","Unitree Dex3-1","Mano robotica a 3 dita leggera per manipolazione di precisione e ricerca.","7 DoF · 710 g · opz. 33 sensori tattili","$6.500","official/unitree-dex3-1.webp"),
  ("dex5-1","Unitree Dex5-1","Mano dexterous high-end per manipolazione avanzata su umanoidi.","Mano singola · high-end","$25.000","official/unitree-dex5-1.webp"),
  ("inspire-rh56","Inspire RH56DFQ","Mano a 5 dita antropomorfa con sensori di pressione, compatibile ROS.","6 DoF · 540 g · carico 3 kg","$9.500","official/inspire-rh56dfx.webp"),
  ("dex1-1-v1","Unitree Dex1-1 V1","Pinza standard per umanoidi G1.","Gripper standard","$380","official/unitree-dex1-1.webp"),
  ("dex1-1-v2","Unitree Dex1-1 V2","Gripper avanzato con camera RGB integrata per grasping vision-guided.","Gripper + camera RGB","$580","official/unitree-dex1-1-b.webp"),
 ],
 "Batterie e alimentazione": [
  ("batt-go2","Batteria Go2","Batteria di ricambio per quadrupede Go2 (EDU e Pro).","8.000 / 15.000 mAh","$560","official/unitree-go2-batteria-long.webp"),
  ("batt-b2","Batteria B2 alta capacità","Batteria ad alta capacità per quadrupede industriale B2.","45 Ah · 2250 Wh","$4.200","official/placeholder-prodotto.webp"),
  ("batt-g1","Batteria G1","Batteria di ricambio ad alte prestazioni per umanoide G1.","High-performance","$800","official/unitree-g1-info-batteria.webp"),
  ("batt-go1","Batteria Go1","Batteria di ricambio per quadrupede Go1.","6.000 mAh","$499","official/unitree-go1-batteria.webp"),
  ("go2-charging","Go2 Self-Charging Board","Base di ricarica wireless ad alta efficienza per Go2 EDU+.","Ricarica wireless","$1.050","official/placeholder-prodotto.webp"),
 ],
 "Sensori LiDAR e camere": [
  ("livox-mid360","Livox MID-360 LiDAR","LiDAR 3D a 360° per mapping e navigazione autonoma.","3D · 360°","$4.275","official/livox-mid360.webp"),
  ("hesai-xt16","Hesai XT16 3D LiDAR","LiDAR 3D a 16 canali per perception ad alta risoluzione.","16 canali · 3D","$6.650","official/hesai-xt16.webp"),
 ],
 "Controllo e sviluppo": [
  ("rc-g1","Telecomando G1","Telecomando per umanoide G1.","Remote controller","$450","official/unitree-telecomando.webp"),
  ("rc-go2","Telecomando Go2","Telecomando per quadrupede Go2.","Remote controller","$375","official/unitree-go2-controller.webp"),
  ("g1-teleop","G1 Teleoperation Kit","Kit teleoperazione full-body in VR con visore PICO 4 Ultra.","Full-body VR · PICO 4 Ultra","$6.000","accessori/g1-teleop.webp"),
  ("g1-gantry","G1 Gantry","Telaio di supporto per sviluppo e test sicuri dell'umanoide G1.","Gantry sviluppo","$960","official/placeholder-prodotto.webp"),
  ("jetson-thor","Jetson AGX Thor Backplate","Modulo di espansione compute NVIDIA Jetson AGX Thor per G1.","AI onboard · backplate","$15.200","accessori/jetson-thor.jpg"),
 ],
 "Bracci robotici": [
  ("z1","Unitree Z1","Braccio robotico 6-DoF di precisione con force control.","6 DoF · force control","$11.900","official/unitree-z1-01.webp"),
  ("d1","Go2 Servo Arm D1","Braccio servo D1 montabile su Go2 per manipolazione mobile.","Servo arm","$4.655","official/unitree-d1-braccio.webp"),
  ("d1-t","D1-T Teleop Kit","Kit doppio braccio servo D1-T per teleoperazione leader-follower.","Doppio braccio · teleop","$12.000","official/unitree-d1-t-kit.webp"),
  ("z1-gripper","Z1 Gripper","Pinza end-effector per braccio Z1.","End-effector","$2.150","official/unitree-z1-pinza.webp"),
  ("z1-d435i","Z1 Gripper + D435i","Pinza Z1 con camera depth Intel RealSense D435i integrata.","+ depth D435i","$3.390","official/unitree-z1-pinza.webp"),
  ("z1-d405","Z1 Gripper + D405","Pinza Z1 con camera depth Intel RealSense D405 integrata.","+ depth D405","$3.390","official/unitree-z1-pinza.webp"),
  ("z1-motor","Z1 Arm Motor","Attuatore/motore di ricambio per giunto del braccio Z1.","Ricambio giunto","$390","official/unitree-z1-motore.webp"),
 ],
}

def fetch(rel, slug):
    """Restituisce il percorso (relativo a images/) se il file ufficiale esiste."""
    if os.path.exists(os.path.join(IMGDIR, rel)):
        return rel
    print("  MANCA", slug, rel, "(esegui scripts/immagini_ufficiali.py)")
    return None

def card(item):
    slug, name, desc, spec, price, fn = item
    rel = fetch(fn, slug)
    img = f'<img src="images/{rel}" alt="{name}" loading="lazy" onerror="this.style.display=\'none\';this.parentElement.classList.add(\'no-img\');">' if rel else '<div class="acc-noimg">Unitree</div>'
    return f'''        <article class="acc-card">
          <div class="acc-media">{img}</div>
          <div class="acc-body">
            <h3>{name}</h3>
            <p class="acc-desc">{desc}</p>
            <span class="acc-spec">{spec}</span>
          </div>
        </article>'''

sections = []
total = 0
for cat, items in ACC.items():
    total += len(items)
    cards = "\n".join(card(it) for it in items)
    sections.append(f'''      <div class="acc-group">
        <h2 class="acc-group-title">{cat}</h2>
        <div class="acc-grid">
{cards}
        </div>
      </div>''')
SECTIONS = "\n\n".join(sections)

HTML = f'''<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Accessori Unitree — Mani, batterie, LiDAR e bracci | Abra Robotics</title>
  <meta name="description" content="Catalogo accessori Unitree disponibili in Italia tramite Abra Robotics: mani dexterous Dex3/Dex5/Inspire, batterie, LiDAR Livox e Hesai, telecomandi, bracci Z1 e D1, moduli di calcolo.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://abrarobotics.com/accessori.html">
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <style>
    .collection-hero {{ padding: calc(40px + 72px + 64px) 0 48px; background: var(--white); }}
    .collection-hero .label {{ margin-bottom: 16px; }}
    .collection-hero h1 {{ font-size: clamp(2.2rem, 5vw, 3.6rem); font-weight: 900; letter-spacing: -0.04em; line-height: 1.05; margin-bottom: 20px; }}
    .collection-hero p.lead {{ font-size: 1.15rem; color: var(--gray-600); line-height: 1.7; max-width: 740px; }}
    .acc-group {{ margin-bottom: 56px; }}
    .acc-group-title {{ font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 24px; padding-bottom: 14px; border-bottom: 1px solid var(--gray-200); }}
    .acc-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 20px; }}
    .acc-card {{ background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; transition: transform .4s cubic-bezier(0.34,1.56,0.64,1), box-shadow .3s ease, border-color .3s ease; }}
    .acc-card:hover {{ transform: translateY(-4px); box-shadow: 0 16px 40px rgba(0,0,0,0.08); border-color: rgba(0,0,0,0.15); }}
    .acc-media {{ aspect-ratio: 1/1; background: linear-gradient(135deg, var(--gray-50), var(--gray-100)); display: flex; align-items: center; justify-content: center; overflow: hidden; border-bottom: 1px solid var(--gray-200); }}
    .acc-media img {{ width: 100%; height: 100%; object-fit: contain; padding: 18px; }}
    .acc-media.no-img {{ font-weight: 800; color: var(--gray-400); }}
    .acc-noimg {{ font-weight: 800; color: var(--gray-400); }}
    .acc-body {{ padding: 18px 18px 20px; display: flex; flex-direction: column; gap: 8px; flex: 1; }}
    .acc-body h3 {{ font-size: 1rem; font-weight: 700; letter-spacing: -0.01em; }}
    .acc-desc {{ font-size: 0.85rem; color: var(--gray-600); line-height: 1.5; flex: 1; }}
    .acc-spec {{ font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gray-400); }}
    @media (max-width: 1024px) {{ .acc-grid {{ grid-template-columns: repeat(3,1fr); }} }}
    @media (max-width: 768px) {{ .acc-grid {{ grid-template-columns: repeat(2,1fr); }} }}
  </style>
</head>
<body>

  <div class="top-bar">
    <p>Parte della filiera di distribuzione di Unitree Italia. <a href="assessment.html">Trova il robot giusto →</a></p>
  </div>

{SITE_NAV_HTML}

  <section class="collection-hero">
    <div class="container">
      <p class="label">Accessori Unitree</p>
      <h1>Accessori e moduli Unitree</h1>
      <p class="lead">Mani dexterous, batterie, sensori LiDAR, telecomandi, bracci robotici e moduli di calcolo per estendere i robot Unitree. Tutti gli accessori sono disponibili tramite Abra Robotics, parte della filiera di distribuzione di Unitree Italia.</p>
    </div>
  </section>

  <section class="section" style="padding-top:24px;">
    <div class="container">
{SECTIONS}
    </div>
  </section>

  <section class="section section-cta">
    <div class="container">
      <div class="cta-content">
        <h2>Cerchi un accessorio o un ricambio?</h2>
        <p class="cta-subtitle">Dicci quale robot devi equipaggiare: verifichiamo compatibilità, disponibilità e prezzo. Risposta entro 12 ore.</p>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:8px;">
          <a href="index.html#cta-finale" class="btn btn-primary">Richiedi disponibilità</a>
          <a href="umanoidi.html" class="btn btn-secondary">Vedi i robot</a>
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
open(os.path.join(ROOT, "accessori.html"), "w", encoding="utf-8").write(HTML)
print(f"written accessori.html ({total} accessori, {len(HTML)} chars)")
