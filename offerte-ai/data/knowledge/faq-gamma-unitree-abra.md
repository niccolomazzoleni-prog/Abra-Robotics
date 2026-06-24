# Gamma Unitree — famiglie prodotto (guida Abra)

## Regola fondamentale per consulenza e quiz
**Non confrontare quadrupedi con umanoidi per task di manipolazione.** Go2, As2, A2, B2 sono **quadrupedi** (locomozione, sorveglianza, payload sensori). **Non fanno manipolazione bimanuale.**

## Quadrupedi (locomozione / sorveglianza / ispezione)
| Famiglia | Modelli Abra (listino) | Ideale per |
|----------|------------------------|------------|
| Go2 EDU | GO2-EDU-STD, GO2-EDU-SMART | Lab, ROS2, POC software, budget contenuto |
| As2 | AS2-AIR, AS2-PRO, AS2-EDU | Sorveglianza compatta IP54, payload sensori |
| A2 | A2-STD, A2-PRO | Industriale IP56/IP67, payload 25 kg |
| B2 | B2-STD, B2-WHEELED | Outdoor severo, carico pesante |

## Umanoidi bipedi — ricerca / lab (mono o dual arm su corpo bipede)
| Famiglia | Modelli Abra (listino) | DoF / note |
|----------|------------------------|------------|
| **G1** | G1-AIR, G1-U1 … G1-U10, G1-COMP | 23–43+ DoF; U2 = braccio 7 DOF; manipolazione mono-braccio |
| **R1** | R1-AIR, R1-U1 … R1-U6 | Entry umanoide; più compatto/economico del G1; ROS2 EDU |
| **H2** | H2-AIR, H2-EDU | Full-size ~180 cm, 31 DoF, top di gamma Unitree |

**H2 Plus:** al momento **non presente** nel listino End-User Abra né come scheda dedicata — verificare disponibilità Unitree / import con Abra.

## Dual-arm / deployment industriale (piantana, mobile, certificazione)
| Prodotto | In listino Abra | Note |
|----------|-----------------|------|
| **R1-D** | SKU R1-D (prezzo da confermare) | Dual-arm nativo; base fissa o mobile; manipolazione bimanuale |
| **G1-D** | **Su preventivo** (non SKU singolo) | Deployment industriale G1; piantana/gantry; pagine manifattura + LP umanoidi |

Per **pick-place scatole A→B** con **certificazione cella**: orientare verso **R1-D o G1-D montati**, non quadrupede.

## Confronti sensati (esempi)
- Sorveglianza capannone: **As2 Pro vs A2 Pro** (quadrupedi)
- Lab universitario locomozione: **G1-U1 vs R1-U1** (umanoide entry)
- Manipolazione mono-braccio: **G1-U2 vs R1-U2**
- Ricerca full-size: **H2 Air vs H2 EDU**
- Bimanuale industriale: **R1-D vs G1-D** (piantana fissa/mobile)
- **MAI** per bimanuale: Go2 EDU vs As2 Pro

## PoC — tempi indicativi Abra
- PoC integrazione listino: 12 / 22 / 35 giornate (€ 10.560 / € 19.360 / € 30.800)
- PoC industriale completo (hardware + integrazione + pilot): spesso **3–6 mesi** — dipende da task, certificazione, mount
