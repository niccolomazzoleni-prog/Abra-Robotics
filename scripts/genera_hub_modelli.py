#!/usr/bin/env python3
"""Pagine hub per famiglia di modello Unitree (IT + EN), generate dal listino pubblico.

Obiettivo SEO: essere la pagina di riferimento tra i venditori per le ricerche
"unitree <modello> prezzo/price/preis/kaufen", versioni (EDU, Air, Pro, W) e specifiche.
- Prezzi e versioni: listini/pubblico/end-user.json (unica fonte, prezzi End-User IVA esclusa).
- Specifiche: SOLO dati ufficiali Unitree (FAMILIES[*]["specs"]), con link alla fonte.
- Header, menu e footer copiati da umanoidi.html / en/umanoidi-en.html (stesso sito, stesso consenso cookie).
Idempotente. Uso: python3 scripts/genera_hub_modelli.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from genera_correlati import label  # noqa: E402
from nomi_en import nome_en  # noqa: E402

SITE = "https://abrarobotics.com"
CAL = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF"

# Famiglie: prefissi del primo token del nome a listino (dopo "UNITREE").
FAMILIES = {
    "g1": {
        "name": "G1", "prefixes": ["G1", "G1-E"], "it_page": "g1.html", "en_page": "en/g1-en.html",
        "seo_it": "Unitree G1 prezzo: da {low} €, Basic, Pro, EDU, Ultimate", "seo_en": "Unitree G1 price: Basic, Pro, EDU U1-U10, Ultimate",
        "image": "images/official/unitree-g1-02.webp", "parent_it": "umanoidi.html", "parent_en": "en/umanoidi-en.html",
        "type_it": "Robot umanoide", "type_en": "Humanoid robot",
        "source": "https://www.unitree.com/g1/",
        "specs": [("Dimensioni in piedi", "Standing dimensions", "1320 × 450 × 200 mm"), ("Peso", "Weight", "circa 35 kg|about 35 kg"),
                  ("Gradi di libertà (G1)", "Degrees of freedom (G1)", "23"), ("Coppia max ginocchio", "Max knee torque", "90 N·m (G1), 120 N·m (EDU)"),
                  ("Carico braccio", "Arm payload", "circa 2 kg (G1), 3 kg (EDU)|about 2 kg (G1), 3 kg (EDU)"),
                  ("Batteria", "Battery", "9000 mAh"), ("Autonomia", "Battery life", "circa 2 ore|about 2 hours")],
        "choose_it": [("G1 Air", "per dimostrazioni, eventi e attività di comunicazione: è la versione con meno gradi di libertà e senza sviluppo software con SDK."),
                      ("G1 EDU (U1–U10)", "per ricerca e sviluppo: aggiunge sviluppo software (SDK), coppia al ginocchio di 120 N·m, carico braccio di 3 kg e, nelle versioni superiori, mani destre."),
                      ("G1-D", "se il compito è la manipolazione su banco o in reparto: busto dual-arm su piantana o base mobile, vedi la famiglia G1-D.")],
        "choose_en": [("G1 Air", "for demos, events and marketing: fewer degrees of freedom and no custom software development."),
                      ("G1 EDU (U1–U10)", "for research and development: custom software development (SDK), 120 N·m knee torque, 3 kg arm payload and, in higher versions, dexterous hands."),
                      ("G1-D", "for bench or shop-floor manipulation: dual-arm torso on a fixed stand or mobile base, see the G1-D family.")],
        "what_it": "Il G1 cammina, si rialza, esegue movimenti dimostrativi dall'app Unitree e, nelle versioni EDU, si programma via SDK per ricerca su locomozione, manipolazione e apprendimento.",
        "what_en": "The G1 walks, gets up, performs demo motions from the Unitree app and, in EDU versions, can be programmed via SDK for research on locomotion, manipulation and learning.",
    },
    "go2": {
        "name": "Go2", "prefixes": ["GO2", "GO2-W", "GO2-X"], "it_page": "go2.html", "en_page": "en/go2-en.html",
        "image": "images/prodotti/go2-edu-smart.webp", "parent_it": "quadrupedi.html", "parent_en": "en/quadrupedi-en.html",
        "type_it": "Cane robot quadrupede", "type_en": "Quadruped robot dog",
        "source": "https://www.unitree.com/go2/",
        "specs": [("Dimensioni in piedi", "Standing dimensions", "70 × 31 × 40 cm"), ("Peso", "Weight", "circa 15 kg|about 15 kg"),
                  ("Velocità max", "Max speed", "2,5 m/s (Air), 3,5 m/s (Pro), 3,7 m/s fino a ~5 m/s (EDU)|2.5 m/s (Air), 3.5 m/s (Pro), 3.7 m/s up to ~5 m/s (EDU)"),
                  ("Carico", "Payload", "≈7 kg (Air), ≈8 kg (Pro, EDU), max ~12 kg (EDU)"),
                  ("Batteria", "Battery", "8000 mAh"), ("Autonomia", "Battery life", "circa 1–2 ore|about 1–2 hours"),
                  ("LiDAR", "LiDAR", "4D LiDAR super grandangolare|Super-wide-angle 4D LiDAR")],
        "choose_it": [("Go2 Air", "per avvicinarsi ai quadrupedi e per eventi: è la versione d'ingresso."),
                      ("Go2 Pro", "più veloce e con più carico dell'Air, per uso dimostrativo avanzato."),
                      ("Go2 EDU", "per sviluppo e ricerca: sviluppo software con SDK, prestazioni più alte e configurazioni con LiDAR aggiuntivi."),
                      ("Go2-W", "versione con ruote alle zampe, per superfici lunghe e piane.")],
        "choose_en": [("Go2 Air", "entry-level version for getting started with quadrupeds and for events."),
                      ("Go2 Pro", "faster and with more payload than the Air, for advanced demos."),
                      ("Go2 EDU", "for development and research: custom software development, higher performance and configurations with extra LiDARs."),
                      ("Go2-W", "wheeled-leg version for long, flat surfaces.")],
        "what_it": "Il Go2 è un quadrupede compatto: cammina e corre su terreni vari, segue la persona, si controlla da app e telecomando; le versioni EDU si programmano per ricerca, ispezione e didattica.",
        "what_en": "The Go2 is a compact quadruped: it walks and runs on varied terrain, follows its user and is controlled via app and remote; EDU versions are programmable for research, inspection and education.",
    },
    "r1": {
        "name": "R1", "prefixes": ["R1"], "exclude": ["R1-A", "R1-D"], "it_page": "r1.html", "en_page": "en/r1-en.html",
        "image": "images/official/unitree-r1-01.webp", "parent_it": "umanoidi.html", "parent_en": "en/umanoidi-en.html",
        "type_it": "Robot umanoide", "type_en": "Humanoid robot",
        "source": "https://www.unitree.com/R1/",
        "specs": [("Dimensioni", "Dimensions", "1230 × 357 × 190 mm"), ("Peso", "Weight", "circa 27 kg (Air), circa 29 kg (R1, EDU)|about 27 kg (Air), about 29 kg (R1, EDU)"),
                  ("Gradi di libertà", "Degrees of freedom", "20 (Air), 26 (R1, EDU)"), ("Autonomia", "Battery life", "circa 1 ora|about 1 hour"),
                  ("Calcolo", "Computing", "processore 8 core|8-core processor"), ("Telecamere", "Cameras", "monoculare (Air), binoculare (R1, EDU)|monocular (Air), binocular (R1, EDU)")],
        "seo_it": "Unitree R1 prezzo: Air, Basic, EDU U1-U6, Professional",
        "seo_en": "Unitree R1 price: Air, Basic, EDU U1-U6, Professional",
        "choose_it": [("R1 Air", "la versione più semplice: 20 gradi di libertà, senza vita e testa motorizzate, nessuno sviluppo software con SDK."),
                      ("R1 Basic", "26 gradi di libertà con vita e testa mobili, telecamera binoculare; nessuno sviluppo software con SDK."),
                      ("R1 Edu Standard (R1-U1)", "sviluppo software con SDK di alto e basso livello, modulo AI 40 TOPS incluso, interfaccia Isaac Sim, garanzia 12 mesi."),
                      ("R1 Edu Smart (R1-U2)", "come la Edu Standard ma con base di espansione da 100 TOPS."),
                      ("R1 Edu Professional A–H (A–D = R1-U3…U6)", "Edu Smart con mani: A/B Dex3-1 (B tattile), C/D BrainCo Revo 2 (D tattile), E/F Linker Hand O6 (F tattile), G pinze Dex1-1, H mani Dex2/5.")],
        "choose_en": [("R1 Air", "the simplest version: 20 degrees of freedom, no motorised waist or head, no custom software development."),
                      ("R1 Basic", "26 degrees of freedom with movable waist and head, binocular camera; no custom software development."),
                      ("R1 Edu Standard (R1-U1)", "high- and low-level custom software development, 40 TOPS AI module included, Isaac Sim interface, 12-month warranty."),
                      ("R1 Edu Smart (R1-U2)", "like the Edu Standard but with a 100 TOPS expansion dock."),
                      ("R1 Edu Professional A–H (A–D = R1-U3…U6)", "Edu Smart with hands: A/B Dex3-1 (B tactile), C/D BrainCo Revo 2 (D tactile), E/F Linker Hand O6 (F tactile), G Dex1-1 grippers, H Dex2/5 hands.")],
        "what_it": "L'R1 è l'umanoide bipede più compatto e accessibile di Unitree: adatto a didattica, laboratori, dimostrazioni e sviluppo di base.",
        "what_en": "The R1 is Unitree's most compact and affordable biped humanoid: suited to education, labs, demos and entry-level development.",
    },
    "r1-d": {
        "name": "R1-D", "prefixes": ["R1-A5", "R1-A7", "R1-A", "R1A-D"], "it_page": "r1-d.html", "en_page": "en/r1-d-en.html",
        "image": "images/prodotti/2026/famiglia-r1-a.png", "parent_it": "umanoidi.html", "parent_en": "en/umanoidi-en.html",
        "type_it": "Umanoide a doppio braccio", "type_en": "Dual-arm humanoid",
        "source": "https://www.unitree.com/mobile/R1-D/",
        "seo_it": "Unitree R1-D e R1-A prezzo: A5, A7, Smart, Ultimate | Abra",
        "seo_en": "Unitree R1-D and R1-A price: A5, A7, Smart, Ultimate | Abra",
        "specs": [("Struttura", "Layout", "busto a doppio braccio su base fissa (R1-A5, R1-A7) o su chassis mobile con colonna (versioni -D)|dual-arm torso on a fixed base (R1-A5, R1-A7) or on a mobile chassis with lifting column (-D versions)"),
                  ("Bracci", "Arms", "5 DoF per braccio (A5), 7 DoF per braccio (A7); carico circa 2 kg per braccio|5 DoF per arm (A5), 7 DoF per arm (A7); about 2 kg payload per arm"),
                  ("Gradi di libertà", "Degrees of freedom", "13 (A5) / 17 (A7) di serie; 16 / 20 nelle versioni -D (colonna + chassis), più le dita delle mani|13 (A5) / 17 (A7) standard; 16 / 20 on -D versions (column + chassis), plus hand DoF"),
                  ("Peso", "Weight", "circa 11 kg (A5), 13 kg (A7), circa 30 kg le versioni -D|about 11 kg (A5), 13 kg (A7), about 30 kg for -D versions"),
                  ("Calcolo", "Computing", "CPU 8 core + 10 TOPS nella testa; Smart con base 40 TOPS, Ultimate con base 100 TOPS|8-core CPU + 10 TOPS in the head; Smart adds a 40 TOPS dock, Ultimate a 100 TOPS dock"),
                  ("Autonomia", "Battery life", "circa 1,5 ore (batteria busto o batteria chassis per le -D)|about 1.5 hours (upper-body battery, or chassis battery on -D)"),
                  ("Garanzia", "Warranty", "12 mesi|12 months")],
        "choose_it": [("R1-A5 / R1-A7 Standard", "solo busto con bracci da 5 o 7 DoF, senza pinze né calcolo aggiuntivo: la base per integrare i propri end effector."),
                      ("R1-A5 / R1-A7 Smart A–H", "con base di calcolo 40 TOPS e telecamere da polso; A = pinze Dex1-1 Plus, B/C mani Dex3-1, D/E BrainCo Revo 2, F/G Linker Hand O6, H mani Dex2/5 (C, E, G tattili)."),
                      ("Versioni -D (R1-A5-D, R1-A7-D)", "lo stesso busto su chassis mobile con colonna e LiDAR: per manipolazione in movimento."),
                      ("R1-A5-D / R1-A7-D Ultimate A–H", "le versioni mobili con base di calcolo 100 TOPS, con le stesse opzioni di mani delle Smart.")],
        "choose_en": [("R1-A5 / R1-A7 Standard", "torso only with 5- or 7-DoF arms, no grippers or extra computing: the base for your own end effectors."),
                      ("R1-A5 / R1-A7 Smart A–H", "with a 40 TOPS dock and wrist cameras; A = Dex1-1 Plus grippers, B/C Dex3-1 hands, D/E BrainCo Revo 2, F/G Linker Hand O6, H Dex2/5 hands (C, E, G tactile)."),
                      ("-D versions (R1-A5-D, R1-A7-D)", "the same torso on a mobile chassis with lifting column and LiDAR, for mobile manipulation."),
                      ("R1-A5-D / R1-A7-D Ultimate A–H", "the mobile versions with a 100 TOPS dock and the same hand options as Smart.")],
        "what_it": "L'R1-D (configurazioni R1-A a listino) è il busto umanoide a doppio braccio di Unitree, su base fissa o su chassis mobile: pensato per manipolazione bimanuale, ricerca su embodied AI e dimostrazioni industriali leggere.",
        "what_en": "The R1-D (R1-A configurations in the price list) is Unitree's dual-arm humanoid torso, on a fixed base or a mobile chassis: built for bimanual manipulation, embodied-AI research and light industrial demos.",
    },
    "a2": {
        "name": "A2", "prefixes": ["A2", "A2-W"], "it_page": "a2.html", "en_page": "en/a2-en.html",
        "image": "images/official/unitree-a2-02.webp", "parent_it": "quadrupedi.html", "parent_en": "en/quadrupedi-en.html",
        "type_it": "Quadrupede industriale", "type_en": "Industrial quadruped",
        "source": "https://www.unitree.com/A2/",
        "specs": [("Peso", "Weight", "circa 42 kg con batteria|about 42 kg with battery"),
                  ("Carico", "Payload", "circa 100 kg da fermo, circa 25 kg in camminata continua|about 100 kg standing, about 25 kg continuous walking"),
                  ("Velocità max", "Max speed", "0–3,7 m/s (fino a ~5 m/s)|0–3.7 m/s (up to ~5 m/s)"),
                  ("Autonomia", "Endurance", "oltre 5 ore senza carico (circa 20 km)|over 5 hours unloaded (about 20 km)"),
                  ("Protezione", "Protection", "IP56 (A2), IP56–IP67 (A2 Pro)"),
                  ("Sensori", "Sensors", "1 LiDAR + telecamera HD (A2), 2 LiDAR + telecamera HD (A2 Pro)|1 LiDAR + HD camera (A2), 2 LiDAR + HD camera (A2 Pro)")],
        "choose_it": [("A2 Standard", "quadrupede industriale per ispezione e trasporto leggero, IP56."),
                      ("A2 Pro", "due LiDAR e componenti principali IP67, per ambienti più gravosi."),
                      ("A2-W", "versione con ruote per percorsi lunghi su superfici regolari.")],
        "choose_en": [("A2 Standard", "industrial quadruped for inspection and light transport, IP56."),
                      ("A2 Pro", "two LiDARs and IP67 core components for harsher environments."),
                      ("A2-W", "wheeled version for long routes on regular surfaces.")],
        "what_it": "L'A2 è un quadrupede industriale per ispezioni, sorveglianza e trasporto in impianti, con lunga autonomia e protezione dagli agenti esterni.",
        "what_en": "The A2 is an industrial quadruped for inspection, surveillance and transport in plants, with long endurance and environmental protection.",
    },
    "b2": {
        "name": "B2", "prefixes": ["B2", "B2-W", "B2W"], "seo_it": "Unitree B2 e B2-W prezzo Italia: da {low} €", "it_page": "b2.html", "en_page": "en/b2-en.html",
        "image": "images/official/unitree-b2-montagna.webp", "parent_it": "quadrupedi.html", "parent_en": "en/quadrupedi-en.html",
        "type_it": "Quadrupede industriale pesante", "type_en": "Heavy industrial quadruped",
        "source": "https://www.unitree.com/b2/",
        "specs": [("Peso", "Weight", "≈60 kg con batteria|≈60 kg with battery"),
                  ("Carico", "Payload", "≥120 kg da fermo, >40 kg in camminata|≥120 kg standing, >40 kg walking"),
                  ("Velocità max", "Max speed", "> 6 m/s"), ("Batteria", "Battery", "45 Ah (2250 Wh), 58 V"),
                  ("Autonomia", "Endurance", "oltre 5 ore senza carico, oltre 20 km|over 5 hours unloaded, over 20 km"),
                  ("Protezione", "Protection", "IP67")],
        "choose_it": [("B2", "quadrupede pesante su zampe per ispezione industriale, terreni difficili e carichi elevati."),
                      ("B2-W", "versione con ruote, più efficiente su lunghe distanze; disponibile anche come kit di conversione.")],
        "choose_en": [("B2", "heavy legged quadruped for industrial inspection, rough terrain and high payloads."),
                      ("B2-W", "wheeled version, more efficient over long distances; also available as a conversion kit.")],
        "what_it": "Il B2 è il quadrupede industriale più robusto di Unitree: ispezione di impianti, ambienti esterni e trasporto di carichi.",
        "what_en": "The B2 is Unitree's most rugged industrial quadruped: plant inspection, outdoor environments and payload transport.",
    },
    "z1": {
        "name": "Z1 e D1", "name_en": "Z1 and D1", "prefixes": ["Z1", "D1", "D1-T"], "it_page": "z1.html", "en_page": "en/z1-en.html",
        "image": "images/official/unitree-z1-01.webp", "parent_it": "accessori.html", "parent_en": "en/accessori-en.html",
        "type_it": "Braccio robotico", "type_en": "Robot arm", "seo_it": "Unitree Z1 prezzo: bracci robotici Z1 e D1", "seo_en": "Unitree Z1 price: Z1 and D1 robot arms",
        "source": "https://www.unitree.com/z1/", "source2": "https://www.unitree.com/D1-T/",
        "specs": [("Z1: assi", "Z1: axes", "6"), ("Z1: peso", "Z1: weight", "4,3 kg (Air), 4,5 kg (Pro)|4.3 kg (Air), 4.5 kg (Pro)"),
                  ("Z1: carico", "Z1: payload", "2 kg (Air), ≥3 kg (Pro)"), ("Z1: sbraccio", "Z1: reach", "740 mm"),
                  ("Z1: ripetibilità", "Z1: repeatability", "~0,1 mm|~0.1 mm"),
                  ("D1: assi", "D1: axes", "6 + pinza|6 + gripper"), ("D1: carico", "D1: payload", "500 g"), ("D1: sbraccio", "D1: reach", "550 mm (670 mm con pinza)|550 mm (670 mm with gripper)")],
        "choose_it": [("Z1 Air", "braccio a 6 assi da 2 kg, anche da montare su quadrupede."),
                      ("Z1 Pro", "stesso sbraccio, carico di almeno 3 kg."),
                      ("D1 / D1-T", "braccio leggero da 500 g; il D1-T è il kit di teleoperazione con due bracci.")],
        "choose_en": [("Z1 Air", "6-axis arm with 2 kg payload, also mountable on a quadruped."),
                      ("Z1 Pro", "same reach, payload of at least 3 kg."),
                      ("D1 / D1-T", "lightweight 500 g payload arm; D1-T is the dual-arm teleoperation kit.")],
        "what_it": "Z1 e D1 sono i bracci robotici Unitree per manipolazione leggera, ricerca e montaggio su robot mobili.",
        "what_en": "Z1 and D1 are Unitree's robot arms for light manipulation, research and mounting on mobile robots.",
    },
    # Solo EN: le pagine italiane esistono gia' (as2.html, h2.html, g1-d.html).
    "as2": {
        "name": "AS2", "prefixes": ["AS2", "AS2-W", "AS2-X"], "it_page": "as2.html", "en_page": "en/as2-en.html", "en_only": True,
        "image": "images/prodotti/2026/as2.png", "parent_en": "en/quadrupedi-en.html",
        "type_en": "Quadruped robot", "source": "https://www.unitree.com/As2/",
        "specs": [("", "Weight", "|approx. 20 kg with battery"),
                  ("", "Max speed", "|0–3.0 m/s (Air), 0–3.7 m/s (Pro), 0–3.7 m/s up to ~5 m/s (X, EDU)"),
                  ("", "Walking payload", "|approx. 10 kg (Air), 13 kg (Pro), 15 kg (X, EDU)"),
                  ("", "Endurance", "|~2 h (Air), ~4 h (Pro, X, EDU) unloaded"), ("", "Protection", "|IP54 (Pro, X, EDU); no IP rating declared for Air"),
                  ("", "LiDAR", "|Unitree L2 (Air), industrial 64–128-line LiDAR (Pro, X, EDU)")],
        "choose_en": [("AS2 Air", "entry version with HD camera, for demos and getting started."),
                      ("AS2 Pro / X", "industrial 64–128-line LiDAR, IP54 and about 4 h endurance."),
                      ("AS2 EDU", "for development: industrial LiDAR and custom software development."),
                      ("AS2-W", "wheeled version.")],
        "what_en": "The AS2 is Unitree's new-generation mid-size quadruped, between Go2 and A2, for research, inspection and demos.",
    },
    "h2": {
        "name": "H2", "prefixes": ["H2", "H2-D", "H2-A"], "it_page": "h2.html", "en_page": "en/h2-en.html", "en_only": True,
        "image": "images/official/unitree-h2-01.webp", "parent_en": "en/umanoidi-en.html",
        "type_en": "Full-size humanoid robot", "source": "https://www.unitree.com/H2/",
        "specs": [("", "Dimensions", "|1820 × 456 × 218 mm"), ("", "Weight", "|about 70 kg"), ("", "Degrees of freedom", "|31"),
                  ("", "Battery life", "|about 3 hours"), ("", "Max joint torque", "|360 N·m (leg), 120 N·m (arm)"),
                  ("", "Computing", "|Intel Core i5, optional Intel Core i7")],
        "choose_en": [("H2 Air", "full-size humanoid for demos and showrooms."),
                      ("H2 EDU", "for research and development with custom software development."),
                      ("H2-D / H2-A", "dual-arm torso versions for manipulation.")],
        "what_en": "The H2 is Unitree's full-size humanoid (about 1.8 m), for research, advanced demos and human-scale tasks.",
    },
    "g1-d": {
        "name": "G1-D", "prefixes": ["G1-D", "G1D"], "it_page": "g1-d.html", "en_page": "en/g1-d-en.html", "en_only": True,
        "image": "images/official/unitree-g1-d-mobile.webp", "parent_en": "en/umanoidi-en.html",
        "type_en": "Wheeled dual-arm humanoid", "source": "https://www.unitree.com/G1-D/",
        "specs": [("", "Type", "|wheeled dual-arm humanoid, differential drive, 360° in-place rotation"),
                  ("", "Degrees of freedom", "|17 (Standard), 19 (Ultimate), excl. end effector; 7 per arm"),
                  ("", "Single-arm payload", "|approx. 3 kg"), ("", "Height", "|1260–1680 mm (adjustable column)"),
                  ("", "Weight", "|approx. 90 kg incl. battery"), ("", "Base speed", "|1.5 m/s"),
                  ("", "Battery life", "|approx. 2 h (Standard), approx. 6 h (Ultimate)")],
        "choose_en": [("G1-D Standard", "fixed stand or base, 17 DOF, about 2 h battery."),
                      ("G1-D Flagship / Ultimate", "mobile base, 19 DOF, about 6 h battery.")],
        "what_en": "The G1-D is a dual-arm humanoid torso on a fixed stand or mobile base, built for manipulation tasks on benches and shop floors.",
    },
}


# Testi guida delle pagine hub (solo IT). Fatti: specifiche ufficiali Unitree gia' nel generatore,
# listino pubblico, servizio Abra. Niente nomi di concorrenti, niente prezzi scritti a mano (sono in tabella).
GUIDE_IT = {
"go2": [
 ("Go2 Air, Pro, EDU, Go2-X e Go2-W: le differenze in pratica", [
  "Tutte le versioni del Go2 condividono lo stesso corpo da circa 15 kg, la batteria da 8000 mAh e il LiDAR 4D super grandangolare di serie. Cambiano tre cose: la potenza dei motori (quindi velocità e carico), la possibilità di programmare il robot e i sensori aggiuntivi.",
  "Il Go2 Air è la versione d'ingresso: si comanda da app, segue la persona ed è pensato per eventi, comunicazione e primo contatto con i quadrupedi. Il Go2 Pro aggiunge prestazioni più alte (fino a 3,5 m/s e circa 8 kg di carico) e funzioni vocali e di interazione più complete.",
  "Le versioni Go2 EDU sono le uniche aperte allo sviluppo software con SDK: SDK ufficiale Unitree, accesso ai sensori e al controllo di basso livello, calcolo NVIDIA Jetson a bordo. Si distinguono per i sensori: Standard, Smart, Plus con LiDAR Livox Mid-360 e Ultimate con LiDAR Hesai XT16 per la mappatura 3D di precisione.",
  "Il Go2-W monta ruote all'estremità delle zampe: cammina come un Go2 ma su superfici piane si sposta rotolando, con meno consumo e più velocità. È disponibile nelle configurazioni U1–U5, dalla Standard alla Inspection con gimbal."]),
 ("A cosa serve un Unitree Go2", [
  "Ricerca e università: è la piattaforma quadrupede più diffusa nei laboratori di locomozione e reinforcement learning, grazie al prezzo contenuto e all'ecosistema software (unitree_sdk2, ROS 2, simulazione in Isaac Sim e MuJoCo).",
  "Didattica e scuole: con l'app e la programmazione grafica si usa per corsi di robotica, STEM e laboratori; le versioni EDU permettono di passare poi a Python e C++.",
  "Ispezione leggera e sicurezza: le versioni con LiDAR e telecamere servono per sopralluoghi, mappatura di ambienti e controlli ripetitivi in spazi dove un robot su ruote non passa. Per carichi o ambienti industriali gravosi conviene guardare l'<a href=\"a2.html\">Unitree A2</a> o il <a href=\"b2.html\">B2</a>.",
  "Eventi e comunicazione: il Go2 Air e il Pro sono i modelli più usati per fiere, showroom e attività marketing."]),
 ("Go2 o un altro quadrupede Unitree?", [
  "Il Go2 è il quadrupede compatto: leggero, facile da trasportare, ideale per sviluppo e ambienti interni. L'<a href=\"as2.html\">AS2</a> è la fascia intermedia, più robusta e con più autonomia. L'<a href=\"a2.html\">A2</a> e il <a href=\"b2.html\">B2</a> sono quadrupedi industriali con protezione IP, carichi molto più alti e diverse ore di autonomia. Il confronto completo è nella pagina <a href=\"quadrupedi.html\">robot quadrupedi Unitree</a>."]),
 ("Comprare un Unitree Go2 in Italia con Abra Robotics", [
  "I prezzi in tabella sono End-User IVA esclusa, con spedizione e dazio in Italia già inclusi: nessun costo doganale a sorpresa. Prima dell'ordine ti aiutiamo a scegliere versione e accessori in base all'uso reale e verifichiamo gratuitamente se l'acquisto rientra in <a href=\"finanziamenti.html\">iperammortamento, Nuova Sabatini o bandi regionali</a>.",
  "Fattura italiana, consegna in Italia, Svizzera e Balcani, supporto in italiano per messa in servizio e primi passi con l'SDK."]),
],
"a2": [
 ("Unitree A2: un quadrupede pensato per l'industria", [
  "L'A2 nasce per lavorare in impianti, cantieri e aree esterne: pesa circa 42 kg, porta circa 25 kg in camminata continua (circa 100 kg da fermo) e cammina oltre 5 ore senza carico, coprendo circa 20 km con una carica. La protezione IP56, IP67 sui componenti principali della versione Pro, gli permette di lavorare con polvere e pioggia.",
  "A differenza dei quadrupedi compatti come il <a href=\"go2.html\">Go2</a>, l'A2 è progettato per missioni ripetute e lunghe: giri di ispezione programmati, sorveglianza perimetrale, trasporto di strumenti e sensori."]),
 ("A2 Standard, A2 Pro o A2-W?", [
  "L'A2 Standard ha un LiDAR e una telecamera HD: è la scelta per ispezioni e trasporto leggero in ambienti già mappati. L'A2 Pro aggiunge un secondo LiDAR e protezione IP67 dei componenti principali, per ambienti più gravosi e percezione più completa intorno al robot.",
  "Le versioni A2-W hanno ruote all'estremità delle zampe: su strade, piazzali e corridoi lunghi si muovono rotolando, più veloci e con meno consumo, mantenendo la capacità di salire scale e ostacoli."]),
 ("Applicazioni tipiche dell'A2", [
  "Ispezione di impianti (energia, oil & gas, chimico, acque): letture di strumenti, termografia e rilevamento di anomalie lungo percorsi ripetuti.",
  "Sicurezza e sorveglianza: ronde notturne e controllo perimetrale con telecamere e LiDAR.",
  "Logistica leggera in esterno: trasporto di attrezzature e campioni dove non arrivano carrelli o AMR su ruote.",
  "Per carichi ancora maggiori e velocità oltre 6 m/s c'è il <a href=\"b2.html\">Unitree B2</a>; per un quadrupede di fascia intermedia l'<a href=\"as2.html\">AS2</a>. Il confronto è nella pagina <a href=\"quadrupedi.html\">robot quadrupedi Unitree</a>."]),
 ("Comprare un Unitree A2 in Italia", [
  "Prezzi End-User IVA esclusa, spedizione e dazio in Italia inclusi. Per un progetto industriale partiamo da una call sul percorso di ispezione o sul compito da svolgere, poi definiamo versione, accessori (batterie di ricambio, telecomando G20, modulo UWB) e verifichiamo gli incentivi disponibili nella pagina <a href=\"finanziamenti.html\">Finanziamenti</a>."]),
],
"g1": [
 ("G1 Air, G1 Pro, G1 EDU, G1-Comp: come orientarsi", [
  "Il G1 è l'umanoide bipede di Unitree alto circa 1,32 m e pesante circa 35 kg. Le versioni si distinguono per gradi di libertà, coppia ai motori, calcolo a bordo e mani.",
  "Il G1 Air (Basic) ha 23 gradi di libertà, mani fisse e nessuno sviluppo software con SDK: è pensato per dimostrazioni ed eventi. Il G1 Pro aggiunge funzioni di intrattenimento e interazione. Il G1-Comp è la versione atletica per competizioni.",
  "Le versioni G1 EDU (codici Unitree G1-U1 … U10) sono quelle per ricerca e sviluppo: SDK di alto e basso livello, NVIDIA Jetson Orin a bordo, coppia al ginocchio di 120 N·m e carico al braccio di circa 3 kg. Salendo di codice si aggiungono vita e polsi articolati e mani dexterous: Dex3-1 a tre dita (anche tattile), Inspire e BrainCo a cinque dita."]),
 ("Quale G1 EDU per il tuo laboratorio", [
  "Locomozione e controllo del corpo intero: G1 EDU Standard (U1) o Plus (U2, vita e polsi articolati).",
  "Manipolazione e apprendimento per imitazione: le Ultimate con mani Dex3-1 (U3, U4 tattile) o a cinque dita (Inspire, BrainCo) per afferrare oggetti reali.",
  "Raccolta dati per AI fisica e teleoperazione: valuta anche il <a href=\"g1-d.html\">G1-D</a>, il busto dual-arm su piantana o base mobile pensato proprio per la manipolazione."]),
 ("Programmare il G1", [
  "Unitree pubblica su GitHub l'SDK ufficiale (unitree_sdk2), il pacchetto ROS 2 e i modelli per la simulazione in Isaac Sim e MuJoCo: si sviluppa la politica in simulazione e la si porta sul robot reale. Approfondimenti nella <a href=\"blog/unitree-g1-programmazione.html\">guida alla programmazione del G1</a> e nel confronto <a href=\"blog/unitree-g1-quale-versione-scegliere.html\">quale versione del G1 scegliere</a>."]),
 ("Comprare un Unitree G1 in Italia", [
  "Prezzi End-User IVA esclusa con spedizione e dazio in Italia inclusi, fattura italiana, supporto in italiano. Per università ed enti di ricerca prepariamo offerte e documentazione per gare pubbliche; per le imprese verifichiamo gli <a href=\"finanziamenti.html\">incentivi</a>. Altri umanoidi: <a href=\"r1.html\">Unitree R1</a> (più compatto) e <a href=\"h2.html\">H2</a> (full-size)."]),
],
"r1": [
 ("Unitree R1: l'umanoide compatto per iniziare", [
  "L'R1 è alto circa 1,23 m e pesa circa 29 kg: è l'umanoide bipede più accessibile di Unitree. Cammina, corre, esegue movimenti dinamici e acrobatici, e nella versione EDU è completamente programmabile.",
  "Le versioni: R1 Air (20 gradi di libertà, senza vita e testa motorizzate), R1 Basic (26 gradi di libertà, telecamera binoculare), R1 EDU Standard (R1-U1) con SDK per lo sviluppo software e modulo AI da 40 TOPS, R1 EDU Smart (R1-U2) con base da 100 TOPS, e le R1 EDU Professional (R1-U3 … U6 e oltre) con mani Dex3-1, BrainCo Revo 2 o Linker Hand."]),
 ("R1 o G1?", [
  "L'R1 costa molto meno del <a href=\"g1.html\">G1</a> ed è più piccolo e leggero: è la scelta giusta per didattica, laboratori universitari, corsi su locomozione e reinforcement learning, dimostrazioni. Il G1 ha motori più potenti, più gradi di libertà nelle versioni alte e più opzioni di mani: è la piattaforma per la ricerca su manipolazione e AI fisica."]),
 ("Programmare l'R1 EDU", [
  "Le versioni EDU danno accesso allo sviluppo di alto e basso livello con l'SDK Unitree e all'interfaccia per la simulazione in Isaac Sim: si addestra in simulazione e si trasferisce sul robot. Per il busto a doppio braccio su base fissa o mobile c'è la famiglia <a href=\"r1-d.html\">R1-D / R1-A</a>."]),
 ("Comprare un Unitree R1 in Italia", [
  "Prezzi End-User IVA esclusa, spedizione e dazio in Italia inclusi, fattura italiana e supporto in italiano. Per scuole, università ed enti pubblici prepariamo offerte e documentazione per gare pubbliche; per le imprese verifichiamo gli <a href=\"finanziamenti.html\">incentivi</a>."]),
],
"b2": [
 ("Unitree B2: il quadrupede industriale per carichi e ambienti difficili", [
  "Il B2 pesa circa 60 kg, regge almeno 120 kg da fermo e oltre 40 kg in camminata, supera i 6 m/s e lavora oltre 5 ore senza carico grazie alla batteria da 2250 Wh. La protezione IP67 gli permette di lavorare sotto pioggia, polvere e fango.",
  "È pensato per ispezioni industriali lunghe, trasporto di strumenti pesanti, soccorso e ricerca su locomozione ad alte prestazioni, dove un quadrupede compatto come il <a href=\"go2.html\">Go2</a> non basta."]),
 ("B2 o B2-W?", [
  "Il B2 cammina su zampe ed è il più versatile su terreni accidentati, scale e macerie. Il B2-W ha ruote all'estremità delle zampe: su strade, piazzali e capannoni copre distanze lunghe più velocemente e con meno consumo, senza perdere la capacità di superare ostacoli. Esiste anche il kit di conversione a quattro ruote per trasformare un B2 in B2-W.",
  "Entrambi si ordinano anche con il kit LiDAR SLAM per la mappatura e la navigazione autonoma, e con moduli di calcolo dedicati (Intel Core i7 o NVIDIA Jetson AGX fino a 550 TOPS) per far girare a bordo visione e AI."]),
 ("B2, A2 o AS2?", [
  "L'<a href=\"a2.html\">A2</a> è il quadrupede industriale più leggero (circa 42 kg) con lunga autonomia, adatto a ronde e ispezioni ripetute. L'<a href=\"as2.html\">AS2</a> è la fascia intermedia. Il B2 è la scelta quando servono carico, velocità e robustezza massimi. Confronto completo nella pagina <a href=\"quadrupedi.html\">robot quadrupedi Unitree</a>."]),
 ("Comprare un Unitree B2 in Italia", [
  "Prezzi End-User IVA esclusa, spedizione e dazio in Italia inclusi, fattura italiana e supporto in italiano. Per i progetti industriali partiamo dal compito da svolgere (percorso, carico, ambiente) e definiamo versione, batterie di ricambio (standard, basse temperature, alta capacità) e calcolo; verifichiamo gli <a href=\"finanziamenti.html\">incentivi</a> disponibili."]),
],
"z1": [
 ("Z1 Air, Z1 Pro e D1: quale braccio scegliere", [
  "Lo Z1 è un braccio a 6 assi da circa 4,5 kg con 740 mm di sbraccio e ripetibilità di circa 0,1 mm. Lo Z1 Air porta 2 kg, lo Z1 Pro almeno 3 kg. Si ordina con pinza standard o con pinza e telecamera RealSense D405 o D435i per la presa guidata dalla visione.",
  "Il D1 è più leggero (500 g di carico, 550 mm di sbraccio, 670 mm con pinza) ed è pensato per didattica, ricerca e raccolta dati. Il D1-T è il kit di teleoperazione in stile Mobile ALOHA con due o quattro bracci D1, usato per registrare dimostrazioni e addestrare politiche di manipolazione."]),
 ("Montare il braccio su un quadrupede", [
  "Lo Z1 è pensato anche per il montaggio su robot mobili, per esempio su un quadrupede come il <a href=\"b2.html\">B2</a>: si ottiene un manipolatore mobile per aprire porte, premere pulsanti, prelevare campioni o ispezionare da vicino. Si programma con l'SDK Unitree e con ROS."]),
 ("Comprare Z1 e D1 in Italia", [
  "Prezzi End-User IVA esclusa, spedizione e dazio in Italia inclusi, fattura italiana e supporto in italiano. Per laboratori e università prepariamo offerte e documentazione per gare pubbliche; per le imprese verifichiamo gli <a href=\"finanziamenti.html\">incentivi</a>."]),
],
}


def family_of(name: str) -> str | None:
    first = name.upper().replace("UNITREE ", "").split()[0].rstrip("/") if name.strip() else ""
    best = None
    for key, f in FAMILIES.items():
        for p in f["prefixes"]:
            if first == p or (first.startswith(p) and not first[len(p):len(p) + 1].isalnum()):
                if any(first.startswith(x) for x in f.get("exclude", [])):
                    continue
                if best is None or len(p) > best[1]:
                    best = (key, len(p))
    return best[0] if best else None


def eur(x: float, en: bool) -> str:
    s = f"{x:,.0f}"
    return s if en else s.replace(",", ".")


def load() -> dict[str, dict]:
    items = json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8"))
    out: dict[str, dict] = {k: {"robots": [], "acc": []} for k in FAMILIES}
    for sku, v in items.items():
        slug = v.get("slug")
        p = ROOT / "prodotti" / (slug or "_")
        if not slug or not p.is_file() or 'http-equiv="refresh"' in p.read_text(encoding="utf-8"):
            continue
        fam = family_of(v.get("nome", ""))
        if not fam:
            continue
        # R1 / R1-D: nomi di listino così come sono (label() abbassa le lettere di variante "A", "E")
        name = v["nome"] if fam in ("r1", "r1-d") else label(v["nome"])
        # label() abbassa le lettere di variante ("Ultimate a", "G1 e"): le rimette maiuscole
        name = re.sub(r"\b(Ultimate|Professional|Smart|Standard|Plus|G1|H2|R1|Go2-W|AS2-W)\s([a-z])\b", lambda m: f"{m.group(1)} {m.group(2).upper()}", name)
        name = re.sub(r"\b(standard|smart|plus|ultimate|professional)\b", lambda m: m.group(1).capitalize(), name)
        # prezzo_su_richiesta (es. G1-PLUS): nessun prezzo, riga "su richiesta" in tabella
        row = {"sku": sku, "name": name, "price": v.get("prezzo_eur"), "slug": slug, "on_request": bool(v.get("prezzo_su_richiesta"))}
        is_robot = v.get("categoria") == "UMANOIDI"
        if fam == "z1":  # bracci: i "robot" sono i bracci, non pinze/telecamere/motori
            n = v["nome"].upper()
            is_robot = bool(re.match(r"Z1 (AIR|PRO)\b|D1 ROBOTIC ARM|D1-T", n))
        out[fam]["robots" if is_robot else "acc"].append(row)
    for f in out.values():
        f["robots"].sort(key=lambda r: (r["price"] is None, r["price"] or 0))  # "su richiesta" in fondo
        f["acc"].sort(key=lambda r: (r["price"] is None, r["price"] or 0))
    # R1-D: 52 configurazioni, ordinate per modello (A5, A7, A5-D, A7-D), livello e lettera invece che per prezzo
    base = {"R1-A5": 0, "R1-A7": 1, "R1-A5-D": 2, "R1-A7-D": 3}
    tier = {"Standard": 0, "Smart": 1, "Ultimate": 2}
    # R1: Air, Basic, Edu Standard e Smart per prezzo, poi Edu Professional A–H in ordine di lettera
    out["r1"]["robots"].sort(key=lambda r: ("Professional" in r["name"], r["name"] if "Professional" in r["name"] else "", r["price"] or 0))
    out["r1-d"]["robots"].sort(key=lambda r: (base.get(r["name"].split()[0], 9), tier.get(r["name"].split()[1], 9) if len(r["name"].split()) > 1 else 9, r["name"]))
    return out


def split(v: str, en: bool) -> str:
    if "|" in v:
        it, e = v.split("|", 1)
        return e if en else it
    return v


def template(en: bool) -> tuple[str, str, str, str]:
    """(head_prefix, style_block, body_chrome, footer) dalla pagina umanoidi della lingua."""
    s = (ROOT / ("en/umanoidi-en.html" if en else "umanoidi.html")).read_text(encoding="utf-8")
    head_prefix = s[: s.index("<title>")]
    # via i tag specifici della pagina template (canonical, hreflang, descrizione, social, JSON-LD)
    head_prefix = re.sub(r'\s*<link[^>]*(rel="canonical"|hreflang=)[^>]*>', "", head_prefix)
    head_prefix = re.sub(r'\s*<meta[^>]*(name="(description|robots|keywords)"|property="og:|name="twitter:)[^>]*>', "", head_prefix)
    head_prefix = re.sub(r'\s*<script type="application/ld\+json">[\s\S]*?</script>', "", head_prefix)
    style = re.search(r"<style>[\s\S]*?</style>", s).group(0)
    body = s[s.index("<body>"): s.index("<!-- HERO -->")]
    footer = s[s.index('<footer class="footer">'): s.index("</footer>") + len("</footer>")]
    return head_prefix, style, body, footer


HUB_CSS = """<style id="hub-modello-css">
.hm-table{width:100%;border-collapse:collapse;font-size:.95rem}
.hm-table th,.hm-table td{padding:10px 12px;border-bottom:1px solid var(--gray-200);text-align:left;vertical-align:top}
.hm-table th{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--gray-600)}
.hm-table td.p{white-space:nowrap;font-weight:700}
.hm-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.hm-specs{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:20px}
.hm-specs div{border:1px solid var(--gray-200);border-radius:var(--radius);padding:14px}
.hm-specs span{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--gray-600);margin-bottom:4px}
.hm-specs strong{font-size:1rem;line-height:1.35}
.hm-choose{display:grid;gap:12px;margin-top:20px}
.hm-choose p{margin:0;line-height:1.6}
.hm-acc{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:6px;list-style:none;padding:0;margin:20px 0 0}
.hm-acc a{display:flex;justify-content:space-between;gap:10px;padding:9px 12px;border:1px solid var(--gray-200);border-radius:8px;color:var(--black);text-decoration:none;font-size:.92rem}
.hm-acc a span{color:var(--gray-600);white-space:nowrap}
.hm-src a{color:var(--accent-text);overflow-wrap:anywhere}
.hm-faq details{border-bottom:1px solid var(--gray-200);padding:14px 0}
.hm-faq summary{font-weight:700;cursor:pointer}
.hm-faq p{margin:10px 0 0;line-height:1.6;color:var(--gray-600)}
.hm-fam{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.hm-fam a{padding:6px 12px;border:1px solid var(--gray-200);border-radius:999px;color:var(--black);text-decoration:none;font-size:.9rem}
</style>"""


def page(key: str, f: dict, data: dict, en: bool) -> str:
    pre = "../" if en else ""
    url_it = f"{SITE}/{f['it_page']}"
    url_en = f"{SITE}/{f['en_page']}"
    own = url_en if en else url_it
    name = f.get("name_en", f["name"]) if en else f["name"]
    robots, acc = data["robots"], data["acc"]
    prices = [r["price"] for r in robots if r["price"]] or [r["price"] for r in acc if r["price"]]
    low, high = (min(prices), max(prices)) if prices else (None, None)
    head_prefix, style, body, footer = template(en)

    def link(slug: str) -> str:
        if en:
            en_slug = slug.replace(".html", "-en.html")
            if (ROOT / "en/prodotti" / en_slug).is_file():
                return f"prodotti/{en_slug}"
            return f"../prodotti/{slug}"
        return f"prodotti/{slug}"

    if en:
        title = f.get("seo_en") or f"Unitree {name} price: versions and specs | Abra"
        h1 = f"Unitree {name}: price and versions in Europe"
        desc = (f"Unitree {name} price in Europe: all versions from € {eur(low, True)} excl. VAT, official specs and "
                f"which to choose. Sold in Italy by Abra Robotics.") if low else f"Unitree {name}: versions, official specs and quote from Abra Robotics."
        lead = f"{f['what_en']} Below: every {name} version we sell with its end-user price (excl. VAT), the official specifications and how to choose."
    else:
        title = (f.get("seo_it") or "").replace("{low}", eur(low, False) if low else "") or (f"Unitree {name} prezzo Italia: da {eur(low, False)} €, tutte le versioni" if low else f"Unitree {name} prezzo: versioni e specifiche | Abra")
        h1 = f"Unitree {name}: prezzi e versioni in Italia"
        desc = (f"Prezzo Unitree {name} in Italia: tutte le versioni da {eur(low, False)} € IVA esclusa, specifiche ufficiali "
                f"e quale scegliere. Spedizione e dazio inclusi, supporto in italiano.") if low else f"Unitree {name}: versioni, specifiche ufficiali e preventivo da Abra Robotics."
        lead = f"{f['what_it']} Qui trovi tutte le versioni {name} a listino con prezzo End-User (IVA esclusa), le specifiche ufficiali e come scegliere."
    if len(title) > 60:
        title = title.replace(" | Abra", "")[:60].rsplit(" ", 1)[0]
    if len(desc) > 158:  # toglie l'ultima frase intera invece di troncare a metà ("supporto in.")
        desc = desc.rsplit(". ", 1)[0].rstrip(",.") + "."

    rows = robots or acc
    th = ("Version", "Price (excl. VAT)", "") if en else ("Versione", "Prezzo (IVA esclusa)", "")
    tr = "\n".join(
        f'<tr><td><a href="{link(r["slug"])}">{html.escape(nome_en(r["name"]) if en else r["name"])}</a></td>'
        f'<td class="p">{(("on request" if en else "su richiesta") if not r["price"] else ("from € " + eur(r["price"], True)) if en else ("da " + eur(r["price"], False) + " €"))}</td>'
        f'<td><a href="{link(r["slug"])}">{"Details" if en else "Scheda"} →</a></td></tr>'
        for r in rows if r["price"] or r["on_request"])
    table = f'<div class="hm-wrap"><table class="hm-table"><thead><tr><th>{th[0]}</th><th>{th[1]}</th><th>{th[2]}</th></tr></thead><tbody>\n{tr}\n</tbody></table></div>'

    specs = "".join(f'<div><span>{html.escape(s[1] if en else s[0])}</span><strong>{html.escape(split(s[2], en))}</strong></div>'
                    for s in f["specs"] if (s[1] if en else s[0]))
    choose = "".join(f"<p><strong>{html.escape(a)}</strong>: {html.escape(b)}</p>" for a, b in f["choose_en" if en else "choose_it"])
    # Testi guida (HTML fidato, scritto qui sopra): solo pagine IT.
    guide = "" if en else "".join(
        f'<section class="section hm-guide" style="padding-top:0"><div class="container"><h2>{html.escape(h)}</h2>'
        + "".join(f"<p>{p}</p>" for p in ps) + "</div></section>\n" for h, ps in GUIDE_IT.get(key, []))
    acc_html = ""
    if robots and acc:
        acc_html = (f'<section class="section" style="padding-top:0"><div class="container"><h2>{"Accessories for" if en else "Accessori per"} Unitree {html.escape(name)}</h2>'
                    '<ul class="hm-acc">' + "".join(
                        f'<li><a href="{link(a["slug"])}">{html.escape(nome_en(a["name"]) if en else a["name"])}<span>{("from € " + eur(a["price"], True)) if en else ("da " + eur(a["price"], False) + " €")}</span></a></li>'
                        for a in acc[:24] if a["price"]) + "</ul></div></section>")

    srcs = [f["source"]] + ([f["source2"]] if f.get("source2") else [])
    if en:
        faq = [
            (f"How much does the Unitree {name} cost?", f"End-user prices for the Unitree {name} start from € {eur(low, True)} excluding VAT and go up to € {eur(high, True)} depending on the version. Prices include shipping and duty to Italy; every order is confirmed with an updated quote." if low else f"Contact us for a quote on the Unitree {name}."),
            (f"Which Unitree {name} version should I choose?", " ".join(f"{a}: {b}" for a, b in f["choose_en"])),
            (f"What can the Unitree {name} do?", f["what_en"]),
            (f"Can I buy the Unitree {name} outside Italy?", "We mainly work in Italy, Switzerland and the Balkans; other EU countries on a project basis. Contact us for delivery and a quote for your country."),
            (f"Where do the {name} specifications come from?", "From Unitree's official product page, linked in the Sources section. Actual configuration depends on the version you order."),
        ]
    else:
        faq = [
            (f"Quanto costa l'Unitree {name}?", f"I prezzi End-User dell'Unitree {name} partono da {eur(low, False)} € IVA esclusa e arrivano a {eur(high, False)} € a seconda della versione. Spedizione e dazio in Italia sono inclusi; ogni ordine si conferma con un preventivo aggiornato." if low else f"Contattaci per un preventivo sull'Unitree {name}."),
            (f"Quale versione dell'Unitree {name} scegliere?", " ".join(f"{a}: {b}" for a, b in f["choose_it"])),
            (f"Cosa fa l'Unitree {name}?", f["what_it"]),
            (f"Si può finanziare l'acquisto dell'Unitree {name}?", "Spesso sì: verifichiamo gratuitamente se il progetto rientra in iperammortamento, Nuova Sabatini o bandi regionali prima del preventivo. Dettagli nella pagina Finanziamenti."),
            (f"Consegnate l'Unitree {name} anche fuori dall'Italia?", "Lavoriamo principalmente in Italia, Svizzera e Balcani; altri paesi UE su progetto. Contattaci per tempi e preventivo."),
        ]
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)

    fam_links = "".join(
        f'<a href="{(("../" + g["en_page"].split("/", 1)[1]) if False else (g["en_page"].split("/", 1)[1] if en else g["it_page"]))}">Unitree {html.escape(g.get("name_en", g["name"]) if en else g["name"])}</a>'
        for k2, g in FAMILIES.items() if k2 != key and (en or not g.get("en_only") or (ROOT / g["it_page"]).is_file()))

    ld_product = {"@context": "https://schema.org", "@type": "Product", "name": f"Unitree {name}", "brand": {"@type": "Brand", "name": "Unitree"},
                  "image": f"{SITE}/{f['image']}", "description": desc, "url": own}
    if low:
        ld_product["offers"] = {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": f"{low:.2f}", "highPrice": f"{high:.2f}",
                                "offerCount": len([r for r in rows if r["price"]]),
                                "seller": {"@type": "Organization", "name": "Abra Robotics", "url": SITE}}
    parent = f["parent_en"] if en else f["parent_it"]
    ld_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/{'en/index-en.html' if en else ''}"},
        {"@type": "ListItem", "position": 2, "name": parent.split("/")[-1].replace("-en.html", "").replace(".html", "").capitalize(), "item": f"{SITE}/{parent}"},
        {"@type": "ListItem", "position": 3, "name": f"Unitree {name}", "item": own}]}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld_product, ld_bc, ld_faq))

    # altre lingue (scripts/genera_lingue.py): solo se la pagina esiste gia'
    others = "".join(f'<link rel="alternate" hreflang="{ {"no": "nb"}.get(c, c)}" href="{SITE}/{c}/unitree-{key}.html"/>\n'
                     for c in ("de", "fr", "nl", "da", "sv", "no", "fi", "es", "pl", "cs") if (ROOT / c / f"unitree-{key}.html").is_file())
    hreflang = (f'<link rel="alternate" hreflang="it" href="{url_it}"/>\n<link rel="alternate" hreflang="en" href="{url_en}"/>\n'
                f'{others}<link rel="alternate" hreflang="x-default" href="{url_it}"/>')
    lang_label = ("Italiano", url_it) if en else ("English", url_en)
    sources = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{u}</a></li>' for u in srcs)
    parent_rel = parent.split("/", 1)[1] if en else parent
    cta_assess = "assessment-en.html" if en else "assessment.html"
    T = (lambda e, i: e if en else i)

    head = f"""{head_prefix}<title>{html.escape(title)}</title>
{hreflang}
<meta content="{html.escape(desc)}" name="description"/>
<meta content="index, follow" name="robots"/>
<link href="{own}" rel="canonical"/>
<link href="{pre}favicon.ico" rel="icon" sizes="any"/>
<link href="{pre}images/favicon-32x32.png" rel="icon" type="image/png" sizes="32x32"/>
<link href="{pre}images/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link rel="preload" href="/fonts/satoshi-400.woff2" as="font" type="font/woff2" crossorigin/>
<link rel="preload" href="/fonts/satoshi-700.woff2" as="font" type="font/woff2" crossorigin/>
<link href="{pre}style.css" rel="stylesheet"/>
{style}
{HUB_CSS}
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Abra Robotics"/>
<meta property="og:title" content="{html.escape(title)}"/>
<meta property="og:description" content="{html.escape(desc)}"/>
<meta property="og:url" content="{own}"/>
<meta property="og:image" content="{SITE}/{f['image']}"/>
<meta property="og:locale" content="{T('en_GB', 'it_IT')}"/>
<meta name="twitter:card" content="summary_large_image"/>
{lds}
</head>
"""
    main = f"""<!-- HERO -->
<section class="collection-hero">
<div class="container">
<p class="label"><a href="{parent_rel}" style="color:inherit">{html.escape(T(f['type_en'], f.get('type_it', '')))}</a> · <a href="{lang_label[1]}" hreflang="{T('it', 'en')}" style="color:inherit">{lang_label[0]}</a></p>
<h1>{html.escape(h1)}</h1>
<p class="lead">{html.escape(lead)}</p>
<div class="hero-meta">
<div><strong>{len([r for r in rows if r['price']])}</strong><span>{T('Versions', 'Versioni a listino')}</span></div>
{('<div><strong>' + (T('from € ' + eur(low, True), 'da ' + eur(low, False) + ' €')) + '</strong><span>' + T('excl. VAT', 'IVA esclusa') + '</span></div>') if low else ''}
<div><strong>{T('Italy', 'Italia')}</strong><span>{T('Unitree Italy distribution chain', 'Filiera di distribuzione di Unitree Italia')}</span></div>
</div>
<div class="hm-fam">{fam_links}</div>
</div>
</section>
<section class="section" style="padding-top:24px"><div class="container">
<h2>{T(f'Unitree {name} versions and prices', f'Versioni e prezzi Unitree {name}')}</h2>
<p>{T('End-user prices excluding VAT, shipping and duty to Italy included. Each order is confirmed with an updated quote.', 'Prezzi End-User IVA esclusa, spedizione e dazio in Italia inclusi. Ogni ordine si conferma con un preventivo aggiornato.')}</p>
{table}
</div></section>
<section class="section" style="padding-top:0"><div class="container">
<h2>{T(f'Which Unitree {name} should I choose?', f'Quale Unitree {name} scegliere')}</h2>
<div class="hm-choose">{choose}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
<h2>{T(f'Unitree {name} official specifications', f'Specifiche ufficiali Unitree {name}')}</h2>
<div class="hm-specs">{specs}</div>
</div></section>
{guide}{acc_html}
<section class="section section-cta"><div class="container" style="text-align:center">
<h2>{T(f'Get a quote for the Unitree {name}', f"Preventivo per l'Unitree {name}")}</h2>
<p>{T('Tell us what you need it for: we suggest the right version, accessories and financing options.', 'Raccontaci a cosa ti serve: ti indichiamo versione, accessori e possibilità di finanziamento.')}</p>
<p style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:20px"><a class="btn btn-primary" href="{cta_assess}">{T('Find the right model', 'Trova il modello giusto')}</a><a class="btn btn-secondary" href="{CAL}" target="_blank" rel="noopener noreferrer">{T('Book a call', 'Prenota una chiamata')}</a></p>
</div></section>
<section class="section hm-faq" id="faq"><div class="container"><h2>{T('Frequently asked questions', 'Domande frequenti')}</h2>{faq_html}</div></section>
<section class="section hm-src" style="padding-top:0"><div class="container"><h2>{T('Sources', 'Fonti')}</h2><ul>{sources}<li><a href="{pre}listini/pubblico/end-user.json">{T('Abra Robotics public end-user price list', 'Listino pubblico End-User Abra Robotics')}</a></li></ul></div></section>
"""
    tail = f'\n<script defer src="{pre}script.js"></script>\n</body>\n</html>\n'
    return "<!-- generato da scripts/genera_hub_modelli.py -->\n" + head + body + main + footer + tail


def add_hreflang(it_page: str, en_page: str) -> None:
    """Pagine IT esistenti (as2, h2, g1-d): hreflang verso la nuova pagina EN."""
    p = ROOT / it_page
    s = p.read_text(encoding="utf-8")
    url_it, url_en = f"{SITE}/{it_page}", f"{SITE}/{en_page}"
    s = re.sub(r'\s*<link[^>]*hreflang="(it|en|de|fr|nl|da|sv|nb|fi|es|pl|cs|x-default)"[^>]*>', "", s)
    key = next(k for k, f in FAMILIES.items() if f["it_page"] == it_page)
    others = "".join(f'<link rel="alternate" hreflang="{ {"no": "nb"}.get(c, c)}" href="{SITE}/{c}/unitree-{key}.html"/>\n'
                     for c in ("de", "fr", "nl", "da", "sv", "no", "fi", "es", "pl", "cs") if (ROOT / c / f"unitree-{key}.html").is_file())
    links = (f'\n<link rel="alternate" hreflang="it" href="{url_it}"/>\n<link rel="alternate" hreflang="en" href="{url_en}"/>\n'
             f'{others}<link rel="alternate" hreflang="x-default" href="{url_it}"/>')
    s = re.sub(r"(</title>)", r"\1" + links.replace("\\", "\\\\"), s, count=1)
    p.write_text(s, encoding="utf-8")


def link_row(page_path: str, en: bool, keys: list[str]) -> None:
    """Riga "Famiglie Unitree" dopo l'hero delle pagine categoria (tra marcatori, idempotente)."""
    p = ROOT / page_path
    s = p.read_text(encoding="utf-8")
    links = "".join(
        f'<a href="{(FAMILIES[k]["en_page"].split("/", 1)[1]) if en else FAMILIES[k]["it_page"]}">Unitree {html.escape(FAMILIES[k].get("name_en", FAMILIES[k]["name"]) if en else FAMILIES[k]["name"])}</a>'
        for k in keys)
    block = (f'<!-- HUB:MODELLI -->\n<section class="section" style="padding:8px 0 0"><div class="container">'
             f'<p class="label">{"Unitree families: prices and versions" if en else "Famiglie Unitree: prezzi e versioni"}</p>'
             f'<div class="hm-fam" style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div></section>\n<!-- /HUB:MODELLI -->')
    block = block.replace('<a href', '<a style="padding:6px 12px;border:1px solid var(--gray-200);border-radius:999px;color:var(--black);text-decoration:none;font-size:.9rem" href')
    if "<!-- HUB:MODELLI -->" in s:
        s = re.sub(r"<!-- HUB:MODELLI -->[\s\S]*?<!-- /HUB:MODELLI -->", lambda m: block, s)
    else:
        if '<section class="collection-hero">' in s:
            i = s.index('<section class="collection-hero">')
            j = s.index("</section>", i) + len("</section>")
        else:  # catalogo: hero in <header class="cat-hero">
            i = s.index('<header class="cat-hero">')
            j = s.index("</header>", i) + len("</header>")
        s = s[:j] + "\n" + block + s[j:]
    p.write_text(s, encoding="utf-8")


def seo_schede(data: dict) -> None:
    """Una sola pagina per modello su Google: le schede rimandano all'hub, gli accessori non iniziano col nome del robot."""
    for key, f in FAMILIES.items():
        if f.get("en_only"):
            continue
        hub = f["it_page"]
        for r in data[key]["robots"]:
            p = ROOT / "prodotti" / r["slug"]
            s = p.read_text(encoding="utf-8")
            if 'class="hub-link"' in s:
                continue
            a = (f'<p class="hub-link" style="margin:.4rem 0 1rem"><a href="../{hub}">'
                 f'Tutte le versioni Unitree {f["name"]} a confronto, con prezzi →</a></p>')
            s2 = re.sub(r'(<h1 class="product-title">.*?</h1>)', lambda m: m.group(1) + "\n" + a, s, count=1, flags=re.S)
            if s2 != s:
                p.write_text(s2, encoding="utf-8")
        for r in data[key]["acc"]:
            p = ROOT / "prodotti" / r["slug"]
            s = p.read_text(encoding="utf-8")
            m = re.search(r"<title>(Unitree ([A-Z0-9][\w-]*(?: / [A-Z0-9][\w-]*)?) (.+?))(( prezzo|: accessorio|, prezzo).*)?</title>", s)
            if not m or m.group(3).startswith("per "):
                continue
            rest = m.group(3)[0].upper() + m.group(3)[1:]
            new = f"{rest} per Unitree {m.group(2)}{(m.group(4) or '').replace(' prezzo', ', prezzo', 1)}"
            s = s.replace(f">{m.group(0)[7:-8]}<", f">{new}<").replace(f'"{m.group(0)[7:-8]}"', f'"{html.escape(new)}"')
            p.write_text(s, encoding="utf-8")


def main() -> None:
    data = load()
    written = []
    for key, f in FAMILIES.items():
        if not f.get("en_only"):
            (ROOT / f["it_page"]).write_text(page(key, f, data[key], en=False), encoding="utf-8")
            written.append(f["it_page"])
        (ROOT / f["en_page"]).write_text(page(key, f, data[key], en=True), encoding="utf-8")
        written.append(f["en_page"])
        if f.get("en_only"):
            add_hreflang(f["it_page"], f["en_page"])
    link_row("umanoidi.html", False, ["g1", "g1-d", "h2", "r1", "r1-d"])
    link_row("quadrupedi.html", False, ["go2", "as2", "a2", "b2"])
    link_row("accessori.html", False, ["z1"])
    link_row("catalogo-unitree.html", False, ["go2", "as2", "a2", "b2", "g1", "g1-d", "h2", "r1", "r1-d", "z1"])
    link_row("en/umanoidi-en.html", True, ["g1", "g1-d", "h2", "r1", "r1-d"])
    link_row("en/quadrupedi-en.html", True, ["go2", "as2", "a2", "b2"])
    link_row("en/catalogo-unitree-en.html", True, ["go2", "as2", "a2", "b2", "g1", "g1-d", "h2", "r1", "r1-d", "z1"])
    seo_schede(data)
    for k, f in FAMILIES.items():
        print(f"{k:5s} robot {len(data[k]['robots']):3d} accessori {len(data[k]['acc']):3d}")
    print("scritte:", " ".join(written))


if __name__ == "__main__":
    main()
