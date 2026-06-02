# -*- coding: utf-8 -*-
"""Generatore schede prodotto quadrupedi Unitree (Abra Robotics).
Dati da RoboStore. Riusa _template.html + product.css/js."""
import os
from _buy import buy_area, schema
BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = open(os.path.join(BASE, "_template.html"), encoding="utf-8").read()

# Lineup ordinato (per neighbor-comparison). go2-edu-plus = pagina esistente.
LINEUP = ["go2-pro", "go2-edu", "go2-edu-plus", "go2-ent-u2", "a2", "a2-pro", "b2"]
COMPACT = {
 "go2-pro":     dict(file="unitree-go2-pro.html",          short="Go2 Pro",        tag="Consumer / base",        payload="10 kg", speed="1,7 m/s", computing="8-core CPU",        lidar="3D L1",       ip="—",    warranty="12 mesi"),
 "go2-edu":     dict(file="unitree-go2-edu.html",          short="Go2 EDU",        tag="Education · 40 TOPS",    payload="12 kg", speed="2 m/s",   computing="Orin Nano 40 TOPS", lidar="4D L2",       ip="—",    warranty="12 mesi"),
 "go2-edu-plus":dict(file="unitree-go2-edu-plus.html",     short="Go2 EDU+",       tag="Education · 100 TOPS",   payload="12 kg", speed="2 m/s",   computing="Orin NX 100 TOPS",  lidar="4D L2",       ip="—",    warranty="12 mesi"),
 "go2-ent-u2":  dict(file="unitree-go2-enterprise-u2.html",short="Go2 Ent+ U2",    tag="Enterprise · sorveglianza",payload="10 kg",speed="1,7 m/s", computing="8-core CPU",        lidar="L1",          ip="—",    warranty="12 mesi"),
 "a2":          dict(file="unitree-a2.html",               short="A2",             tag="Industriale · IP56",     payload="25 kg", speed="~5 m/s",  computing="8-core + Intel i7", lidar="Industriale", ip="IP56", warranty="12 mesi"),
 "a2-pro":      dict(file="unitree-a2-pro.html",           short="A2 Pro",         tag="Field autonomy · IP67",  payload="25 kg", speed="~5 m/s",  computing="Tri-processore i7", lidar="Dual ind.",   ip="IP67", warranty="12 mesi"),
 "b2":          dict(file="unitree-b2.html",               short="B2",             tag="Industriale pesante · IP67",payload="40 kg",speed=">6 m/s",  computing="Intel i5 + i7",     lidar="32 canali",   ip="IP67", warranty="12 mesi"),
}

