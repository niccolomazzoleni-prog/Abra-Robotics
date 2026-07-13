# PoC umanoidi in ambito industriale (manifattura, tessile, logistica)

## Quando ha senso un PoC umanoide in azienda
Un Proof of Concept umanoide serve a **validare un'ipotesi** prima di un investimento pieno: capire se la piattaforma regge layout, sicurezza, integrazione IT e un task reale (pick-place leggero, ispezione, campionamento, telepresenza in reparto).

Non sostituisce subito operatori o macchine specializzate: il PoC produce **dati, demo e stima ROI** per una fase 2.

## I 5 step Abra per strutturare un PoC (umanoidi)
1. **Call scoperta (gratuita)** — reparto target, vincoli di spazio/sicurezza, task da testare, KPI (es. cicli/ora, % successo pick, tempo ispezione).
2. **Scelta piattaforma** — tipicamente **G1-U1** (lab/POC software, 23 DoF) o **G1-U2** (29 DoF, braccio 7 DOF se serve manipolazione). **R1 EDU** se budget più contenuto. Hardware a listino End-User separato.
3. **Progetto PoC in laboratorio Abra** — mount payload, ROS 2 / SDK, test sicurezza e teleoperazione (fascia **base** listino integrazione).
4. **Pilot on-site (opzionale)** — 1–2 settimane in azienda con tecnici Abra, affinamento task e formazione operatori (fascia **standard** o **avanzata** + trasferte a parte).
5. **Report e preventivo fase 2** — esito PoC, roadmap verso deployment, eventuale offerta formale PDF.

Durata indicativa PoC completo: **8–14 settimane** (hardware 4–8 sett + integrazione 3–7 sett), variabile per complessità.

## Fasce economiche integrazione PoC Abra (IVA escl., solo servizi)
Tariffa ingegneria: **€ 110/ora**, giornata **8 h** (= **€ 880/giorno**). Trasferte sempre a parte.

| Fascia | Giornate | Importo indicativo | Ideale per |
|--------|----------|-------------------|------------|
| Base | 12 gg | **€ 10.560** | Driver, ROS 2 base, test in lab |
| Standard | 22 gg | **€ 19.360** | Sensori custom, test campo, sorveglianza/ispezione |
| Avanzata | 35 gg | **€ 30.800** | Perception custom, SCADA, multi-robot, formazione |

Il **robot umanoide** (es. G1-U1 da ~€ 37.562) e eventuali sensori/staffe sono **voci separate** dal listino Unitree.

## Esempio: azienda tessile / manifattura leggera
Use case tipici da esplorare in PoC (da confermare in call):
- **Ispezione qualità** su campioni tessuto (camera + AI, teleoperazione).
- **Pick-place leggero** di pezzi piccoli / campioni (richiede spesso **G1-U2** o superiore).
- **Presenza / telepresenza** in reparto per training remoto o audit sicurezza.

Abra **non vende un PoC “chiavi in mano tessile” standard**: strutturiamo il percorso sopra in base al vostro layout e KPI. Per sorveglianza/perlustrazione in capannone esistono spesso soluzioni **quadrupede (As2/A2)** più mature — valutiamo insieme quale piattaforma ha senso.

## Cosa chiediamo al cliente per quotare
- Settore, dimensioni area di test, vincoli EHS.
- Task prioritario (1–2) e peso/dimensioni oggetti.
- Livello integrazione IT (MES, SCADA, solo ROS).
- Disponibilità team interno (ROS/Python) vs supporto Abra full.

Contatto: info@abrarobotics.com · WhatsApp · preventivo formale via chat “Crea offerta”.
