# Direzione E: panel acquirenti, round 1

Materiali guardati come li vedrebbe un acquirente: `applicazioni/hero.png`, `preventivo-cover.png`, `preventivo-interna.png`, `linkedin-sacmi.png`, `linkedin-anonimo.png`, `reel-g1.png`, `totem.png`. Nessun documento di razionale letto prima.

## Le tre voci

### (a) Prof.ssa Rinaldi, laboratorio universitario
- **5 secondi**: "Un robot con il metro accanto, misure e limiti dichiarati. Interessante."
- **Fiducia**: 7/10. Il post con ingombro, LiDAR e l'elenco di sei voci (simulatore, digital twin, manuale, repository, assistenza) è utile per il mio confronto tra offerte.
- **La farebbe chiamare**: la scheda misure del G1 con "Esempio" accanto ai valori non verificati.
- **La farebbe esitare**: "L'imbastitura", "Il modello", "pezzo di carta": parole da sartoria che in un laboratorio di robotica non hanno senso. Nessun cenno a ROS 2 o ai tempi di consegna.
- **Voto**: 7

### (b) Ing. Ferrari, direttore operations
- **5 secondi**: "Prova prima di investire, a fasi. Il metro giallo mi ricorda il nastro di sicurezza del reparto."
- **Fiducia**: 7/10. La pagina interna è forte: calendario a settimane, criteri, costi, "Se ti fermi dopo una fase" ti restano report, video e codice, "anche con un altro fornitore". Il riquadro "Cosa il robot non farà" con la pinza su braccio collaborativo è un segnale di onestà.
- **Lo farebbe chiamare**: la frase sul fornitore alternativo; il totale con IVA esclusa e P0 senza costo.
- **Lo farebbe esitare**: la copertina del preventivo. Riquadri sagomati come cartamodelli, linee tratteggiate, una diagonale gialla che attraversa tutto: non capisco l'ordine delle fasi né perché P0 e P1 siano fuse. In riunione investimenti questa pagina va spiegata.
- **Voto**: 7

### (c) Giulia Conti, event manager
- **5 secondi**: "Noleggio a giornata con un tecnico accanto, e c'è perfino la pianta dello stand."
- **Fiducia**: 7/10. La pianta 300 × 300 cm con posizione del tecnico e distanza dal pubblico risponde a domande che l'allestitore mi farebbe.
- **La farebbe chiamare**: "Scegli la data" con mail e indirizzo web in fascia gialla.
- **La farebbe esitare**: il reel è credibile ma poco scenico; il G1 è dentro un ritaglio di carta su fondo antracite, nessuna persona.
- **Voto**: 7

## Criteri

| Criterio | Voto | Motivazione |
|-|-|-|
| 1. Voto lab | 7 | Misure e contenuti giusti, lessico sartoriale estraneo alla ricerca. |
| 2. Voto operations | 7 | Interna da 8, copertina confusa che va spiegata. |
| 3. Voto event manager | 7 | Totem con pianta dello stand utile, reel poco scenico. |
| 4. Credibilità B2B | 7 | Metro, limiti e "anche con un altro fornitore" rassicurano; i tagli sagomati alleggeriscono troppo. |
| 5. Chiarezza dell'offerta | 7 | Hero chiaro; i nomi delle fasi ("le misure", "l'imbastitura", "il modello") oscurano il metodo. |

**Voto complessivo: 7,0**

## I 3 problemi più gravi
1. La metafora sartoriale entra nel copy ("imbastitura", "il modello", "cartamodello") e confonde tutti e tre gli acquirenti: il metodo P0 a P5 perde chiarezza proprio dove deve essere più chiaro.
2. La copertina del preventivo è un diagramma illeggibile: forme sagomate, tratteggi, diagonale gialla, P0 e P1 fuse senza spiegazione.
3. Il metro giallo è l'unico elemento forte e ripetuto ovunque; senza variazione rischia di diventare decorazione invece di misura.

## Feedback azionabili
1. Nomi delle fasi: usare termini dell'industria (Sopralluogo, Assessment, Simulazione, Prova in laboratorio, Pilota, Consegna) in hero, preventivo e totem; tenere la sartoria solo nella costruzione grafica.
2. `applicazioni/preventivo-cover`: sostituire i cartamodelli con una sola fila lineare P0 a P5 lungo il metro giallo, con durata e "decidi qui" a ogni tacca, come nella pagina interna.
3. `applicazioni/hero`: aggiungere la riga per i laboratori (SDK, ROS 2, simulatore, consegna) nella fascia delle quattro colonne o sotto la CTA.
4. `applicazioni/reel-g1`: liberare il G1 dal riquadro di carta e mostrarlo a tutta altezza in uno spazio con una sagoma di visitatore; tenere la battuta del copione in primo piano.
5. Metro giallo: usarlo solo dove misura qualcosa di reale (altezza, ingombro, settimane), toglierlo dai punti in cui è solo cornice.
6. `applicazioni/linkedin-anonimo`: "85 ore di assistenza" e "Manuale tecnico rev. 1.1" sono dettagli del contratto; generalizzarli nella versione anonima.