V = {}
V["go2-pro"] = dict(
  title="Unitree Go2 Pro", short="Go2 Pro", tag="Consumer / base", imgdir="go2-pro",
  subtitle="Il quadrupede entry-level Unitree: agile, connesso e pronto all'uso per demo, education e prototipazione. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree Go2 Pro: quadrupede agile con LiDAR 3D L1, velocità 1,7 m/s, payload 10 kg, Wi-Fi 6 e 4G. Distributore ufficiale Unitree in Italia.",
  desc="Go2 Pro è la porta d'ingresso alla robotica quadrupede Unitree: LiDAR 3D L1 a campo ultra-ampio (360°×90°), camera frontale HD 120°, connettività Wi-Fi 6 e modulo 4G integrato. Agile e robusto, supera pendenze fino a 40° e gradini fino a 16 cm.",
  speed="1,7 m/s", payload="10 kg", payload_static=None, weight="15 kg",
  dims_stand="700 × 310 × 400 mm", dims_crouch="760 × 310 × 200 mm", dof="12", torque="45 N·m",
  step="16 cm", climb="40°", batt="8.000 mAh", runtime="1–2 h", charger="33,6V / 9A",
  computing_full="Processore 8-core (no sviluppo secondario)", computing_short="8-core CPU", dev="No",
  lidar="LiDAR 3D L1 (360°×90°)", camera="HD 1280×720 · FOV 120°", depth="Compatibile (non inclusa)",
  ip="Non dichiarato", conn="Wi-Fi 6 dual band · Bluetooth 5.2 · 4G integrato", temp="—",
  audio="Speaker 3W · microfono intercom", sdk="ROS · Python · C++ · programmazione grafica", warranty="12 mesi",
  stats=[("10","kg","Carico utile"),("12","","Giunti motorizzati"),("40","°","Pendenza max")],
  visual_p1="Go2 Pro mette la robotica quadrupede alla portata di tutti: percezione LiDAR 3D a 360°, camera HD frontale e connettività 4G integrata per il controllo da remoto, in un corpo agile da 15 kg che supera pendenze e gradini con naturalezza.",
  feats=[("Percezione LiDAR 3D","LiDAR L1 a campo ultra-ampio 360°×90° per consapevolezza dell'ambiente e navigazione assistita."),
         ("Agilità su ogni terreno","12 giunti motorizzati, gradini fino a 16 cm e pendenze fino a 40° per muoversi ovunque."),
         ("Sempre connesso","Wi-Fi 6, Bluetooth 5.2 e modulo 4G integrato per controllo e streaming da remoto.")],
)
V["go2-edu"] = dict(
  title="Unitree Go2 EDU", short="Go2 EDU", tag="Education · 40 TOPS", imgdir="go2-edu",
  subtitle="Il quadrupede per la didattica e lo sviluppo: NVIDIA Jetson Orin Nano (40 TOPS), LiDAR 4D L2 e SDK aperto. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree Go2 EDU: quadrupede da ricerca con NVIDIA Jetson Orin Nano 40 TOPS, LiDAR 4D L2, sensore di forza al piede e SDK aperto ROS. Distributore ufficiale Unitree in Italia.",
  desc="Go2 EDU porta lo sviluppo a bordo: 8-core CPU affiancata da NVIDIA Jetson Orin Nano 8GB (40 TOPS) con sviluppo secondario, LiDAR 4D L2 a campo ultra-ampio e sensore di forza al piede. Payload fino a 12 kg, pendenze fino a 40° e SDK aperto ROS/Python/C++.",
  speed="2 m/s", payload="12 kg", payload_static=None, weight="15 kg",
  dims_stand="700 × 310 × 400 mm", dims_crouch="760 × 310 × 200 mm", dof="12", torque="45 N·m",
  step="16 cm", climb="40°", batt="8.000–15.000 mAh", runtime="2–4 h", charger="33,6V / 9A (fast charge)",
  computing_full="8-core CPU + NVIDIA Jetson Orin Nano 8GB (40 TOPS)", computing_short="Jetson Orin Nano · 40 TOPS", dev="Sì",
  lidar="LiDAR 4D L2 (360°×90°)", camera="HD 1280×720 · FOV 120°", depth="D435i compatibile (non inclusa)",
  ip="Non dichiarato", conn="Wi-Fi 6 dual band · Bluetooth 5.2 · 4G integrato", temp="—",
  audio="Speaker 3W · microfono intercom · funzione vocale", sdk="ROS · Python · C++ · ISS 2.0 · OTA · RTT 2.0", warranty="12 mesi",
  stats=[("40","TOPS","Computing Orin Nano"),("12","kg","Carico utile"),("40","°","Pendenza max")],
  visual_p1="Go2 EDU è la piattaforma di sviluppo quadrupede: il modulo NVIDIA Jetson Orin Nano da 40 TOPS abilita visione, navigazione e reinforcement learning a bordo, mentre il LiDAR 4D L2 e il sensore di forza al piede forniscono la percezione necessaria alla ricerca.",
  feats=[("Sviluppo a bordo","NVIDIA Jetson Orin Nano 8GB (40 TOPS) con SDK aperto: addestra ed esegui le tue policy direttamente sul robot."),
         ("Percezione LiDAR 4D","LiDAR L2 a campo ultra-ampio 360°×90° e sensore di forza al piede per mapping e navigazione autonoma."),
         ("Pronto per la ricerca","ROS, Python e C++, OTA e moduli espandibili per progetti di education e R&D.")],
)
V["go2-ent-u2"] = dict(
  title="Unitree Go2 Enterprise+ U2", short="Go2 Ent+ U2", tag="Enterprise · sorveglianza", imgdir="go2-ent-u2",
  subtitle="Configurazione enterprise del Go2: segnalazione visiva e audio, comunicazione sicura dual-link e video HD in tempo reale. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree Go2 Enterprise+ U2: quadrupede per sorveglianza e ispezione con segnalazione visiva/audio, comunicazione dual-link sicura e video HD real-time. Distributore ufficiale Unitree in Italia.",
  desc="Go2 Enterprise+ U2 estende la piattaforma Go2 con segnalazione visiva e diffusione audio, comunicazione sicura dual-link, video HD in tempo reale e luci di avviso. Pensato per sorveglianza, ispezione e operazioni sul campo, con controller dotato di schermo.",
  speed="1,7 m/s", payload="10 kg", payload_static=None, weight="15 kg",
  dims_stand="700 × 310 × 400 mm", dims_crouch="760 × 310 × 200 mm", dof="12", torque="45 N·m",
  step="16 cm", climb="40°", batt="8.000 mAh", runtime="1–2 h", charger="33,6V / 9A",
  computing_full="Processore 8-core (no sviluppo secondario)", computing_short="8-core CPU", dev="No",
  lidar="LiDAR L1 (360°×90°)", camera="HD · video real-time", depth="Non inclusa",
  ip="Non dichiarato", conn="Wi-Fi 6 · Bluetooth 5.2 · 4G · dual-link sicuro", temp="—",
  audio="Diffusione audio a lungo raggio · microfono", sdk="Programmazione grafica · ROS compatibile", warranty="12 mesi",
  stats=[("10","kg","Carico utile"),("12","","Giunti motorizzati"),("40","°","Pendenza max")],
  visual_p1="Go2 Enterprise+ U2 è la configurazione da campo: luci di avviso e diffusione audio a lungo raggio, comunicazione sicura dual-link e video HD in tempo reale, per sorveglianza perimetrale e ispezioni dove serve segnalare e comunicare.",
  feats=[("Segnalazione visiva e audio","Luci di avviso e diffusione audio a lungo raggio per sorveglianza e gestione delle aree."),
         ("Comunicazione sicura","Doppio link di comunicazione cifrato e video HD in tempo reale dal controller con schermo."),
         ("Operazioni sul campo","Agilità Go2 con dotazione enterprise per ispezione e sorveglianza h24.")],
)
V["a2"] = dict(
  title="Unitree A2", short="A2", tag="Industriale · IP56", imgdir="a2",
  subtitle="Quadrupede di nuova generazione per ambienti industriali esigenti: 25 kg di carico in movimento, autonomia oltre 5 ore e Intel Core i7 a bordo. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree A2: quadrupede industriale IP56 con 25 kg di carico in movimento, 100 kg statico, autonomia >5 h, Intel Core i7 e LiDAR industriale. Distributore ufficiale Unitree in Italia.",
  desc="A2 è il quadrupede industriale di nuova generazione: 25 kg di carico continuo in movimento (100 kg statico), autonomia oltre 5 ore con doppia batteria hot-swap e computing 8-core con Intel Core i7. Grado IP56, range operativo -20°C/+55°C e LiDAR industriale espandibile.",
  speed="~5 m/s", payload="25 kg", payload_static="100 kg", weight="37 kg",
  dims_stand="820 × 440 × 570 mm", dims_crouch="720 × 550 × 220 mm", dof="12", torque="180 N·m",
  step="30 cm", climb="45°", batt="2 × 9.000 mAh (907,2 Wh)", runtime=">5 h", charger="hot-swap · ~1 h/batteria",
  computing_full="8-core CPU + Intel Core i7 (sviluppo utente)", computing_short="8-core + Intel i7", dev="Sì",
  lidar="LiDAR industriale (espandibile a 2)", camera="HD grandangolare (espandibile a 2)", depth="—",
  ip="IP56", conn="Wi-Fi 6 · BT 5.2 · RS485 ×2 · CAN ×2 · Gigabit Ethernet ×2 · USB-C ×2", temp="-20°C / +55°C",
  audio="Array microfonico · speaker · funzione vocale", sdk="Sviluppo secondario · ROS · OTA · RTT 2.0", warranty="12 mesi",
  stats=[("25","kg","Carico in movimento"),("100","kg","Carico statico"),("45","°","Pendenza max")],
  visual_p1="A2 è progettato per il lavoro industriale: 25 kg di carico continuo in movimento e 100 kg statico, doppia batteria hot-swap per oltre 5 ore di autonomia e Intel Core i7 a bordo per percezione e sviluppo, in un grado di protezione IP56 e range -20°C/+55°C.",
  feats=[("Carico industriale","25 kg di carico continuo in movimento e fino a 100 kg statico, con coppia al giunto di 180 N·m."),
         ("Autonomia estesa","Doppia batteria hot-swap da 18.000 mAh per oltre 5 ore di lavoro e ~20 km a vuoto."),
         ("Robusto e connesso","Grado IP56, range -20°C/+55°C, Intel Core i7 e interfacce RS485, CAN, Ethernet e USB-C.")],
)
V["a2-pro"] = dict(
  title="Unitree A2 Pro", short="A2 Pro", tag="Field autonomy · IP67", imgdir="a2-pro",
  subtitle="Per navigazione autonoma avanzata, mapping e operazioni sul campo: dual LiDAR, GPS, architettura tri-processore e protezione fino a IP67. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree A2 Pro: quadrupede per navigazione autonoma con dual LiDAR, GPS, 4G, architettura tri-processore e protezione fino a IP67. Distributore ufficiale Unitree in Italia.",
  desc="A2 Pro è la versione per autonomia di campo dell'A2: doppio LiDAR industriale (anteriore e posteriore), GPS e 4G integrati, posizionamento vettoriale wireless e architettura tri-processore (8-core + Intel i7 + modulo di espansione). Protezione fino a IP67 e compatibilità NVIDIA Isaac Sim.",
  speed="~5 m/s", payload="25 kg", payload_static="100 kg", weight="37 kg",
  dims_stand="820 × 440 × 570 mm", dims_crouch="720 × 550 × 220 mm", dof="12", torque="180 N·m",
  step="30 cm", climb="45°", batt="2 × 9.000 mAh (907,2 Wh)", runtime=">5 h", charger="hot-swap · ~1 h/batteria",
  computing_full="8-core CPU + Intel Core i7 + modulo di espansione (tri-processore)", computing_short="Tri-processore + i7", dev="Sì",
  lidar="Dual LiDAR industriale (ant. + post.)", camera="HD frontale", depth="—",
  ip="IP56–IP67 (componenti core IP67)", conn="Wi-Fi 6 · BT 5.2 · 4G · GPS · posizionamento vettoriale · USB-C ×4", temp="-20°C / +55°C",
  audio="Array microfonico · speaker", sdk="Isaac Sim · SLAM avanzato · navigazione autonoma · surround point-cloud", warranty="12 mesi",
  stats=[("25","kg","Carico in movimento"),("100","kg","Carico statico"),("45","°","Pendenza max")],
  visual_p1="A2 Pro è pensato per l'autonomia sul campo: doppio LiDAR anteriore e posteriore, GPS e 4G integrati e posizionamento vettoriale wireless alimentano SLAM e navigazione autonoma, su un'architettura tri-processore e una protezione che arriva a IP67.",
  feats=[("Navigazione autonoma","Dual LiDAR, GPS e posizionamento vettoriale wireless per SLAM avanzato e mapping del territorio."),
         ("Architettura tri-processore","8-core + Intel i7 + modulo di espansione e compatibilità NVIDIA Isaac Sim per AI ad alte prestazioni."),
         ("Pronto per il campo","Protezione fino a IP67, GPS e 4G integrati e 4 porte USB-C per operazioni outdoor prolungate.")],
)
V["b2"] = dict(
  title="Unitree B2", short="B2", tag="Industriale pesante · IP67", imgdir="b2",
  subtitle="Il quadrupede industriale ad alte prestazioni: oltre 6 m/s, carico statico 120 kg, IP67 e LiDAR automotive a 32 canali. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree B2: quadrupede industriale pesante IP67, velocità >6 m/s, carico statico 120 kg, LiDAR automotive 32 canali, batteria 2250 Wh. Distributore ufficiale Unitree in Italia.",
  desc="B2 è il quadrupede industriale pesante di Unitree: velocità oltre 6 m/s, carico statico fino a 120 kg (oltre 40 kg in movimento), coppia al giunto di 360 N·m e batteria da 2250 Wh per 4-6 ore di autonomia. Grado IP67, LiDAR automotive a 32 canali e compatibilità con il braccio Z1.",
  speed=">6 m/s", payload="40 kg", payload_static="120 kg", weight="60 kg",
  dims_stand="1098 × 450 × 645 mm", dims_crouch="880 × 460 × 330 mm", dof="12", torque="360 N·m",
  step="40 cm", climb=">45°", batt="45 Ah (2250 Wh)", runtime="4–6 h", charger="ricarica wireless compatibile",
  computing_full="Intel Core i5 (piattaforma) + Intel Core i7 (sviluppo) · Jetson Orin NX opzionale", computing_short="Intel i5 + i7", dev="Sì",
  lidar="LiDAR automotive a 32 canali", camera="2 × depth + 2 × ottiche frontali", depth="2 × depth incluse",
  ip="IP67", conn="Wi-Fi 6 · BT 5.2 · fino a 3 dispositivi di calcolo", temp="-20°C / +55°C",
  audio="—", sdk="Sviluppo secondario · OTA · rilevamento e avoidance · compatibile Z1", warranty="12 mesi",
  stats=[("120","kg","Carico statico"),("40","kg","Carico in movimento"),("360","N·m","Coppia max giunto")],
  visual_p1="B2 è la forza bruta della gamma: oltre 6 m/s di velocità, 120 kg di carico statico e 360 N·m di coppia al giunto, con grado IP67 e LiDAR automotive a 32 canali. Salta oltre 1,6 m e affronta i contesti industriali più severi, anche con il braccio Z1.",
  feats=[("Prestazioni industriali","Oltre 6 m/s, 120 kg di carico statico e 360 N·m di coppia: il quadrupede più potente della gamma."),
         ("Costruito per l'industria pesante","Grado IP67, range -20°C/+55°C e batteria da 2250 Wh per 4-6 ore di lavoro continuo."),
         ("Percezione automotive","LiDAR a 32 canali, doppia camera depth e ottiche frontali, con compatibilità braccio Z1.")],
)

