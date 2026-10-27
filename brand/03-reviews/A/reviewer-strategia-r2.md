# Revisione strategica, direzione A, round 2

Revisore: strategia. Data: 28/10/2026.
Materiali aperti: changelog.md, round1-sintesi.md, presentazione.html, logo/test.png, PNG v2 di hero, preventivo copertina, totem, reel, post LinkedIn anonimo; titoli di tutte le applicazioni HTML. Colore firma (verde di misura con alluminio) assunto come vincolo, non valutato.

## Voti per criterio

| Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|
| 1. Coerenza con brief e brand platform | 8 | 8 | La legatura Ab sulla squadra da disegno tiene il legame con il disegno tecnico; la pianta della postazione sulla copertina del preventivo è la migliore immagine di "sai prima" vista finora. |
| 2. Vincoli di posizionamento | 8 | 8 | Nessuna violazione; segnaposto dichiarati, nominativo marcato "solo con consenso scritto". |
| 3. Efficacia sui tre segmenti | 7 | 8 | Hero con tre ingressi e la riga per i laboratori; totem e reel ora hanno scala, sagome e un titolo leggibile a distanza. |
| 4. Differenziazione dai competitor | 6 | 7 | B612 dà una voce propria ai titoli e la legatura esce dalla A isolata; resta Barlow su tutto il testo corrente accanto a un verde pieno, la stessa coppia di MYBOTSHOP (Barlow e verde brillante). |
| 5. Tenuta nel tempo e oltre Unitree | 8 | 8 | Il segno e il cartiglio non dipendono dal produttore; il verde come campo pieno regge su documenti, casse e social. |
| 6. Chiarezza della promessa nei testi applicati | 8 | 8 | "Decidi sul robot con un numero misurato in mano" passa il test dei 5 secondi; il totem perde l'imperativo. |

**Voto complessivo: 7,8** (r1: 7,5)

## Problemi residui

1. **Barlow resta la voce di tutto ciò che si legge da vicino.** Con il verde ora dominante, testo corrente, etichette e dati in Barlow ricostruiscono il codice visivo di MYBOTSHOP, l'unico distributore europeo che fa anche noleggio. Il rischio pesa proprio sul segmento eventi.
2. **La A della legatura si legge come un triangolo rettangolo.** In "Abra Robotics" a 26 px la A perde la traversa visibile e il nome rischia di leggersi "4bra" o "/bra" a chi non lo conosce. A 16 px la favicon funziona perché è isolata.
3. **Headline uguali a quelle di altre direzioni** (dettaglio in fondo): la copertina del preventivo, la pagina delle fasi e il post anonimo hanno strutture quasi identiche a B, D ed E.

## Feedback azionabili ancora necessari

1. `tipografia.md` e `assets/a.css`: porta in B612 anche etichette e dati brevi (cartiglio, riquadri di controllo, targhe), e lascia Barlow al solo testo lungo. Così la voce visibile a distanza non coincide con quella di MYBOTSHOP.
2. `logo/orizzontale.svg` e `logo/test.html`: aggiungi una prova di lettura del logotipo a 20 e 26 px con persone che non conoscono il nome; se "Abra" non si legge al primo colpo, ispessisci la traversa interna della A nella versione per schermi piccoli.
3. `applicazioni/totem.html`: "Umanoide a noleggio, a giornata." è un titolo nominale breve, vicino alle chiusure punchy vietate. Riscrivilo all'imperativo con il beneficio ("Prenota l'umanoide per la tua giornata in fiera, con il nostro tecnico accanto" o simile, nel registro asciutto della direzione).
4. `applicazioni/preventivo-cover.html` e `applicazioni/preventivo-interna.html`: differenzia i titoli dalle versioni di B (vedi tabella). "Decidi" è il verbo di A: tienilo nell'hero e usa un'altra azione nel preventivo, per esempio "Porta in direzione il tempo ciclo misurato della linea 3".
5. `applicazioni/linkedin-sacmi-anonimo.html`: il titolo coincide quasi parola per parola con D ed E; sposta il beneficio sul documento consegnato, che è il codice di A ("Ricevi il robot con mappa, simulatore e manuale già firmati" o simile).

## Headline troppo simili tra direzioni (riguardano A)

| Applicazione | A | Simile a |
|-|-|-|
| Preventivo, copertina | "Decidi sull'umanoide della linea 3 con il tempo ciclo misurato." | B: "Decidi sul robot con il tempo ciclo misurato alla postazione 3." |
| Hero | "Decidi sul robot con un numero misurato in mano." | B, copertina del preventivo (stessa apertura "Decidi sul robot con") |
| Preventivo, fasi | "Decidi fase per fase, con un criterio scritto..." | B: "Decidi fase per fase, con il verbale..." |
| LinkedIn anonimo | "Fai lavorare il tuo team sul robot dal primo giorno, con mappa e simulatore già pronti." | D: "Fai lavorare il tesista sul robot dal primo giorno."; E: "Fai partire una tesi sul robot dal primo giorno." |

Proposta di ripartizione: "Decidi" resta ad A (hero e pagina delle fasi), B cambia verbo nel preventivo.
