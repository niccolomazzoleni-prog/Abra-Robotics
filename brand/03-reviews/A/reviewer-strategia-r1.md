# Revisione strategica, direzione A, round 1

Revisore: strategia (partner esterno, non coinvolto nella creazione). Data: 27/10/2026.
Materiali aperti: presentazione.html, concept.md, voce.md, logo/test.png, tutti i PNG in applicazioni/ (hero, preventivo copertina e interna, LinkedIn nominativo e anonimo, reel, biglietto, totem, livrea).

## Voti per criterio

| Criterio | Voto | Motivazione |
|-|-|-|
| 1. Coerenza con brief e brand platform | 8 | "Prima la prova" diventa segno, griglia e documento; la tabella "cosa sai prima / cosa ti resta" è trascritta quasi alla lettera nella copertina del preventivo. |
| 2. Vincoli di posizionamento | 8 | Unitree compare solo come segnaposto dichiarato, mai rivenditore, mai famiglie; la riga "Responsabilità scritte" del preventivo chiarisce che la certificazione CE dell'insieme passa da un ente terzo, quindi niente turn key. |
| 3. Efficacia sui tre segmenti | 7 | Manifattura da 9, laboratorio da 7 (il pacchetto per i tesisti è nel post, assente dall'hero), eventi da 5: totem e reel sono chiari ma hanno il tono di una scheda tecnica. |
| 4. Differenziazione dai competitor | 6 | Barlow è il carattere di MYBOTSHOP; grigio freddo, etichette maiuscole spaziate e grotesk tecnico sono il default della categoria segnalato in 01-competitor §4; il reel grafite più verde si avvicina a Roboverse Reply. |
| 5. Tenuta nel tempo e oltre Unitree | 8 | Il sistema regge senza robot (preventivo, biglietto, livrea) e con qualunque piattaforma; il segno di riferimento è neutro rispetto al produttore. |
| 6. Chiarezza della promessa nei testi applicati | 8 | Hero e copertina passano il test dei 5 secondi; criteri, importi e limiti sono nella stessa pagina e marcati "Esempio". |

**Voto complessivo: 7,5**

## I 3 problemi più gravi

1. **Riconoscibilità di categoria debole.** Tolto il triangolo, la direzione assomiglia a un fornitore di automazione tedesco qualunque: Barlow (lo stesso di MYBOTSHOP), alluminio e grafite, etichette maiuscole spaziate. Il brief chiedeva di uscire dal grotesk di default; qui si resta dentro con un disegno più curato.
2. **Eventi trattati come una pratica da sbrigare.** Il totem è un foglio dati con calendario: chiaro, e privo della presenza scenica che il brief ammette (scala, luce, allestimento). La stessa direzione lo dichiara nell'autocritica, ma per il segmento più visibile del metodo serve almeno un registro più caldo dentro lo stesso sistema.
3. **La versione anonima del post SACMI è riconoscibile.** "Verbale di consegna", data 29.10.2026, Go2 EDU con LiDAR, tesi in azienda, MuJoCo, manuale rev 1.1: chi segue Abra o il settore ceramico ricostruisce il cliente. Il brief chiede una versione senza dettagli che lo rendano identificabile.

## Feedback azionabili

1. `applicazioni/linkedin-sacmi-anonimo.html`: togli la data esatta e "rev 1.1"; sostituisci "Verbale di consegna · Stabilimento del cliente" con un'etichetta generica ("Consegna di ottobre"); tieni il tipo di robot e il pacchetto, che sono la prova del metodo.
2. `tipografia.md` e `assets/a.css`: valuta un carattere di titolazione meno diffuso nel settore (per esempio una famiglia da segnaletica o da targa con licenza OFL meno usata di Barlow), oppure personalizza Barlow Semi Condensed nei titoli con le stesse regole del logotipo (terminali tagliati, forme a stadio) per renderlo proprietario.
3. `applicazioni/hero.html`: aggiungi nella riga delle quattro icone, o sotto la CTA, una riga dedicata ai laboratori ("Per i laboratori: robot con SDK, ROS 2, simulatore e manuale per i tesisti"). Oggi il criterio di successo "laboratorio" sull'hero non è soddisfatto.
4. `applicazioni/totem.html`: porta la testata grafite a tutta altezza nella metà superiore e usa il G1 in scala reale con il triangolo di riferimento a terra come elemento scenico; il calendario resta, ridotto. Lo scopo è che a 4 metri si legga "umanoide a noleggio" prima di "documento".
5. `applicazioni/reel-g1.html`: il fondo grafite con verde segnale va differenziato dal codice Reply (blu notte con verde). Prova il reel su alluminio chiaro con il verde solo nel bollino "risposta dalla base di conoscenza approvata", coerente con la regola "il verde compare solo dove c'è una misura".
6. `logo/test.png`: a 16 px il vuoto e il triangolo pieno si fondono in una macchia. Disegna una favicon ottica dedicata in cui il triangolo pieno resta e il vuoto superiore diventa una traversa piena; documenta la regola in `sistema-grafico.md`.
7. `presentazione.html`, sezione 10: "preventivo da 54.500 euro di servizi" va scritto come importo di esempio, per coerenza con la regola dei mockup.
8. `voce.md`: aggiungi due headline per gli eventi con il beneficio esplicito della data e del tecnico, nello stesso registro asciutto; oggi il registro eventi è coperto da una sola frase.