for c, d in V.items():
    d["code"] = c
    d["cmp"] = COMPACT[c]

# ── helpers ──
def split_vu(s):
    """'1,7 m/s' -> ('1,7','m/s'); '45°' -> ('45°',''); '12' -> ('12','')"""
    if " " in s:
        p = s.split(" ", 1); return p[0], p[1]
    return s, ""

def neighbors(code):
    i = LINEUP.index(code)
    if i == 0: return LINEUP[0:3]
    if i == len(LINEUP)-1: return LINEUP[-3:]
    return [LINEUP[i-1], code, LINEUP[i+1]]

def key_specs(d):
    items = [
      split_vu(d["speed"]) + ("Velocità max",),
      split_vu(d["payload"]) + ("Carico utile",),
      split_vu(d["runtime"]) + ("Autonomia",),
      split_vu(d["weight"]) + ("Peso",),
      split_vu(d["climb"]) + ("Pendenza max",),
      split_vu(d["torque"]) + ("Coppia giunto",),
    ]
    out = []
    for val, unit, label in items:
        u = f' <small style="font-size:.9rem;font-weight:600">{unit}</small>' if unit else ""
        out.append(f'''            <div class="key-spec">
              <span class="key-spec-value">{val}{u}</span>
              <span class="key-spec-label">{label}</span>
            </div>''')
    return "\n".join(out)

