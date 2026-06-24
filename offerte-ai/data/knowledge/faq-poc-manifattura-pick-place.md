# PoC manifattura — pick & place (scatole A→B) — scelta piattaforma

## Domanda tipica cliente
«Ho un reparto manifattura: devo spostare scatole dal punto A al punto B. Valuto G1-D, R1-D (su piantana fissa o mobile), oppure G1 bipede o H2. La piantana è più facile da certificare. Quale modello per un PoC?»

## Regola generale Abra
Per **pick-place ripetitivo in cella** la scelta dipende da tre assi:
1. **Manipolazione** — serve dual-arm (R1-D / G1-D) o basta un braccio (G1-U2+)?
2. **Mobilità** — il task è **fisso in cella** (piantana/gantry) o serve **spostarsi** tra postazioni (bipede / base mobile)?
3. **Certificazione / safety** — base **fissa** (piantana, gantry, cella caged) semplifica CE/safety rispetto a bipede libero in reparto condiviso.

## Matrice decisionale (indicativa)

| Scenario | Piattaforma consigliata | Perché |
|----------|-------------------------|--------|
| Scatole leggere (<3 kg), tray A→B, cella dedicata, priorità certificazione | **R1-D o G1-D su piantana fissa** | Workspace prevedibile, niente equilibrio dinamico, safety più lineare |
| Stesso task ma layout cambia spesso / più postazioni | **R1-D / G1-D su base mobile** (AMR o rail) | Dual-arm + spostamento senza bipede instabile in traffico |
| Pick-place singolo braccio, budget contenuto, lab/POC software | **G1-U2** (29 DoF, braccio 7 DOF) | Listino End-User chiaro, ROS 2, meno complesso di dual-arm |
| Ricerca / demo prestigio, mobilità umanoide | **G1 bipede (U2/U3+)** o **H2** | Più wow e flessibile, **peggio per certificazione rapida** in reparto produttivo condiviso |
| Solo ispezione / telepresenza, no manipolazione pesante | **G1-U1** o quadrupede se solo patrol | Non serve dual-arm |

## G1-D vs R1-D (dual-arm industrial)
- **R1-D** — dual-arm nativo Unitree, bracci 5 o 7 DoF, base fissa o mobile con LiDAR; **in listino Abra** (SKU R1-D, prezzo da confermare configurazione).
- **G1-D** — gamma deployment industriale Unitree (industrial-ready, ROS2); **configurazione su preventivo Abra** — mount, piantana e varianti non sono SKU singolo standard come G1-U1.

Per **PoC pick-place scatole** Abra orienta spesso verso **R1-D o G1-D fissi/montati** se il cliente cita esplicitamente certificazione e cella; verso **G1-U2** se budget e scope sono più contenuti.

## Piantana fissa vs mobile vs bipede libero
- **Piantana / gantry fissa** — footprint noto, limiti software hard, interlock più semplici, ideale **fase 1 PoC** in manifattura regolamentata.
- **Piantana / pedestal mobile** — stessa logica safety con area di lavoro delimitata, utile se A e B sono lontani ma il percorso è mappato.
- **Bipede libero (G1, H2)** — massima flessibilità, **non** la scelta migliore per primo PoC produttivo pick-place se la priorità è certificazione e ciclo stabile; meglio come **fase 2** dopo validazione algoritmi in lab/cella.

## Step PoC consigliati (pick-place manifattura)
1. **Brief** — peso/dimensioni scatole, distanza A→B, ciclo target, ambiente (umido/polvere?), vincoli safety.
2. **Scelta architettura** — dual-arm montato vs mono-arm vs bipede (tabella sopra).
3. **PoC lab Abra** — grasping, vision, cycle time in mockup (fascia base ~€ 10.560).
4. **Pilot in cella** — mount/piantana, interlock, 1–2 settimane on-site (fascia standard ~€ 19.360 + trasferte).
5. **Report** — KPI raggiunti, roadmap verso produzione o stop/go.

Durata indicativa: **10–16 settimane** (hardware 4–8 sett + integrazione).

## Cosa chiedere al cliente prima di quotare
- Peso max scatola e formato (L×W×H)
- Distanza A→B e se il layout cambia
- Requisito **CE / safety** e presenza operatori nel raggio
- Preferenza **fissa vs mobile vs bipede**
- Budget indicativo hardware + integrazione

## Preventivo formale
Chiedere: «preventivo PoC pick-place manifattura con R1-D e G1-U2 a confronto» — la chat genera offerta con alternative robot + PoC a € 110/h.
