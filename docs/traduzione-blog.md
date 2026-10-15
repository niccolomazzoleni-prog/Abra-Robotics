# Traduzione dei post del blog nelle lingue del sito

Brief operativo per chi (persona o agente) traduce i post di `blog/` in una delle lingue del sito:
`de fr es pl nl cs sv da no fi` (l'inglese è già fatto e vale come riferimento di stile).
Il testo è l'unica cosa da produrre: `scripts/blog_lingue.py` costruisce la pagina completa
(head, JSON-LD, hreflang, menu e footer, link verso le pagine della stessa lingua).

## Fonte di verità

- **Il post italiano in `blog/<slug>.html` è la fonte.** Specifiche, numeri, prezzi, date, citazioni
  e fonti vanno riportati identici. Niente fatti aggiunti, niente arrotondamenti diversi, niente
  specifiche "ricordate": se un dato non è nel post italiano, non va nella traduzione.
- `en/blog/<slug>.html` serve solo come riferimento di terminologia (nomi prodotto, "secondary
  development", "payload") e per vedere come si adatta un passaggio solo-Italia a un altro paese.
- `data/lingue/<codice>.json` è la fonte per il paese: `price_format` (separatore migliaia e
  simbolo), `markets` (paesi coperti), `delivery` (spedizione, IVA, dogana), `incentives`
  (incentivi del paese), `service`, `ui` (etichette). Le pagine modello `<codice>/unitree-g1.html`
  mostrano formato prezzi e terminologia già in uso: copiarli.

## Cosa produrre

Un frammento HTML per ogni post, con esattamente questo contenuto e nient'altro:

```html
<title>Titolo tradotto, 20-65 caratteri</title>
<meta name="description" content="Descrizione tradotta, 70-165 caratteri"/>
<article class="article-wrap"> ... </article>   <!-- l'intero elemento article del post italiano, tradotto -->
```

Poi, dalla radice del repo:

```bash
python scripts/blog_lingue.py build <codice> <slug> <percorso-del-frammento>
python scripts/blog_lingue.py check <codice> <slug>
```

`check` stampa JSON con `ok` ed `errors`: correggere il frammento e ricostruire finché `ok` è `true`.
Non eseguire `sync`, non modificare i post italiani, lo script o altri file, non fare commit.
Il frammento va tenuto fuori dal repo (per esempio in una cartella temporanea).

## Regole di traduzione

1. **Struttura intoccabile.** Ogni tag, attributo, classe, id, href e src resta identico al post
   italiano. Non aggiungere, togliere o riordinare elementi. I link vengono localizzati dallo script.
   Blocchi `pre`/`code`, nomi dei tasti del telecomando (L2 + B), indirizzi IP, nomi di topic e
   comandi restano come sono. Anche gli attributi `aria-label` restano come sono.
2. **Tutto il testo visibile va tradotto**: titoli, paragrafi, tabelle, FAQ, fonti (i titoli dei
   paper restano in inglese), breadcrumb, etichetta sopra il titolo, data, callout, didascalie,
   indice laterale, le card prodotto (`product-strip`: "Prodotti citati nell'articolo", "Listino
   completo", "Tutta la gamma X", "Vedi scheda", "Preventivo", "IVA esclusa", le righe descrittive)
   e la CTA finale (`article-cta`).
3. **Prezzi.** Stesso numero del post italiano, scritto nel formato della lingua
   (`price_format` nel JSON; es. de `19.809 €`, fr `19 809 €`, pl `od 19 809 €`). "da X €" diventa
   l'equivalente usato nelle pagine modello della lingua (de `ab`, fr `dès`, pl `od`, ...).
   "su preventivo" / "su richiesta" diventa "prezzo su richiesta" nella lingua.
   Mai ricalcolare, convertire o aggiornare un prezzo.
4. **Numeri e unità.** Separatore decimale della lingua (de `3,7 m/s`, en `3.7 m/s`), unità
   invariate, date nel formato della lingua ("Aggiornato 15 ott 2026" tradotto).
5. **Frasi solo per l'Italia** (il `check` le rifiuta): IVA esclusa, spedizione e dazio inclusi,
   iperammortamento, Nuova Sabatini, Transizione 5.0, credito d'imposta, "in italiano",
   "filiera Unitree Italia". Si sostituiscono così:
   - nota prezzi: "prezzi in euro, IVA esclusa; trasporto e assicurazione fuori dall'Italia sono
     quotati nell'offerta" nella formulazione di `delivery.intro` del JSON della lingua;
   - incentivi italiani: il testo di `incentives.intro` del JSON della lingua (programmi del
     paese; Abra fornisce offerta e documentazione tecnica, non consulenza fiscale); l'elemento
     link resta, può cambiare solo il testo del link;
   - "Abra Robotics fa parte della filiera Unitree Italia": "Abra Robotics fornisce la gamma
     Unitree in <paesi di `markets`>, con supporto in inglese";
   - "in Italia" nei titoli e nelle FAQ ("Quanto costa ... in Italia?"): il paese principale della
     lingua, oppure nessun paese se la frase regge senza;
   - D.Lgs. 81/2008 (post sul Regolamento macchine): la norma nazionale sulla sicurezza sul lavoro
     del paese, se la si conosce con certezza, altrimenti una frase generica "la normativa nazionale
     sulla sicurezza sul lavoro"; l'elemento link resta;
   - RSPP: "responsabile della sicurezza" nella lingua.
6. **Nessun concorrente.** Mai nominare negozi o rivenditori (il `check` li rifiuta).
7. **Stile.** Testo per tecnici e compratori, scritto come lo scriverebbe un madrelingua: frasi
   brevi, niente trattini lunghi, niente frecce, niente riempitivi di marketing, niente calchi
   dall'italiano. Il titolo deve contenere la parola chiave del post nella lingua (es. de
   "Unitree G1 Preis", fr "prix Unitree G1") quando il post italiano la contiene.
8. **Lunghezza.** Il `check` rifiuta testi sotto il 60% delle parole dell'originale: tradurre tutto.

## Controllo di qualità prima di consegnare

Per ogni post, oltre a `check` verde:

- confrontare la sequenza dei numeri (prezzi, kg, m/s, mAh, mesi di garanzia, DoF, date) tra
  italiano e traduzione: devono coincidere uno a uno;
- confrontare la sequenza dei tag `<h2>`/`<h3>` e il numero di righe delle tabelle;
- aprire il frammento e rileggere intro, tabella prezzi, FAQ e CTA come farebbe un lettore del paese;
- grep nel file costruito di: `IVA`, `Italia`, `€` con formato sbagliato, `—`, `→`.

## Organizzazione del lavoro

- 23 post, ognuno da 1.000 a 2.500 parole: lavorare a blocchi di 3-4 post per volta (un sotto-agente
  per blocco), non tenere più di quattro post nel contesto.
- Ordine consigliato (prima i post con più ricerca): `robot-umanoide-prezzo`, `cane-robot-prezzo`,
  `unitree-go2-vs-go2-pro`, `unitree-g1-quale-versione-scegliere`, `confronto-umanoidi-2026`,
  `unitree-h2-plus-prezzo-specifiche`, `unitree-r1-cosa-fa-prezzo`, `unitree-as2-italia`,
  `unitree-h2-italia`, `unitree-robotics-chi-e`, `cobot-cosa-sono`, `palletizzazione-cobot-costi`,
  `robot-quadrupede-ispezione-industriale`, `umanoidi-vs-robotica-tradizionale`,
  `poc-robot-umanoide-azienda`, `unitree-regolamento-macchine-2027`,
  `finanziamento-robot-industria-40`, `unitree-italia-guida-completa`, `ros2-unitree-guida-rapida`,
  `unitree-g1-programmazione`, `unitree-g1-guida-operativa`, `unitree-g1-aggiornare-firmware`,
  `ricerca-unitree-arxiv`.
- `finanziamento-robot-industria-40` e `unitree-italia-guida-completa` parlano quasi solo
  dell'Italia (incentivi italiani, "chi vende Unitree in Italia"): si traducono per ultimi e con il
  paragrafo incentivi riscritto sul paese usando `incentives` del JSON; se il post non regge in
  quella lingua, segnalarlo invece di forzare.
- Alla fine: `python scripts/blog_lingue.py list` deve mostrare il codice lingua su tutti i post;
  consegnare un elenco dei post con esito del `check` e i passaggi adattati con giudizio.