def marquee(d):
    items = [d["title"], f'Carico {d["payload"]}', f'{d["speed"]} velocità', f'LiDAR {d["cmp"]["lidar"]}',
             d["computing_short"]] + ([f'Protezione {d["ip"]}'] if d["ip"] not in ("Non dichiarato","—") else []) + \
            [f'Garanzia {d["warranty"]}', 'Distributore ufficiale Italia']
    return "\n        ".join(f'<span class="marquee-text">{t}</span><span class="marquee-dot">●</span>' for t in items)

def stats(d):
    out = []
    for target, unit, label in d["stats"]:
        u = f'<span class="stat-unit">{unit}</span>' if unit else ""
        out.append(f'''        <div class="product-stat">
          <span class="stat-number"><span class="counter" data-target="{target}">0</span>{u}</span>
          <span class="stat-label">{label}</span>
        </div>''')
    return "\n".join(out)

def included(d):
    cards = [("Robot", d["short"]), ("Sensori", d["cmp"]["lidar"]),
             ("Computing", d["computing_short"]), ("Alimentazione", "Batteria × 1"),
             ("Copertura", f'Garanzia {d["warranty"]}')]
    return "\n".join(f'''        <div class="included-card">
          <span class="included-card-label">{l}</span>
          <span class="included-card-name">{n}</span>
        </div>''' for l, n in cards)

