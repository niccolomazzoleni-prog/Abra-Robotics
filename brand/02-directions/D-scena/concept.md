# Direzione D: Prova generale (v2)

Territorio D, "Il futuro in scena" (nome di lavoro, solo interno). Nome della direzione: **Prova generale**.

## L'idea in una frase

Prima di ogni debutto c'è la prova generale: Abra fa vedere il robot al lavoro sul caso del cliente prima che investa, e lo scrive con un logotipo in cui ogni lettera è un arco scenico.

## Da dove nasce

In italiano "prova" è la verifica tecnica ed è anche la prova di uno spettacolo. Il posizionamento "Prima la prova" e il teatro usano la stessa parola per la stessa cosa: si ripete tutto, con il copione scritto e i movimenti segnati sulla pianta del palco, prima della sera in cui conta.

Dalla v2 la direzione prende dal teatro due cose sole:
1. **L'arco scenico** del teatro all'italiana, con il tetto tondo e la base piana. Diventa la forma degli occhielli del logotipo e la cornice delle immagini nei formati evento.
2. **La pianta dei movimenti**: in regia il percorso di ogni interprete si segna sulla pianta, da una posizione "a" a una posizione "b". In robotica è lo stesso gesto: la navigazione autonoma porta il robot da a a b, e prima di farlo dal vero lo si prova in simulazione. La pianta diventa il modo di disegnare le fasi P0 a P5, i percorsi e i dati.

## Il sistema in breve

- **Logotipo**: "abra" disegnato a mano in minuscolo geometrico. Ogni occhiello è un arco scenico; la "a" e la "b" sono speculari (angolo tondo a sinistra nella a, a destra nella b), così la parola ha un ritmo di quinte. "Robotics" è un descrittore separato, composto in Archivo Expanded.
- **Simbolo**: "ab", i due portali affiancati. Legge l'iniziale del nome e dice il movimento base del metodo: da a a b. Favicon disegnata a pixel.
- **Colore firma**: Magenta di scena `#D6006F`, il colore delle gelatine magenta che ogni tecnico luci ha nella valigia. È anche un primario di stampa (Pantone 226 C indicativo) e porta il nome di una città lombarda. Accanto: Grafite, Carta, Cemento. Nessun giallo, ocra, ambra, bruno o rosso.
- **Due registri**:
  - *Documento* (preventivo, post aziendali, biglietto, scheda per i laboratori): Carta e Grafite, Archivo Bold per i titoli, il magenta solo nei punti della pianta delle fasi e in qualche etichetta.
  - *Scena* (reel, totem, livrea, eventi): fondo Grafite, campiture magenta piene dentro l'arco scenico, Archivo Condensed in scala grande, il pubblico disegnato come sagome.
- **Voce**: scandita come una regia, con imperativi e benefici chiari; i limiti si scrivono come didascalie in corsivo tra parentesi.

## Razionale strategico

1. **Il metodo arriva prima dello spettacolo.** La home, il preventivo e il post SACMI sono su fondo chiaro e mostrano le fasi come posizioni su un percorso. Il direttore R&D legge un documento tecnico; il teatro resta nella forma del logotipo.
2. **Un marchio proprietario sull'intera parola.** Il logotipo è disegnato da zero e non contiene una A maiuscola. In monocromia la silhouette resta unica: archi a tetto tondo con base piana, la "b" con l'ascendente, la "r" che chiude il ritmo.
3. **Lo spettacolo dove serve.** Eventi e social hanno scala, colore pieno e pubblico in scena. Il passaggio da un registro all'altro cambia la quantità di magenta e la larghezza del carattere; marchio e griglia restano gli stessi.
4. **Funziona senza robot e con qualunque produttore.** L'arco scenico vuoto con la pianta da a a b è già un'immagine; il robot entra quando c'è una foto propria.
5. **Si produce in due.** Una famiglia di font OFL in sei istanze statiche, un colore firma che è un primario di stampa, archi con `border-radius`, percorsi in SVG.

## Segmento a cui parla meglio

Eventi e fiere restano il segmento più servito dai formati di scena. La manifattura ora ha documenti sobri e un preventivo che parla di tempo ciclo e decisioni scritte. Il laboratorio ha una scheda dedicata, "Fai partire i tesisti sul robot nella prima settimana", con SDK, ROS 2, simulatore e percorso di otto settimane.

## Cosa sacrifica

- **La familiarità del colore.** Il magenta è insolito nella robotica industriale: va dosato e tenuto fuori dalle superfici grandi dei documenti.
- **La leggibilità immediata del simbolo da solo.** "ab" va imparato; per questo il primo contatto usa sempre il logotipo intero.
- **Una parte del teatro.** Sipari, riflettori, coni di luce e palco acceso del round 1 sono stati tolti.
