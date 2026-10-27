# Revisione art director, round 1: direzione C

File aperti: `logo/simbolo.svg`, `logo/favicon.svg`, `logo/test.png`, tutti i PNG in `applicazioni/`, `palette.md`, `tipografia.md`, `concept.md`, `autocritica.md`.

## Voti

| Criterio | Voto | Motivazione |
|-|-|-|
| 1. Qualità del marchio | 6 | Idea forte (la traversa diventa un richiamo); il tracciato in `simbolo.svg` è però la A di STIX Two Bold con le curve originali, la proprietà del segno sta solo nel punto e nel filo, e il filo che sporge a destra sbilancia la lettera. |
| 2. Originalità | 7 | Il registro del paper scientifico (figure numerate, note, barre d'errore) non è usato da nessun concorrente rilevato ed è credibile per laboratori e R&D. |
| 3. Tipografia | 8 | La migliore del round: STIX Two e DM Mono con gerarchia chiara, numeri di riga, note, corsivi per i limiti; regge nel documento lungo come nel titolo. |
| 4. Colore | 6 | Sistema sobrio e ben regolato (una evidenziazione per pagina); il giallo evidenziatore è acido, su schermo è efficace, su carta e vinile rischia di sembrare economico o da cancelleria. |
| 5. Coerenza del sistema | 8 | Richiamo, evidenziatore, figura numerata e nota a margine tornano su ogni formato con lo stesso significato. |
| 6. Qualità delle applicazioni | 8 | Preventivo interna eccellente (tabella criteri, nota di revisione, grafico simulato contro misurato con dispersione); reel con registro della conversazione e risposta fuori copione è la migliore traduzione della promessa eventi. |
| 7. Assenza di AI slop | 6 | Due tic ripetuti e un'affermazione falsa nel mockup (vedi sotto). |

**Voto complessivo: 7,0**

## Slop e problemi trovati

- Evidenziatore giallo sotto parte dell'headline in quasi ogni formato: `hero.png` "prima di investire.", `linkedin-sacmi.png` "conosce già il tuo stabilimento.", `totem.png` "con un tecnico Abra". Ripetuto così diventa un effetto da landing, e contraddice la regola di `palette.md` (l'evidenziatore marca il dato misurato).
- Richiami decorativi: in `linkedin-sacmi.png` "Manuale rev 1.1" punta a una zampa, "Simulatore MuJoCo" punta all'anca, "Repository" al fianco; in `hero.png` "Limiti" punta al dorso. Il richiamo, che nel sistema significa "qui c'è la cosa misurata", viene usato su punti a caso.
- `linkedin-sacmi.png`, piede: "Caso pubblicato con il consenso scritto di SACMI". Il consenso oggi non esiste: il mockup afferma un fatto falso e rischia di essere pubblicato così.
- `linkedin-sacmi-anonimo.png`: il paragrafo tocca il riquadro della figura, manca lo spazio di respiro presente nella versione nominativa.
- `livrea.png`: l'etichetta di inventario dice "Unità G1-002" ed è applicata, nella figura C, su un Go2.

## I 3 problemi più gravi

1. **Il simbolo è una lettera di un font libero con un'aggiunta.** Chiunque scarichi STIX Two ottiene la stessa A; per un marchio da registrare serve un disegno proprio (aste, grazie, apice) oltre al richiamo.
2. **Il richiamo perde significato quando è decorativo.** È l'elemento proprietario del sistema e oggi è usato come ornamento su foto e titoli.
3. **Registro accademico per il segmento eventi e per gli acquisti.** Totem e reel funzionano grazie alla chiarezza, ma l'evidenziatore acido e il serif da rivista restano distanti dal brand manager.

## Feedback azionabili

1. `logo/simbolo.svg`: ridisegnare la A a mano partendo da STIX (apice tagliato, grazie asimmetriche ridotte, contrasto adattato al punto) e accorciare il filo in modo che sporga dalla gamba destra al massimo di un tratto; verificare a 16 px con una versione dedicata pixel per pixel, come già previsto in autocritica.
2. Regola d'uso dell'evidenziatore: solo su numeri e criteri misurati, mai sull'headline. Correggere `hero.png`, `linkedin-sacmi.png`, `linkedin-sacmi-anonimo.png`, `totem.png`.
3. Richiami sulle foto: ogni punto deve cadere sul componente nominato (LiDAR sulla testa, batteria sul vano batteria); le voci che non sono parti fisiche (manuale, repository, simulatore) vanno in nota a margine, senza punto sulla foto.
4. `linkedin-sacmi.png`: sostituire la frase di piede con "Bozza: pubblicare solo con il consenso scritto di SACMI".
5. `livrea.png`: allineare l'etichetta al robot mostrato (Go2) oppure mostrare il G1.
6. `palette.md`: provare un giallo meno acido e più pigmentato (verso `#E3D64A` o una tinta Pantone gialla non fluorescente) e verificarlo su vinile opaco prima di fissarlo.
7. `linkedin-sacmi-anonimo.png`: ripristinare lo spazio tra testo e figura come nella versione nominativa.

## Somiglianze con altre direzioni

- **C e A**: stesso registro documentale (revisioni, cartigli, riquadri "Esempio", schede di prova al banco) e stessa headline dell'hero. Oggi le separa soprattutto la tipografia (serif scientifico contro grotesk da segnaletica). Se entrambe passano al round 2, A deve spingere sulla targa dati e sul disegno tecnico, C sul paper e sulla nota.