def specs_accordion(d):
    static_row = f'<tr><td>Carico statico</td><td>{d["payload_static"]}</td></tr>' if d.get("payload_static") else ""
    return f'''          <details class="faq-item" open>
            <summary>Telaio e dimensioni</summary>
            <table class="specs-table">
              <tr><td>Dimensioni in piedi</td><td>{d["dims_stand"]}</td></tr>
              <tr><td>Dimensioni accovacciato</td><td>{d["dims_crouch"]}</td></tr>
              <tr><td>Peso (con batteria)</td><td>{d["weight"]}</td></tr>
              <tr><td>Giunti motorizzati</td><td>{d["dof"]} DoF</td></tr>
              <tr><td>Materiali</td><td>Lega di alluminio + plastica tecnica ad alta resistenza</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Mobilità e performance</summary>
            <table class="specs-table">
              <tr><td>Velocità max</td><td>{d["speed"]}</td></tr>
              <tr><td>Carico utile (movimento)</td><td>{d["payload"]}</td></tr>
              {static_row}
              <tr><td>Coppia max giunto</td><td>{d["torque"]}</td></tr>
              <tr><td>Gradino max</td><td>{d["step"]}</td></tr>
              <tr><td>Pendenza max</td><td>{d["climb"]}</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Batteria e alimentazione</summary>
            <table class="specs-table">
              <tr><td>Batteria</td><td>{d["batt"]}</td></tr>
              <tr><td>Autonomia</td><td>{d["runtime"]}</td></tr>
              <tr><td>Ricarica</td><td>{d["charger"]}</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Computing e sviluppo</summary>
            <table class="specs-table">
              <tr><td>Unità di calcolo</td><td>{d["computing_full"]}</td></tr>
              <tr><td>Sviluppo secondario</td><td>{d["dev"]}</td></tr>
              <tr><td>SDK / software</td><td>{d["sdk"]}</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Sensori e protezione</summary>
            <table class="specs-table">
              <tr><td>LiDAR</td><td>{d["lidar"]}</td></tr>
              <tr><td>Camera</td><td>{d["camera"]}</td></tr>
              <tr><td>Depth camera</td><td>{d["depth"]}</td></tr>
              <tr><td>Grado di protezione</td><td>{d["ip"]}</td></tr>
              <tr><td>Temperatura operativa</td><td>{d["temp"]}</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Connettività e sistema</summary>
            <table class="specs-table">
              <tr><td>Connettività</td><td>{d["conn"]}</td></tr>
              <tr><td>Audio</td><td>{d["audio"]}</td></tr>
              <tr><td>Garanzia</td><td>{d["warranty"]}</td></tr>
            </table>
          </details>'''

