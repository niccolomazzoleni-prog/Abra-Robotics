# Gamma Unitree — famiglie prodotto (guida Abra)

## Regola fondamentale per consulenza e quiz
**Non confrontare quadrupedi con umanoidi per task di manipolazione.** Go2, As2, A2, B2 sono **quadrupedi** (locomozione, sorveglianza, payload sensori). **Non fanno manipolazione bimanuale.**

## Quadrupedi (locomozione / sorveglianza / ispezione)
| Famiglia | Modelli Abra (listino) | Ideale per |
|----------|------------------------|------------|
| Go2 EDU | GO2-EDU-STD, GO2-EDU-SMART | Lab, ROS2, POC software, budget contenuto |
| As2 | AS2-AIR, AS2-PRO, AS2-EDU | Sorveglianza compatta IP54, payload sensori |
| A2 | A2-STD, A2-PRO, A2W-STD, A2W-PRO | Industriale IP56/IP67, payload 25 kg |
| B2 | B2, B2W, B2-LIDAR, B2W-LIDAR | Outdoor severo, carico pesante |

## Umanoidi — hub Abra (umanoidi.html)
| Famiglia | Modelli Abra (listino) | Tipo |
|----------|------------------------|------|
| **G1** | G1-AIR, G1-U1 … G1-U10, G1-COMP | Bipede ricerca · 23–43+ DoF |
| **G1-D** | G1D-U1 … G1D-U10 | Dual-arm su colonna · Standard fissa (U1–U5) o Flagship mobile (U6–U10) |
| **R1** | R1-AIR, R1-U1 … R1-U6 | Bipede entry · compatto · ROS2 EDU |
| **R1-D** | R1-D | Dual-arm tavolo/mobile · 15–31 DoF |
| **H2** | H2-AIR, H2-EDU | Full-size ~180 cm · 31 DoF |
| **H2 Plus** | H2-PLUS | Reference NVIDIA Isaac GR00T · preordine fine 2026 |

**G1-D ≠ G1 bipede:** G1-D è piattaforma wheeled humanoid (colonna + bracci 7×2), non cammina su gambe.

## Dual-arm / deployment industriale (piantana, mobile, certificazione)
| Prodotto | In listino Abra | Note |
|----------|-----------------|------|
| **G1-D** | G1D-U1 … G1D-U10 | Data collection AI, pick-place industriale, base fissa o mobile |
| **R1-D** | SKU R1-D (listino **da € 12.000**, `prezzo_da: true`) | Dual-arm compatto; base fissa o mobile con LiDAR |

Per **pick-place scatole A→B** con **certificazione cella**: orientare verso **R1-D o G1-D montati**, non quadrupede.

## Confronti sensati (esempi)
- Sorveglianza capannone: **As2 Pro vs A2 Pro** (quadrupedi)
- Lab universitario locomozione: **G1-U1 vs R1-U1** (umanoide entry)
- Manipolazione mono-braccio: **G1-U2 vs R1-U2**
- Ricerca full-size: **H2 Air vs H2 EDU**
- Bimanuale industriale: **R1-D vs G1-D U6–U10** (mobile) o **G1-D U1–U5** (fissa)
- Ricerca GR00T / embodied AI top: **H2 Plus** (2026)
- **MAI** per bimanuale: Go2 EDU vs As2 Pro

## PoC — tempi indicativi Abra
- PoC integrazione listino: 12 / 22 / 35 giornate (€ 10.560 / € 19.360 / € 30.800)
- PoC industriale completo (hardware + integrazione + pilot): spesso **3–6 mesi** — dipende da task, certificazione, mount
