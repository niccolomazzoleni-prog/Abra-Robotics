# -*- coding: utf-8 -*-
"""Generatore schede prodotto Unitree G1 (Abra Robotics).
Dati specifiche/immagini da RoboStore. Produce le pagine U1-U8 + Comp
replicando la struttura di unitree-g1.html, con CSS/JS condivisi."""
import os
import sys
from _buy import buy_area, schema

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(BASE), "scripts"))
from site_nav import render_site_nav

# ── Dati compatti per tutta la gamma (per neighbor-comparison) ──
# code -> dict(file, short, tag, hands, dof, tactile, computing, knee, warranty)
LINEUP = ["g1", "g1-u1", "g1-u2", "g1-u3", "g1-u4", "g1-u5", "g1-u6", "g1-u7", "g1-u8", "g1-comp"]
COMPACT = {
 "g1":     dict(file="unitree-g1.html",            short="G1 Air",         tag="Marketing e Comunicazione", hands="Dummy (no polsi)",   dof="23", tactile="—",   computing="8-core CPU",       knee="90 N·m",  warranty="8 mesi"),
 "g1-u1":  dict(file="unitree-g1-edu-standard.html",short="G1 EDU Standard",tag="Ricerca e sviluppo",      hands="Dummy (no polsi)",   dof="23", tactile="—",   computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-u2":  dict(file="unitree-g1-edu-plus.html",    short="G1 EDU Plus",    tag="Sviluppo avanzato",       hands="Dummy + polsi",      dof="28", tactile="—",   computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-u3":  dict(file="unitree-g1-edu-ultimate-a.html",short="G1 Ultimate A",tag="Manipolazione Dex3",      hands="Dex3 (3 dita)",      dof="42", tactile="—",   computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-u4":  dict(file="unitree-g1-edu-ultimate-b.html",short="G1 Ultimate B",tag="Dex3 tattile",            hands="Dex3-1 tattile",     dof="42", tactile="Sì",  computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-u5":  dict(file="unitree-g1-edu-ultimate-c.html",short="G1 Ultimate C",tag="Inspire 5 dita",          hands="Inspire 5 dita",     dof="40", tactile="Sì",  computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-u6":  dict(file="unitree-g1-edu-ultimate-d.html",short="G1 Ultimate D",tag="Inspire tattile top",     hands="Inspire 5 dita",     dof="40", tactile="Sì",  computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-u7":  dict(file="unitree-g1-edu-ultimate-e.html",short="G1 Ultimate E",tag="BrainCo 5 dita",          hands="BrainCo 5 dita",     dof="40", tactile="—",   computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-u8":  dict(file="unitree-g1-edu-ultimate-f.html",short="G1 Ultimate F",tag="BrainCo Touch",           hands="BrainCo Touch",      dof="40", tactile="Sì",  computing="Jetson Orin NX",   knee="120 N·m", warranty="18 mesi"),
 "g1-comp":dict(file="unitree-g1-comp.html",        short="G1 Comp",        tag="Atletico / competizioni", hands="Dummy + polsi (upg.)",dof="25", tactile="Opz.",computing="CPU (Jetson opz.)",knee="120 N·m", warranty="12 mesi"),
}

# ── Dati completi per variante da generare ──
# Campi: code, title, unum, subtitle, metadesc, desc, imgdir, n_imgs,
#        hands_full, computing_full, depthcam, sviluppo, arm, speed, weight,
#        dof breakdown, visual_p1, included list, stats, key_features (3)
V = {}

def base_specs(d):
    """tabella specifiche comune (accordion), variabile per chiave."""
    return d

V["g1-u1"] = dict(
  title="Unitree G1 EDU Standard", unum="U1", short="G1 EDU Standard",
  subtitle="Il robot umanoide entry-level per AI e ricerca: piattaforma G1 con NVIDIA Jetson Orin NX (100 TOPS) e sviluppo secondario abilitato. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Standard (U1): umanoide da ricerca con 23 gradi di libertà, NVIDIA Jetson Orin NX 16GB 100 TOPS, LiDAR 3D MID-360 e RealSense D435i. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Standard porta la piattaforma G1 nel mondo della ricerca: 8-core CPU affiancata da NVIDIA Jetson Orin NX 16GB (100 TOPS) per sviluppo secondario, con LiDAR 3D LIVOX MID-360 e depth camera Intel RealSense D435i. 23 gradi di libertà e coppia al ginocchio di 120 N·m per locomozione robusta in ambienti reali.",
  imgdir="g1-u1",
  hands_full="Mani dummy senza polsi", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="23", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","1 DoF"),("Polsi","0 DoF"),("Mani","0 DoF (dummy)"),("Testa","0 DoF")],
  visual_p1="G1 EDU Standard è la porta d'ingresso allo sviluppo: il modulo NVIDIA Jetson Orin NX 16GB da 100 TOPS abilita il deploy di policy di controllo, visione e reinforcement learning direttamente a bordo, mentre LiDAR e depth camera forniscono la percezione necessaria alla navigazione autonoma.",
  features=[("Sviluppo a bordo","Jetson Orin NX 16GB con 100 TOPS: addestra e fai girare le tue policy direttamente sul robot, senza PC esterno."),
            ("Locomozione robusta","Coppia al ginocchio di 120 N·m e controllo dinamico per camminare, recuperare da spinte e affrontare terreni irregolari."),
            ("Percezione 360°","LiDAR LIVOX MID-360 e depth camera RealSense D435i per mappatura e navigazione autonoma anche in spazi affollati.")],
)
V["g1-u2"] = dict(
  title="Unitree G1 EDU Plus", unum="U2", short="G1 EDU Plus",
  subtitle="Prestazioni potenziate per sviluppo robotico e AI: vita e polsi articolati (28 DoF), predisposto per mani Dex3, Dex5 e Inspire. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Plus (U2): umanoide da ricerca con 28 gradi di libertà, vita e polsi articolati, Jetson Orin NX 100 TOPS, predisposto per mani dexterous. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Plus aggiunge vita e polsi articolati (28 gradi di libertà totali) ed è predisposto per il montaggio di mani dexterous Dex3, Dex5 o Inspire a 5 dita. Mantiene il computing NVIDIA Jetson Orin NX 16GB (100 TOPS), LiDAR 3D MID-360 e depth camera RealSense D435i.",
  imgdir="g1-u2",
  hands_full="Mani dummy con polsi (predisposte upgrade)", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="28", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","3 DoF"),("Polsi (×2)","3 DoF"),("Mani","0 DoF (predisposte)"),("Range polso","P ±92,5° · Y ±92,5°")],
  visual_p1="G1 EDU Plus è la base modulare per la manipolazione: vita a 3 DoF e polsi a 3 DoF ampliano lo spazio di lavoro delle braccia, mentre l'interfaccia standard consente di montare mani Dex3, Dex5 o Inspire a 5 dita quando il progetto lo richiede.",
  features=[("Vita e polsi articolati","3 DoF alla vita e 3 DoF per polso ampliano raggio e destrezza delle braccia per task di manipolazione."),
            ("Pronto per le mani dexterous","Interfaccia standard per Dex3, Dex3-1 tattile, Dex5 e Inspire a 5 dita: aggiorni la manipolazione quando serve."),
            ("Computing da ricerca","NVIDIA Jetson Orin NX 16GB (100 TOPS) per AI a bordo, con LiDAR MID-360 e RealSense D435i per la percezione.")],
)
V["g1-u3"] = dict(
  title="Unitree G1 EDU Ultimate A", unum="U3", short="G1 EDU Ultimate A",
  subtitle="Umanoide ad alte prestazioni per ricerca AI e manipolazione avanzata, con mani dexterous Dex3 a tre dita (42 DoF). Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Ultimate A (U3): umanoide da ricerca con 42 gradi di libertà e mani Dex3 a tre dita, Jetson Orin NX 100 TOPS. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Ultimate A integra le mani dexterous Dex3 a tre dita (7 DoF per mano) su polsi e vita articolati, per un totale di 42 gradi di libertà. Computing NVIDIA Jetson Orin NX 16GB (100 TOPS), LiDAR 3D MID-360 e depth camera RealSense D435i.",
  imgdir="g1-u3",
  hands_full="Mani Dex3 a 3 dita con polsi", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="42", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","3 DoF"),("Polsi (×2)","3 DoF"),("Mani Dex3 (×2)","7 DoF ciascuna"),("Sensori tattili","No")],
  visual_p1="G1 EDU Ultimate A porta la manipolazione a tre dita: le mani Dex3, con 7 DoF ciascuna, afferrano e manipolano oggetti di forma complessa, mentre i 42 gradi di libertà totali offrono una piattaforma completa per la ricerca su manipolazione e interazione.",
  features=[("Mani Dex3 a 3 dita","7 DoF per mano per prese di precisione e manipolazione di oggetti di forma complessa."),
            ("42 gradi di libertà","Gambe, braccia, vita, polsi e mani articolate: piattaforma completa per ricerca su manipolazione e HRI."),
            ("AI a bordo","NVIDIA Jetson Orin NX 16GB (100 TOPS) con LiDAR MID-360 e RealSense D435i per percezione e controllo.")],
)
V["g1-u4"] = dict(
  title="Unitree G1 EDU Ultimate B", unum="U4", short="G1 EDU Ultimate B",
  subtitle="La piattaforma G1 per manipolazione fine: mani Dex3-1 a tre dita con sensori tattili (42 DoF). Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Ultimate B (U4): umanoide da ricerca con 42 gradi di libertà e mani Dex3-1 tattili a tre dita, Jetson Orin NX 100 TOPS. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Ultimate B monta le mani Dex3-1 a controllo di forza con sensori tattili integrati: feedback di contatto per la manipolazione fine, su una piattaforma a 42 gradi di libertà. Computing NVIDIA Jetson Orin NX 16GB (100 TOPS), LiDAR 3D MID-360 e RealSense D435i.",
  imgdir="g1-u4",
  hands_full="Mani Dex3-1 a 3 dita con sensori tattili", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="42", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","3 DoF"),("Polsi (×2)","3 DoF"),("Mani Dex3-1 (×2)","7 DoF ciascuna"),("Sensori tattili","Sì (sulle mani)")],
  visual_p1="G1 EDU Ultimate B aggiunge il senso del tatto: le mani Dex3-1 a controllo di forza, con sensori tattili integrati, restituiscono il feedback di contatto necessario alla manipolazione fine e alla ricerca su grasping adattivo.",
  features=[("Mani Dex3-1 tattili","Tre dita a controllo di forza con sensori tattili: feedback di contatto per manipolazione fine e grasping adattivo."),
            ("Manipolazione di precisione","42 DoF totali con polsi e vita articolati per traiettorie complesse e prese stabili."),
            ("AI a bordo","NVIDIA Jetson Orin NX 16GB (100 TOPS) con LiDAR MID-360 e RealSense D435i per percezione e controllo.")],
)
V["g1-u5"] = dict(
  title="Unitree G1 EDU Ultimate C", unum="U5", short="G1 EDU Ultimate C",
  subtitle="Massima destrezza con mani Inspire a 5 dita tattili (RH56DFQ): per interazione uomo-robot e task del mondo reale (40 DoF). Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Ultimate C (U5): umanoide da ricerca con 40 gradi di libertà e mani Inspire a 5 dita tattili RH56DFQ, Jetson Orin NX 100 TOPS. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Ultimate C integra le mani Inspire a 5 dita tattili (RH56DFQ): manipolazione antropomorfa con feedback tattile su una piattaforma a 40 gradi di libertà. Computing NVIDIA Jetson Orin NX 16GB (100 TOPS), LiDAR 3D MID-360 e RealSense D435i.",
  imgdir="g1-u5",
  hands_full="Mani Inspire a 5 dita tattili (RH56DFQ)", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="40", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","3 DoF"),("Polsi (×2)","3 DoF"),("Mani Inspire (×2)","6 DoF · 12 giunti ciascuna"),("Sensori tattili","Sì (integrati)")],
  visual_p1="G1 EDU Ultimate C porta la manipolazione antropomorfa: le mani Inspire a 5 dita, con sensori tattili integrati e 12 giunti per mano, riproducono prese e gesti umani per la ricerca su HRI e su task del mondo reale.",
  features=[("Mani Inspire a 5 dita","Manipolazione antropomorfa con 12 giunti e sensori tattili per prese e gesti umani."),
            ("Interazione uomo-robot","40 DoF totali con vita e polsi articolati per ricerca su HRI e manipolazione naturale."),
            ("AI a bordo","NVIDIA Jetson Orin NX 16GB (100 TOPS) con LiDAR MID-360 e RealSense D435i per percezione e controllo.")],
)
V["g1-u6"] = dict(
  title="Unitree G1 EDU Ultimate D", unum="U6", short="G1 EDU Ultimate D",
  subtitle="Il top della serie G1 EDU: mani Inspire a 5 dita tattili di fascia alta (RH56DFTP) per la ricerca più avanzata (40 DoF). Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Ultimate D (U6): top di gamma con 40 gradi di libertà e mani Inspire a 5 dita tattili RH56DFTP, Jetson Orin NX 100 TOPS. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Ultimate D è il top della serie EDU: mani Inspire a 5 dita tattili di fascia alta (RH56DFTP) con feedback tattile evoluto, su una piattaforma a 40 gradi di libertà. Computing NVIDIA Jetson Orin NX 16GB (100 TOPS), LiDAR 3D MID-360 e RealSense D435i.",
  imgdir="g1-u6",
  hands_full="Mani Inspire a 5 dita tattili (RH56DFTP)", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="40", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","3 DoF"),("Polsi (×2)","3 DoF"),("Mani Inspire (×2)","6 DoF · 12 giunti ciascuna"),("Sensori tattili","Sì (fascia alta)")],
  visual_p1="G1 EDU Ultimate D è la configurazione di punta: le mani Inspire RH56DFTP portano il feedback tattile a un livello superiore, per la ricerca più avanzata su manipolazione fine, destrezza e interazione uomo-robot.",
  features=[("Mani Inspire RH56DFTP","Cinque dita con feedback tattile di fascia alta: il massimo della destrezza nella serie G1 EDU."),
            ("Top della gamma EDU","40 DoF totali e la dotazione di manipolazione più avanzata per la ricerca di frontiera."),
            ("AI a bordo","NVIDIA Jetson Orin NX 16GB (100 TOPS) con LiDAR MID-360 e RealSense D435i per percezione e controllo.")],
)
V["g1-u7"] = dict(
  title="Unitree G1 EDU Ultimate E", unum="U7", short="G1 EDU Ultimate E",
  subtitle="Il set completo G1 EDU Plus con mani BrainCo a 5 dita dexterous (Revo 2): destrezza antropomorfa per la ricerca (40 DoF). Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Ultimate E (U7): umanoide da ricerca con 40 gradi di libertà e mani BrainCo Revo 2 a 5 dita, Jetson Orin NX 100 TOPS. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Ultimate E abbina il set completo EDU Plus alle mani BrainCo Revo 2 a 5 dita dexterous (6 DoF, 11 giunti per mano): destrezza antropomorfa su una piattaforma a 40 gradi di libertà. Computing NVIDIA Jetson Orin NX 16GB (100 TOPS), LiDAR 3D MID-360 e RealSense D435i.",
  imgdir="g1-u7",
  hands_full="Mani BrainCo Revo 2 a 5 dita (Basic)", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="40", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","3 DoF"),("Polsi (×2)","3 DoF"),("Mani BrainCo (×2)","6 DoF · 11 giunti ciascuna"),("Forza di presa","50 N · pinch 15 N")],
  visual_p1="G1 EDU Ultimate E monta le mani BrainCo Revo 2 a 5 dita: 6 DoF e 11 giunti per mano, forza di presa fino a 50 N e ripetibilità di 0,1°, per una destrezza antropomorfa al servizio della ricerca.",
  features=[("Mani BrainCo Revo 2","Cinque dita, 6 DoF e 11 giunti per mano: 50 N di forza di presa e ripetibilità 0,1°."),
            ("Set completo EDU Plus","40 DoF totali con vita e polsi articolati, su computing da ricerca a bordo."),
            ("AI a bordo","NVIDIA Jetson Orin NX 16GB (100 TOPS) con LiDAR MID-360 e RealSense D435i per percezione e controllo.")],
)
V["g1-u8"] = dict(
  title="Unitree G1 EDU Ultimate F", unum="U8", short="G1 EDU Ultimate F",
  subtitle="Mani BrainCo Revo 2 Touch a 5 dita con sensori tattili: pressione, attrito e prossimità per manipolazione fine (40 DoF). Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 EDU Ultimate F (U8): umanoide da ricerca con 40 gradi di libertà e mani BrainCo Revo 2 Touch tattili, Jetson Orin NX 100 TOPS. Distributore ufficiale Unitree in Italia.",
  desc="G1 EDU Ultimate F monta le mani BrainCo Revo 2 Touch a 5 dita con sensori tattili: rilevamento di pressione, attrito, direzione e prossimità per la manipolazione fine. Piattaforma a 40 gradi di libertà, computing NVIDIA Jetson Orin NX 16GB (100 TOPS), LiDAR 3D MID-360 e RealSense D435i.",
  imgdir="g1-u8",
  hands_full="Mani BrainCo Revo 2 Touch a 5 dita (tattili)", computing_full="8-core CPU + NVIDIA Jetson Orin NX 16GB (100 TOPS)",
  arm="~3 kg", knee="120 N·m",
  dof_total="40", dof_rows=[("Gamba (×2)","6 DoF ciascuna"),("Braccio (×2)","5 DoF ciascuno"),("Vita","3 DoF"),("Polsi (×2)","3 DoF"),("Mani BrainCo Touch (×2)","6 DoF · 11 giunti ciascuna"),("Sensori tattili","Sì (pressione/attrito/prossimità)")],
  visual_p1="G1 EDU Ultimate F è la configurazione tattile completa: le mani BrainCo Revo 2 Touch rilevano pressione, attrito, direzione e prossimità, restituendo al robot il senso del contatto necessario alla manipolazione fine e alla ricerca su grasping.",
  features=[("Mani BrainCo Revo 2 Touch","Cinque dita con sensori tattili: pressione, attrito, direzione e prossimità per manipolazione fine."),
            ("Feedback di contatto","40 DoF totali con percezione tattile: la dotazione ideale per ricerca su grasping e manipolazione adattiva."),
            ("AI a bordo","NVIDIA Jetson Orin NX 16GB (100 TOPS) con LiDAR MID-360 e RealSense D435i per percezione e controllo.")],
)
V["g1-comp"] = dict(
  title="Unitree G1 Comp", unum="", short="G1 Comp",
  subtitle="L'umanoide atletico di Unitree per competizioni robotiche e sfide ad alta dinamica: testa articolata e velocità oltre i 2 m/s. Distribuito in Italia da Abra Robotics.",
  metadesc="Unitree G1 Comp: umanoide atletico per competizioni robotiche (calcio robotico), testa articolata, velocità >2 m/s, coppia 120 N·m. Distributore ufficiale Unitree in Italia.",
  desc="G1 Comp è la piattaforma atletica di Unitree, pensata per le competizioni robotiche e le sfide ad alta dinamica come il calcio robotico. Testa articolata a 2 DoF, velocità oltre i 2 m/s, coppia al ginocchio di 120 N·m e depth camera Intel RealSense D455. Computing 8-core CPU, con NVIDIA Jetson Orin NX (100 TOPS) opzionale.",
  imgdir="g1-comp",
  hands_full="Mani dummy con polsi (aggiornabili)", computing_full="8-core CPU · NVIDIA Jetson Orin NX 16GB (100 TOPS) opzionale",
  arm="—", knee="120 N·m", speed=">2 m/s", warranty="12 mesi", depthcam="Intel RealSense D455", sviluppo="Opzionale",
  dof_total="25", dof_rows=[("Testa","2 DoF"),("Braccio (×2)","5 DoF ciascuno"),("Gamba (×2)","6 DoF ciascuna"),("Vita","1 DoF"),("Mani","0 DoF (dummy con polsi)"),("DoF opzionali","+2")],
  visual_p1="G1 Comp è costruito per il movimento: testa articolata a 2 DoF per il tracking, velocità oltre i 2 m/s e controllo dinamico per le competizioni robotiche e il calcio robotico. La depth camera RealSense D455 e il LiDAR 3D integrato gestiscono la percezione ad alta dinamica.",
  features=[("Velocità oltre 2 m/s","L'unico G1 con velocità rated oltre i 2 m/s: pensato per le sfide atletiche e il calcio robotico."),
            ("Testa articolata","2 DoF alla testa per il tracking di palla e avversari durante le competizioni."),
            ("Computing scalabile","8-core CPU con NVIDIA Jetson Orin NX (100 TOPS) opzionale e depth camera RealSense D455 per la percezione ad alta dinamica.")],
)

# ── defaults ──
for c, d in V.items():
    d.setdefault("speed", "2 m/s")
    d.setdefault("weight", "35+ kg" if c != "g1" else "35 kg")
    d.setdefault("warranty", "18 mesi")
    d.setdefault("depthcam", "Intel RealSense D435i")
    d.setdefault("sviluppo", "Sì")
    d["code"] = c
    d["cmp"] = COMPACT[c]


def esc(s): return s

def neighbors(code):
    i = LINEUP.index(code)
    prev = LINEUP[i-1] if i > 0 else None
    nxt = LINEUP[i+1] if i < len(LINEUP)-1 else None
    # ensure exactly 3 cards: shift window at the ends
    if prev is None: trio = [LINEUP[0], LINEUP[1], LINEUP[2]]
    elif nxt is None: trio = [LINEUP[-3], LINEUP[-2], LINEUP[-1]]
    else: trio = [prev, code, nxt]
    return trio

# ── HTML fragment builders ──
def key_specs(d):
    items = [
      (d["speed"].split()[0], d["speed"].split()[1] if " " in d["speed"] else "", "Velocità max"),
      (d["dof_total"], "", "Gradi libertà"),
      ("~2", "ore", "Autonomia"),
      (d["weight"].split()[0], d["weight"].split()[1] if " " in d["weight"] else "", "Peso"),
      ("132", "cm", "Altezza"),
      (d["knee"].split()[0], "N·m", "Coppia ginocchio"),
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
    items = [d["title"], f'{d["dof_total"]} Gradi di Libertà', f'{d["speed"]} velocità',
             'LiDAR 3D LIVOX MID-360', d["hands_full"], d["computing_full"].split(" + ")[-1].split(" · ")[0],
             f'Garanzia {d["warranty"]}', 'Distributore ufficiale Italia']
    one = "\n        ".join(f'<span class="marquee-text">{t}</span><span class="marquee-dot">●</span>' for t in items)
    return one

def stats(d):
    if d["code"] == "g1-comp":
        s = [("25","","Gradi di libertà totali"),("120","N·m","Coppia max ginocchio"),("2","ore","Autonomia batteria")]
    else:
        s = [(d["dof_total"],"","Gradi di libertà totali"),("100","TOPS","Potenza Jetson Orin NX"),("2","ore","Autonomia batteria")]
    out = []
    for target, unit, label in s:
        u = f'<span class="stat-unit">{unit}</span>' if unit else ""
        out.append(f'''        <div class="product-stat">
          <span class="stat-number"><span class="counter" data-target="{target}">0</span>{u}</span>
          <span class="stat-label">{label}</span>
        </div>''')
    return "\n".join(out)

def included(d):
    comp_short = "Jetson Orin NX" if d["code"] not in ("g1-comp",) else "CPU + Jetson opz."
    cards = [("Robot", d["short"]), ("Mani", d["hands_full"].replace("Mani ","")),
             ("Computing", comp_short), ("Alimentazione", "Batteria × 1"),
             ("Copertura", f'Garanzia {d["warranty"]}')]
    out = []
    for label, name in cards:
        out.append(f'''        <div class="included-card">
          <span class="included-card-label">{label}</span>
          <span class="included-card-name">{name}</span>
        </div>''')
    return "\n".join(out)

def dof_table(d):
    rows = [f'              <tr><td>DoF totali</td><td>{d["dof_total"]}</td></tr>']
    for k, v in d["dof_rows"]:
        rows.append(f'              <tr><td>{k}</td><td>{v}</td></tr>')
    return "\n".join(rows)

def specs_accordion(d):
    tactile = d["cmp"]["tactile"]
    tactile_full = {"Sì":"Sì (integrati nelle mani)","—":"Non inclusi","Opz.":"Opzionali","No":"No"}.get(tactile, tactile)
    return f'''          <details class="faq-item" open>
            <summary>Hardware — Telaio e dimensioni</summary>
            <table class="specs-table">
              <tr><td>Altezza in piedi</td><td>1.320 mm</td></tr>
              <tr><td>Larghezza × Profondità</td><td>450 × 200 mm</td></tr>
              <tr><td>Dimensioni ripiegato</td><td>690 × 450 × 300 mm</td></tr>
              <tr><td>Peso totale</td><td>{d["weight"]} (batteria inclusa)</td></tr>
              <tr><td>Materiali</td><td>Lega di alluminio + plastica tecnica ad alta resistenza</td></tr>
              <tr><td>Coscia + polpaccio</td><td>0,6 m</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Performance</summary>
            <table class="specs-table">
              <tr><td>Velocità max</td><td>{d["speed"]}</td></tr>
              <tr><td>Coppia max ginocchio</td><td>{d["knee"]}</td></tr>
              <tr><td>Carico max braccia</td><td>{d["arm"]}</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Meccanica — Gradi di libertà e articolazioni</summary>
            <table class="specs-table">
{dof_table(d)}
              <tr><td>Motori</td><td>PMSM rotore interno bassa inerzia</td></tr>
              <tr><td>Cuscinetti</td><td>Rulli incrociati industriali</td></tr>
              <tr><td>Encoder</td><td>Doppio per giunto</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Computing e sviluppo</summary>
            <table class="specs-table">
              <tr><td>Unità di calcolo</td><td>{d["computing_full"]}</td></tr>
              <tr><td>Sviluppo secondario</td><td>{d["sviluppo"]}</td></tr>
              <tr><td>CPU</td><td>8-core</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Batteria e alimentazione</summary>
            <table class="specs-table">
              <tr><td>Capacità</td><td>9.000 mAh litio 13S</td></tr>
              <tr><td>Autonomia</td><td>~2 ore</td></tr>
              <tr><td>Caricatore</td><td>54V / 5A</td></tr>
              <tr><td>Sgancio rapido</td><td>Sì</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Sensori e mani</summary>
            <table class="specs-table">
              <tr><td>LiDAR 3D</td><td>LIVOX MID-360</td></tr>
              <tr><td>Depth camera</td><td>{d["depthcam"]}</td></tr>
              <tr><td>Mani</td><td>{d["hands_full"]}</td></tr>
              <tr><td>Sensori tattili</td><td>{tactile_full}</td></tr>
            </table>
          </details>

          <details class="faq-item">
            <summary>Audio, connettività e sistema</summary>
            <table class="specs-table">
              <tr><td>Microfoni</td><td>4 con cancellazione rumore/eco</td></tr>
              <tr><td>Speaker</td><td>5W stereo</td></tr>
              <tr><td>Wi-Fi / Bluetooth</td><td>Wi-Fi 6 / BT 5.2</td></tr>
              <tr><td>Telecomando</td><td>Incluso</td></tr>
              <tr><td>OTA update</td><td>Sì</td></tr>
              <tr><td>Raffreddamento</td><td>Aria locale</td></tr>
              <tr><td>Garanzia</td><td>{d["warranty"]}</td></tr>
            </table>
          </details>'''

def parallax(d, imgs):
    caps = [(f'{d["dof_total"]} DoF', "Gradi di libertà totali"),
            (d["weight"], "Peso totale con batteria"),
            (d["speed"], "Velocità massima"),
            (d["knee"], "Coppia massima ginocchio")]
    p = imgs
    return f'''          <div class="parallax-col-a" id="parallax-col-a">
            <div class="parallax-img-wrap">
              <img src="{p[0]}" alt="{d['short']} struttura e articolazioni" loading="lazy">
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
              <img src="{p[3 if len(p)>3 else 0]}" alt="{d['short']} dettaglio sensori" loading="lazy">
              <div class="parallax-caption"><span class="parallax-caption-value">{caps[3][0]}</span><span class="parallax-caption-label">{caps[3][1]}</span></div>
            </div>
          </div>'''

def features(d):
    th = ["assets/thumbs/thumb-01.jpg","assets/thumbs/thumb-02.jpg","assets/thumbs/thumb-03.jpg"]
    vd = ["assets/videos/vid-01.mp4","assets/videos/vid-02.mp4","assets/videos/vid-03.mp4"]
    out = []
    for i,(h,p) in enumerate(d["features"]):
        out.append(f'''        <div class="feature-card">
          <div class="feature-video-wrap">
            <video class="feature-video" muted loop playsinline preload="none" data-src="{vd[i]}"></video>
            <img class="feature-video-poster" src="{th[i]}" alt="{h} {d['short']}">
          </div>
          <h3>{h}</h3>
          <p>{p}</p>
        </div>''')
    return "\n".join(out)

def gallery_thumbs(d, imgs):
    out = []
    for i, src in enumerate(imgs):
        active = " active" if i == 0 else ""
        out.append(f'            <div class="gallery-thumb{active}" data-index="{i}"><img src="{src}" alt="{d["short"]} vista {i+1}"></div>')
    return "\n".join(out)

def comp_cards(code):
    trio = neighbors(code)
    out = []
    for c in trio:
        cd = COMPACT[c]
        cur = " current" if c == code else ""
        out.append(f'''        <div class="comp-model-card{cur}">
          <span class="comp-model-name">{cd["short"]}</span>
          <span class="comp-model-tag">{cd["tag"]}</span>
        </div>''')
    return "\n".join(out), trio

def comp_table(code, trio):
    def cells(key):
        return "".join(f'<td>{COMPACT[c][key]}</td>' for c in trio)
    def linkrow():
        tds = []
        for c in trio:
            if c == code:
                tds.append('<td style="padding:16px;"><a href="#form" class="btn btn-primary btn-card">Richiedi info</a></td>')
            else:
                tds.append(f'<td style="padding:16px;"><a href="{COMPACT[c]["file"]}" class="btn btn-secondary btn-card">Vedi scheda</a></td>')
        return "".join(tds)
    return f'''        <table class="comp-table">
          <colgroup><col><col><col><col></colgroup>
          <tbody>
            <tr class="comp-section-row"><td colspan="4">Mani e manipolazione</td></tr>
            <tr><td>Tipo mani</td>{cells("hands")}</tr>
            <tr><td>Sensori tattili</td>{cells("tactile")}</tr>
            <tr class="comp-section-row"><td colspan="4">Performance e computing</td></tr>
            <tr><td>DoF totali</td>{cells("dof")}</tr>
            <tr><td>Coppia ginocchio</td>{cells("knee")}</tr>
            <tr><td>Computing</td>{cells("computing")}</tr>
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
            wrap_open = '<div style="border:1px solid var(--black);border-radius:var(--radius);overflow:hidden;">'
            btn = '<a href="#form" class="btn btn-primary" style="width:100%;justify-content:center;display:flex;">Richiedi info</a>'
        else:
            head = f'<div style="background:var(--gray-50);padding:20px 16px;border-bottom:1px solid var(--gray-200);"><span style="display:block;font-family:var(--font);font-size:1rem;font-weight:700;color:var(--black);margin-bottom:4px;">{cd["short"]}</span><span style="font-size:0.78rem;color:var(--gray-400);">{cd["tag"]}</span></div>'
            wrap_open = '<div style="border:1px solid var(--gray-200);border-radius:var(--radius);overflow:hidden;">'
            btn = f'<a href="{cd["file"]}" class="btn btn-secondary" style="width:100%;justify-content:center;display:flex;">Vedi scheda</a>'
        out.append(f'''        {wrap_open}
          {head}
          <div style="background:var(--white);">
            <div class="cmr"><span>Mani</span><span>{cd["hands"]}</span></div>
            <div class="cmr"><span>DoF totali</span><span>{cd["dof"]}</span></div>
            <div class="cmr"><span>Tattile</span><span>{cd["tactile"]}</span></div>
            <div class="cmr"><span>Computing</span><span>{cd["computing"]}</span></div>
            <div class="cmr" style="border-bottom:none;"><span>Garanzia</span><span>{cd["warranty"]}</span></div>
          </div>
          <div style="padding:16px;background:var(--white);border-top:1px solid var(--gray-100);">{btn}</div>
        </div>''')
    return "\n".join(out)

def spec_mini(d):
    items = [(d["dof_total"],"","Gradi di libertà"),(d["speed"].split()[0],d["speed"].split()[1] if " " in d["speed"] else "","Velocità massima"),
             (d["knee"].split()[0],"N·m","Coppia ginocchio"),("~2","ore","Autonomia batteria"),
             (d["weight"].split()[0],d["weight"].split()[1] if " " in d["weight"] else "","Peso totale"),("132","cm","Altezza"),
             ("MID-360","big","LiDAR 3D"),(d["depthcam"].split()[-1],"big","Depth Camera"),
             ("Jetson Orin NX" if d["code"]!="g1-comp" else "CPU + Jetson","big","Computing")]
    out = []
    for val, unit, label in items:
        if unit == "big":
            out.append(f'''        <div class="spec-mini-card">
          <span class="spec-mini-value" style="font-size:1.1rem;">{val}</span>
          <span class="spec-mini-label">{label}</span>
        </div>''')
        else:
            u = f' <small style="font-size:1rem;font-weight:600">{unit}</small>' if unit else ""
            out.append(f'''        <div class="spec-mini-card">
          <span class="spec-mini-value">{val}{u}</span>
          <span class="spec-mini-label">{label}</span>
        </div>''')
    return "\n".join(out)

# ── Page template ──
TEMPLATE = open(os.path.join(BASE, "_template.html"), encoding="utf-8").read()

def variant_imgs(imgdir: str, n: int = 5) -> list[str]:
    out = []
    for i in range(1, n + 1):
        base = f'assets/variants/{imgdir}/img-0{i}'
        if i == 1:
            out.append(f'{base}.png')
        else:
            out.append(f'{base}.jpg')
    return out


def render(code):
    d = V[code]
    n = 5
    imgs = variant_imgs(d["imgdir"], n)
    cards, trio = comp_cards(code)
    title_full = d["title"] + (f' ({d["unum"]})' if d["unum"] else "")
    repl = {
      "%%LANG_TITLE%%": f'{title_full} — Robot Umanoide | Abra Robotics',
      "%%METADESC%%": d["metadesc"],
      "%%FILENAME%%": d["cmp"]["file"],
      "%%COLLECTION_FILE%%": "umanoidi.html",
      "%%COLLECTION_NAME%%": "Umanoidi",
      "%%COMP_LABEL%%": "Gamma G1",
      "%%COMP_RANGE%%": "gamma G1",
      "%%BADGE%%": "Robot Umanoide" + (f" · {d['unum']}" if d["unum"] else ""),
      "%%TITLE%%": title_full,
      "%%SUBTITLE%%": d["subtitle"],
      "%%KEYSPECS%%": key_specs(d),
      "%%DESC%%": d["desc"],
      "%%MARQUEE%%": marquee(d),
      "%%STATS%%": stats(d),
      "%%INCLUDED%%": included(d),
      "%%SPECS_ACCORDION%%": specs_accordion(d),
      "%%GALLERY_MAIN%%": imgs[0],
      "%%GALLERY_MAIN_ALT%%": f'{title_full} — Robot Umanoide',
      "%%GALLERY_THUMBS%%": gallery_thumbs(d, imgs),
      "%%VISUAL_P1%%": d["visual_p1"],
      "%%PARALLAX%%": parallax(d, imgs),
      "%%FEATURES%%": features(d),
      "%%FEATURES_INTRO%%": f'Le capacità chiave di {d["short"]} — pronte all\'uso.',
      "%%COMP_CARDS%%": cards,
      "%%COMP_TABLE%%": comp_table(code, trio),
      "%%COMP_MOBILE%%": comp_mobile(code, trio),
      "%%SPEC_MINI%%": spec_mini(d),
      "%%FORM_PRODUCT%%": title_full,
      "%%BUY_AREA%%": buy_area(d["cmp"]["file"]),
      "%%PRODUCT_SCHEMA%%": schema(d["cmp"]["file"], title_full, d["metadesc"], imgs[0]),
      "%%SITE_NAV%%": render_site_nav("../"),
    }
    html = TEMPLATE
    for k, v in repl.items():
        html = html.replace(k, v)
    out = os.path.join(BASE, d["cmp"]["file"])
    open(out, "w", encoding="utf-8").write(html)
    return d["cmp"]["file"]

if __name__ == "__main__":
    for code in ["g1-u1","g1-u2","g1-u3","g1-u4","g1-u5","g1-u6","g1-u7","g1-u8","g1-comp"]:
        print("written", render(code))