def parallax(d, imgs):
    caps = [(d["payload"], "Carico utile"), (d["weight"], "Peso con batteria"),
            (d["speed"], "Velocità massima"), (d["torque"], "Coppia max giunto")]
    p = imgs
    return f'''          <div class="parallax-col-a" id="parallax-col-a">
            <div class="parallax-img-wrap">
              <img src="{p[0]}" alt="{d['short']} vista" loading="lazy">
              <div class="parallax-caption"><span class="parallax-caption-value">{caps[0][0]}</span><span class="parallax-caption-label">{caps[0][1]}</span></div>
            </div>
            <div class="parallax-img-wrap">
              <img src="{p[1]}" alt="{d['short']} dettaglio" loading="lazy">
              <div class="parallax-caption"><span class="parallax-caption-value">{caps[1][0]}</span><span class="parallax-caption-label">{caps[1][1]}</span></div>
            </div>
          </div>
          <div class="parallax-col-b" id="parallax-col-b">
            <div class="parallax-img-wrap">
              <img src="{p[2]}" alt="{d['short']} in movimento" loading="lazy">
              <div class="parallax-caption"><span class="parallax-caption-value">{caps[2][0]}</span><span class="parallax-caption-label">{caps[2][1]}</span></div>
            </div>
            <div class="parallax-img-wrap">
              <img src="{p[3]}" alt="{d['short']} dettaglio" loading="lazy">
              <div class="parallax-caption"><span class="parallax-caption-value">{caps[3][0]}</span><span class="parallax-caption-label">{caps[3][1]}</span></div>
            </div>
          </div>'''

