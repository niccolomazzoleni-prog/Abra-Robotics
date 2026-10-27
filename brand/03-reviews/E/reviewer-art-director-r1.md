# Revisione art director, round 1: direzione E

File aperti: `logo/simbolo.svg`, `logo/favicon-16.svg`, `logo/test.png`, tutti i PNG in `applicazioni/`, `palette.md`, `tipografia.md`, `concept.md`, `autocritica.md`.

## Voti

| Criterio | Voto | Motivazione |
|-|-|-|
| 1. Qualità del marchio | 5 | Il simbolo è una A senza traversa con un tratteggio che la attraversa: ripropone la "Λ" che il brief chiede di sostituire, e il tratteggio giallo su fondo scuro si legge come linea di mezzeria stradale; a 16 px restano tre puntini. |
| 2. Originalità | 7 | Il cartamodello è il territorio più inatteso del round e la corrispondenza fasi e mestiere (misure, imbastitura, prova, modello) è precisa. |
| 3. Tipografia | 6 | Bricolage Grotesque ha carattere ma è il grotesk con ink trap più usato nel 2024 e 2025; nel verticale "R o b o t i c s" spaziato a forza sulla larghezza di "Abra" è un errore di composizione. |
| 4. Colore | 6 | Tela e carta modello sono calde e proprie; flanella con giallo metro, soprattutto in tratteggio, richiama nastro di sicurezza e segnaletica stradale. |
| 5. Coerenza del sistema | 7 | Regola tratteggio contro linea continua applicata ovunque, pezzo di carta con tacche riconoscibile; il tratteggio è usato anche dove non significa "in prova" (cornici, pulsanti). |
| 6. Qualità delle applicazioni | 6 | Hero chiaro e preventivo interna ben strutturato (calendario a metro, fasi in prova tratteggiate); copertina del preventivo e livrea hanno elementi senza funzione. |
| 7. Assenza di AI slop | 6 | Frecce e tratteggi decorativi, un righello che non misura. |

**Voto complessivo: 6,1**

## Slop e problemi trovati

- `preventivo-cover.png`: ogni pezzo di cartamodello porta una freccia doppia orizzontale che non quota nulla, e un tratteggio giallo diagonale attraversa la pagina senza collegare niente.
- `linkedin-sacmi.png` e `linkedin-anonimo.png`: il metro giallo sotto il Go2 arriva a 60 e il robot lo supera, mentre il testo dice "circa 70 × 31 × 40 cm". Per una direzione basata sulla misura, il righello deve misurare.
- `biglietto.png`, fronte: A bianca e tratteggio giallo su flanella; senza il retro sembra un cartello stradale.
- `livrea.png`, flight case: tratteggio giallo spesso sulla cassa scura, la lettura più vicina è il nastro da cantiere che `autocritica.md` dichiara di evitare.
- `hero.png`: pulsante secondario con bordo tratteggiato; in questo sistema il tratteggio vuol dire "non ancora misurato", quindi su un pulsante comunica incertezza.

## I 3 problemi più gravi

1. **Il simbolo torna alla A senza traversa.** È proprio il difetto del logo attuale citato nel brief; il filo d'imbastitura non basta a chiudere la lettera a 16 e 32 px.
2. **Lettura stradale o di sicurezza del giallo tratteggiato.** Su fondo scuro (biglietto, avatar, cassa) la metafora sartoriale non arriva, arriva la mezzeria.
3. **Elementi della metafora usati come decorazione.** Frecce, tratteggi e metri che non quotano niente svuotano la regola semantica che è il punto di forza della direzione.

## Feedback azionabili

1. `logo/simbolo.svg`: chiudere la A con una traversa continua nel controforma (il filo cucito che diventa linea piena) e lasciare il tratteggio solo fuori dalle aste; così la lettera è completa e la regola "tratteggio in prova, continuo misurato" si legge nel segno stesso.
2. `logo/favicon-16.svg`: ridisegnare con traversa piena e un solo punto giallo esterno; tre trattini a 16 px sono rumore.
3. `logo/verticale.svg`: eliminare la spaziatura forzata di "Robotics"; comporlo con spaziatura normale e allineato a sinistra.
4. `preventivo-cover.png`: sostituire le frecce con quote vere (durata in settimane di ogni fase, con il metro come scala) e togliere il tratteggio diagonale.
5. `linkedin-sacmi.png` e `linkedin-anonimo.png`: portare il metro a 70 cm e allinearlo alla lunghezza reale del robot nella foto.
6. Formati scuri (`biglietto.png`, `livrea.png`, avatar): usare il giallo come metro con tacche e numeri, mai come tratteggio spesso su flanella.
7. `hero.png`: pulsante secondario con bordo continuo sottile; riservare il tratteggio a fasi e dati non ancora misurati.
8. `tipografia.md`: valutare un grotesk OFL meno diffuso per i titoli, oppure usare Bricolage a larghezza 100 e peso 600 per ridurre l'effetto ink trap di tendenza.

## Somiglianze con altre direzioni

- **E e A**: stesso motivo del righello millimetrato sul biglietto (A sul fronte, E sul retro) e stessa quota verticale accanto al robot nell'hero. Se restano entrambe, il metro deve appartenere a una sola.
- **E e D**: fondo scuro con giallo segnale nei formati evento; più distanti nel resto del sistema.
- **E, B e D** condividono l'headline dell'hero ("Prova il robot sul tuo caso prima di investire.").
