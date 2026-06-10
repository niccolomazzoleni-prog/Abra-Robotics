# -*- coding: utf-8 -*-
"""Genera accessori.html (catalogo accessori Unitree) + scarica immagini.
Dati da RoboStore. Prezzi tenuti in commento HTML (convenzione sito)."""
import os, sys, urllib.request, ssl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from site_nav import render_site_nav

SITE_NAV_HTML = render_site_nav("")
IMGDIR = os.path.join(ROOT, "images", "accessori")
os.makedirs(IMGDIR, exist_ok=True)
CDN = "https://robostore.com/cdn/shop/files/"

# (slug, nome, descrizione, spec, prezzo_usd, image_filename, url_prodotto)
ACC = {
 "Mani e gripper": [
  ("dex3-1","Unitree Dex3-1","Mano robotica a 3 dita leggera per manipolazione di precisione e ricerca.","7 DoF · 710 g · opz. 33 sensori tattili","$6.500","unitree-dex3-1-dexterous-hands-with-tactile-sensors-7544266.jpg"),
  ("dex5-1","Unitree Dex5-1","Mano dexterous high-end per manipolazione avanzata su umanoidi.","Mano singola · high-end","$25.000","unitree-dex5-1-robotic-hands-4377616.jpg"),
  ("inspire-rh56","Inspire RH56DFQ","Mano a 5 dita antropomorfa con sensori di pressione, compatibile ROS.","6 DoF · 540 g · carico 3 kg","$9.500","inspire-robots-rh56dfq-dexterous-hands-5-finger-robotic-manipulator-176100.png"),
  ("dex1-1-v1","Unitree Dex1-1 V1","Pinza standard per umanoidi G1.","Gripper standard","$380","unitree-dex1-1-v1-standard-gripper-9119898.jpg"),
  ("dex1-1-v2","Unitree Dex1-1 V2","Gripper avanzato con camera RGB integrata per grasping vision-guided.","Gripper + camera RGB","$580","unitree-dex1-1-v2-advanced-gripper-with-rgb-camera-3167065.jpg"),
 ],
 "Batterie e alimentazione": [
  ("batt-go2","Batteria Go2","Batteria di ricambio per quadrupede Go2 (EDU e Pro).","8.000 / 15.000 mAh","$560","unitree-go2-ai-robot-dog-battery-904150.webp"),
  ("batt-b2","Batteria B2 alta capacità","Batteria ad alta capacità per quadrupede industriale B2.","45 Ah · 2250 Wh","$4.200","unitree-b2-quadruped-robot-high-capacity-battery-6102761.jpg"),
  ("batt-g1","Batteria G1","Batteria di ricambio ad alte prestazioni per umanoide G1.","High-performance","$800","unitree-g1-humanoid-high-performance-battery-325427.jpg"),
  ("batt-h1","Batteria H1","Batteria di ricambio ad alte prestazioni per umanoide H1.","High-performance","$1.580","unitree-h1-humanoid-high-performance-battery-2657496.png"),
  ("batt-go1","Batteria Go1","Batteria di ricambio per quadrupede Go1.","6.000 mAh","$499","unitree-go1-ai-robot-dog-battery-213508.webp"),
  ("go2-charging","Go2 Self-Charging Board","Base di ricarica wireless ad alta efficienza per Go2 EDU+.","Ricarica wireless","$1.050","unitree-go2-self-charging-board-568056.png"),
 ],
 "Sensori LiDAR e camere": [
  ("livox-mid360","Livox MID-360 LiDAR","LiDAR 3D a 360° per mapping e navigazione autonoma.","3D · 360°","$4.275","livox-mid360-lidar-339214.png"),
  ("hesai-xt16","Hesai XT16 3D LiDAR","LiDAR 3D a 16 canali per perception ad alta risoluzione.","16 canali · 3D","$6.650","hesai-xt16-3d-lidar-605177.png"),
 ],
 "Controllo e sviluppo": [
  ("rc-g1","Telecomando G1","Telecomando per umanoide G1.","Remote controller","$450","unitree-g1-remote-controller-668299.jpg"),
  ("rc-go2","Telecomando Go2","Telecomando per quadrupede Go2.","Remote controller","$375","unitree-g1-remote-controller-668299.jpg"),
  ("g1-teleop","G1 Teleoperation Kit","Kit teleoperazione full-body in VR con visore PICO 4 Ultra.","Full-body VR · PICO 4 Ultra","$6.000","unitree-g1-teleoperation-kit-full-body-vr-control-with-pico-4-ultra-3154174.jpg"),
  ("g1-gantry","G1 Gantry","Telaio di supporto per sviluppo e test sicuri dell'umanoide G1.","Gantry sviluppo","$960","g1-gantry-for-humanoid-development-5758653.jpg"),
  ("jetson-thor","Jetson AGX Thor Backplate","Modulo di espansione compute NVIDIA Jetson AGX Thor per G1.","AI onboard · backplate","$15.200","nvidia-jetson-agx-thor-backplate-expansion-for-unitree-g1-9926687.jpg"),
 ],
 "Bracci robotici": [
  ("z1","Unitree Z1","Braccio robotico 6-DoF di precisione con force control.","6 DoF · force control","$11.900","unitree-z1-robotic-arms-253379.jpg"),
  ("d1","Go2 Servo Arm D1","Braccio servo D1 montabile su Go2 per manipolazione mobile.","Servo arm","$4.655","unitree-go2-ai-robot-dog-servo-arm-6246944.jpg"),
  ("d1-t","D1-T Teleop Kit","Kit doppio braccio servo D1-T per teleoperazione leader-follower.","Doppio braccio · teleop","$12.000","unitree-d1-t-servo-arm-teleoperation-kits-7144552.jpg"),
  ("z1-gripper","Z1 Gripper","Pinza end-effector per braccio Z1.","End-effector","$2.150","unitree-z1-gripper-for-robotic-arm-3503458.jpg"),
  ("z1-d435i","Z1 Gripper + D435i","Pinza Z1 con camera depth Intel RealSense D435i integrata.","+ depth D435i","$3.390","unitree-z1-gripper-with-intel-realsense-d435i-depth-sensor-6383637.jpg"),
  ("z1-d405","Z1 Gripper + D405","Pinza Z1 con camera depth Intel RealSense D405 integrata.","+ depth D405","$3.390","unitree-z1-gripper-with-intel-realsense-d405-depth-sensor-6858284.jpg"),
  ("z1-motor","Z1 Arm Motor","Attuatore/motore di ricambio per giunto del braccio Z1.","Ricambio giunto","$390","unitree-z1-robotic-arm-motor-replacement-joint-actuator-5866950.jpg"),
 ],
}

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
def fetch(fn, slug):
    ext = os.path.splitext(fn)[1]
    dst = os.path.join(IMGDIR, slug + ext)
    if os.path.exists(dst): return "accessori/"+slug+ext
    try:
        req = urllib.request.Request(CDN+fn+"?width=800", headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r: data = r.read()
        if len(data) < 1500: raise RuntimeError("too small")
        open(dst,"wb").write(data); return "accessori/"+slug+ext
    except Exception as e:
        print("  FAIL", slug, e); return None

def card(item):
    slug, name, desc, spec, price, fn = item
    rel = fetch(fn, slug)
    img = f'<img src="images/{rel}" alt="{name}" loading="lazy" onerror="this.style.display=\'none\';this.parentElement.classList.add(\'no-img\');">' if rel else '<div class="acc-noimg">Unitree</div>'
    return f'''        <!-- {name} — prezzo rif. {price} USD -->
        <article class="acc-card">
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
  <meta name="description" content="Catalogo accessori Unitree distribuiti in Italia da Abra Robotics: mani dexterous Dex3/Dex5/Inspire, batterie, LiDAR Livox e Hesai, telecomandi, bracci Z1 e D1, moduli di calcolo.">
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
    <p>Distributore ufficiale Unitree in Italia. <a href="assessment.html">Trova il robot giusto →</a></p>
  </div>

{SITE_NAV_HTML}

  <section class="collection-hero">
    <div class="container">
      <p class="label">Accessori Unitree</p>
      <h1>Accessori e moduli Unitree</h1>
      <p class="lead">Mani dexterous, batterie, sensori LiDAR, telecomandi, bracci robotici e moduli di calcolo per estendere i robot Unitree. Tutti gli accessori sono disponibili tramite Abra Robotics, distributore ufficiale in Italia.</p>
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