def features(d, imgs):
    """Feature card con immagine statica (no video per i quadrupedi)."""
    pics = [imgs[1 % len(imgs)], imgs[2 % len(imgs)], imgs[3 % len(imgs)]]
    out = []
    for i, (h, p) in enumerate(d["feats"]):
        out.append(f'''        <div class="feature-card">
          <div class="feature-video-wrap">
            <img src="{pics[i]}" alt="{h} {d['short']}" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
          </div>
          <h3>{h}</h3>
          <p>{p}</p>
        </div>''')
    return "\n".join(out)

def gallery_thumbs(d, imgs):
    return "\n".join(f'            <div class="gallery-thumb{" active" if i==0 else ""}" data-index="{i}"><img src="{s}" alt="{d["short"]} vista {i+1}"></div>' for i, s in enumerate(imgs))

def comp_cards(code):
    trio = neighbors(code); out = []
    for c in trio:
        cd = COMPACT[c]; cur = " current" if c == code else ""
        out.append(f'''        <div class="comp-model-card{cur}">
          <span class="comp-model-name">{cd["short"]}</span>
          <span class="comp-model-tag">{cd["tag"]}</span>
        </div>''')
    return "\n".join(out), trio

def comp_table(code, trio):
    def cells(k): return "".join(f'<td>{COMPACT[c][k]}</td>' for c in trio)
    def linkrow():
        tds = []
        for c in trio:
            if c == code: tds.append('<td style="padding:16px;"><a href="#form" class="btn btn-primary btn-card">Richiedi info</a></td>')
            else: tds.append(f'<td style="padding:16px;"><a href="{COMPACT[c]["file"]}" class="btn btn-secondary btn-card">Vedi scheda</a></td>')
        return "".join(tds)
    return f'''        <table class="comp-table">
          <colgroup><col><col><col><col></colgroup>
          <tbody>
            <tr class="comp-section-row"><td colspan="4">Mobilità e carico</td></tr>
            <tr><td>Carico utile</td>{cells("payload")}</tr>
            <tr><td>Velocità max</td>{cells("speed")}</tr>
            <tr class="comp-section-row"><td colspan="4">Computing e percezione</td></tr>
            <tr><td>Computing</td>{cells("computing")}</tr>
            <tr><td>LiDAR</td>{cells("lidar")}</tr>
            <tr><td>Protezione</td>{cells("ip")}</tr>
            <tr class="comp-section-row"><td colspan="4">Copertura</td></tr>
            <tr><td>Garanzia</td>{cells("warranty")}</tr>
            <tr><td></td>{linkrow()}</tr>
          </tbody>
        </table>'''

def comp_mobile(code, trio):
    out = []
    for c in trio:
        cd = COMPACT[c]
        if c == code:
            head = f'<div style="background:var(--black);padding:20px 16px;"><span style="display:block;font-family:var(--font);font-size:1rem;font-weight:700;color:var(--white);margin-bottom:4px;">{cd["short"]}</span><span style="font-size:0.78rem;color:rgba(255,255,255,0.45);">{cd["tag"]}</span></div>'
            wrap = '<div style="border:1px solid var(--black);border-radius:var(--radius);overflow:hidden;">'
            btn = '<a href="#form" class="btn btn-primary" style="width:100%;justify-content:center;display:flex;">Richiedi info</a>'
        else:
            head = f'<div style="background:var(--gray-50);padding:20px 16px;border-bottom:1px solid var(--gray-200);"><span style="display:block;font-family:var(--font);font-size:1rem;font-weight:700;color:var(--black);margin-bottom:4px;">{cd["short"]}</span><span style="font-size:0.78rem;color:var(--gray-400);">{cd["tag"]}</span></div>'
            wrap = '<div style="border:1px solid var(--gray-200);border-radius:var(--radius);overflow:hidden;">'
            btn = f'<a href="{cd["file"]}" class="btn btn-secondary" style="width:100%;justify-content:center;display:flex;">Vedi scheda</a>'
        out.append(f'''        {wrap}
          {head}
          <div style="background:var(--white);">
            <div class="cmr"><span>Carico</span><span>{cd["payload"]}</span></div>
            <div class="cmr"><span>Velocità</span><span>{cd["speed"]}</span></div>
            <div class="cmr"><span>Computing</span><span>{cd["computing"]}</span></div>
            <div class="cmr"><span>LiDAR</span><span>{cd["lidar"]}</span></div>
            <div class="cmr" style="border-bottom:none;"><span>Garanzia</span><span>{cd["warranty"]}</span></div>
          </div>
          <div style="padding:16px;background:var(--white);border-top:1px solid var(--gray-100);">{btn}</div>
        </div>''')
    return "\n".join(out)

def spec_mini(d):
    items = [split_vu(d["speed"])+("Velocità massima",), split_vu(d["payload"])+("Carico utile",),
             split_vu(d["runtime"])+("Autonomia",), split_vu(d["weight"])+("Peso totale",),
             split_vu(d["climb"])+("Pendenza max",), split_vu(d["torque"])+("Coppia giunto",),
             (d["cmp"]["lidar"],"big","LiDAR"), (d["computing_short"],"big","Computing"),
             (d["ip"] if d["ip"] not in ("Non dichiarato",) else "Wi-Fi 6","big","Protezione" if d["ip"] not in ("Non dichiarato","—") else "Connettività")]
    out = []
    for val, unit, label in items:
        if unit == "big":
            out.append(f'''        <div class="spec-mini-card">
          <span class="spec-mini-value" style="font-size:1.05rem;">{val}</span>
          <span class="spec-mini-label">{label}</span>
        </div>''')
        else:
            u = f' <small style="font-size:1rem;font-weight:600">{unit}</small>' if unit else ""
            out.append(f'''        <div class="spec-mini-card">
          <span class="spec-mini-value">{val}{u}</span>
          <span class="spec-mini-label">{label}</span>
        </div>''')
    return "\n".join(out)

def render(code):
    d = V[code]
    imgs = [f'assets/variants/{d["imgdir"]}/img-0{i}.jpg' for i in range(1, 6)]
    cards, trio = comp_cards(code)
    repl = {
      "%%LANG_TITLE%%": f'{d["title"]} — Robot Quadrupede | Abra Robotics',
      "%%METADESC%%": d["metadesc"],
      "%%FILENAME%%": d["cmp"]["file"],
      "%%COLLECTION_FILE%%": "quadrupedi.html",
      "%%COLLECTION_NAME%%": "Quadrupedi",
      "%%COMP_LABEL%%": "Gamma quadrupedi",
      "%%COMP_RANGE%%": "gamma quadrupedi Unitree",
      "%%BADGE%%": f"Robot Quadrupede · {d['tag']}",
      "%%TITLE%%": d["title"],
      "%%SUBTITLE%%": d["subtitle"],
      "%%KEYSPECS%%": key_specs(d),
      "%%DESC%%": d["desc"],
      "%%MARQUEE%%": marquee(d),
      "%%STATS%%": stats(d),
      "%%INCLUDED%%": included(d),
      "%%SPECS_ACCORDION%%": specs_accordion(d),
      "%%GALLERY_MAIN%%": imgs[0],
      "%%GALLERY_MAIN_ALT%%": f'{d["title"]} — Robot Quadrupede',
      "%%GALLERY_THUMBS%%": gallery_thumbs(d, imgs),
      "%%VISUAL_P1%%": d["visual_p1"],
      "%%PARALLAX%%": parallax(d, imgs),
      "%%FEATURES%%": features(d, imgs),
      "%%FEATURES_INTRO%%": f'Le capacità chiave di {d["short"]} — in sintesi.',
      "%%COMP_CARDS%%": cards,
      "%%COMP_TABLE%%": comp_table(code, trio),
      "%%COMP_MOBILE%%": comp_mobile(code, trio),
      "%%SPEC_MINI%%": spec_mini(d),
      "%%FORM_PRODUCT%%": d["title"],
      "%%BUY_AREA%%": buy_area(d["cmp"]["file"]),
      "%%PRODUCT_SCHEMA%%": schema(d["cmp"]["file"], d["title"], d["metadesc"], imgs[0]),
    }
    html = TEMPLATE
    for k, v in repl.items(): html = html.replace(k, v)
    open(os.path.join(BASE, d["cmp"]["file"]), "w", encoding="utf-8").write(html)
    return d["cmp"]["file"]

if __name__ == "__main__":
    # go2-edu-plus esiste gia (pagina hand-built): non rigenerare
    for code in ["go2-pro", "go2-edu", "go2-ent-u2", "a2", "a2-pro", "b2"]:
        print("written", render(code))
