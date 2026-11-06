# Piano SEO operativo per Claude: riferimento Unitree in Europa entro il 2027

Scritto il 28/10/2026. È un piano di esecuzione per le sessioni Claude che lavorano su questo repo: ogni attività
dice cosa cambiare, in quali file, quando è finita e perché si fa. Le attività che richiedono una persona
(account, telefonate, invii) sono segnate **[persona]**: Claude prepara il materiale, non le esegue.
Completa e sostituisce le priorità di `seo-sopra-meko.md`, che resta valido per la tabella di misura.

## Dove siamo (dati del 28/10/2026)

Fonti: Search Console API, 90 giorni (`company-brain/seo-monitor`), ricerca Google.it senza login, audit del repo.

- Il sito è giovane: impressioni da fine settembre, 3.849 nella settimana del 19/10, 207 clic in tutto il periodo.
  Paesi: Italia 1.836 impressioni, poi Svezia 558, Germania 442, USA 415, Spagna 372, Polonia 257.
- **"unitree"** su Google.it: assenti nei circa 75 risultati mostrati. Primi: unitree.com, Wikipedia, Meko
  (`mekosrl.it/unitree`, 3°), YouTube, Generation Robots. Meko ha 6 pagine nei risultati, noi 0.
- **"unitree italia"**: siamo 3° con `catalogo-unitree`, Meko 1° e 5°.
- La pagina `/unitree` di Meko ha circa 470 parole, nessuno schema, contenuto minimo. Il nostro catalogo ne ha
  4.400 con 341 link interni. **Il distacco non è di contenuto: è di autorità e di segnali confusi.**

Problemi misurati, in ordine di peso:

1. **Le nostre pagine si fanno concorrenza.** In Italia, per "unitree go2" Google divide le impressioni tra
   `prodotti/unitree-go2-edu-smart` (pos. 81), `prodotti/unitree-go2-pro` (64), `go2.html` (46) e
   `quadrupedi.html` (61). Lo stesso succede per "unitree b2" (3 pagine, pos. 43-55), "unitree go2 edu" (4 pagine),
   "unitree g1" (3 pagine), "unitree italia" (guida e catalogo, entrambe pos. 7).
2. **La pagina del marchio non è collegata dal sito.** `catalogo-unitree` riceve link da 12 pagine italiane,
   gli hub di famiglia da 37-72. La home non la collega. `lp-unitree` è "scansionata ma non indicizzata".
3. **Molte pagine povere.** Ci sono 511 schede in `prodotti/`, e quelle degli accessori hanno circa 250 parole
   (caricabatterie, piedini, telecomando). Undici URL sono "scansionate ma non indicizzate", soprattutto schede.
4. **L'x-default punta all'italiano.** L'hreflang delle pagine estere manda `x-default` su `go2.html`, quindi
   un utente austriaco, belga o portoghese senza versione nella sua lingua vede l'italiano.
5. **Le lingue estere hanno solo gli hub.** Le cartelle `de/` `fr/` `es/` `pl/` `nl/` `sv/` `da/` `no/` `cs/`
   `fi/` contengono circa 40 pagine ciascuna, contro le 466 italiane: non ci sono schede prodotto né catalogo.
   Dove la concorrenza è debole rendiamo già bene: `sv/unitree-go2` è 7° in Svezia, `da/unitree-go2` è 6° in
   Danimarca, `sv/unitree-g1` è 5°.
6. **CTR basso in prima pagina.** `blog/unitree-italia-guida-completa` è in pos. 6,6 con 0 clic; la guida G1
   in inglese ha 378 impressioni in pos. 6 e CTR dell'1,9%. `blog/cane-robot-prezzo` ha 200 impressioni in Italia
   in pos. 10, al limite della prima pagina.

## Obiettivo per il 2027, detto onestamente

"unitree" da solo è una ricerca di marca: unitree.com, Wikipedia e YouTube restano sopra qualsiasi rivenditore.
L'obiettivo misurabile è quindi:

- **primo rivenditore** su "unitree", "unitree [paese]" e "unitree [modello] (prezzo)" in ogni paese target;
- **prima pagina** su "unitree [modello] prezzo" per G1, H2, R1, Go2, AS2, A2 e B2 in IT, DE, FR, ES, NL, PL,
  SE, DK, NO, FI, CZ;
- **fonte citata** nelle AI Overviews e in ChatGPT/Perplexity per "dove comprare Unitree in [paese]" e "prezzo Unitree [modello]".

Tappe: entro fine gennaio 2027 sopra Meko su 8 delle 12 ricerche di `seo-sopra-meko.md`; entro giugno 2027
prima pagina in Italia su tutte e primo rivenditore in almeno 5 paesi esteri; entro dicembre 2027 tutti i paesi.

## Regole per chi esegue

- Ogni fase è una PR su un branch proprio, mai push diretti su `main`. Le PR restano piccole: una fase o una famiglia di pagine.
- Le pagine prodotto vengono dai generatori in `scripts/`: si modifica il generatore e si rigenera, non si
  ritoccano a mano centinaia di file. Le pagine scritte a mano (hub, blog) si modificano direttamente.
- Prezzi e specifiche vengono solo dal listino e dalle schede ufficiali, mai inventati.
- Dopo ogni deploy si richiede l'indicizzazione delle pagine cambiate (massimo 10 al giorno, prima gli hub)
  con `company-brain/seo-monitor/richiedi_indicizzazione.py` da WSL, e si manda IndexNow.
- Nessuna attività si chiude senza il controllo della metrica scritta nel suo "Fatto quando".

---

## Fase 0: misura (prima di tutto, 1 giorno)

Senza una misura per paese non si sa cosa funziona. Le posizioni medie di Search Console mescolano i paesi:
"unitree go2" risulta in pos. 51 di media, ma è 7 in Svezia e 46-81 in Italia.

**0.1 Report settimanale per paese e per pagina.** Estendere `company-brain/seo-monitor/report_unitree.py`:
- dimensioni `country` + `query` + `page` per i paesi target;
- sezione "Concorrenza interna": ricerche con 2 o più nostre pagine con almeno 5 impressioni nello stesso paese;
- sezione "Quasi in prima pagina": posizione tra 4 e 20 con almeno 20 impressioni;
- confronto con la settimana precedente.
Fatto quando: il report del lunedì contiene le tre sezioni e `run_weekly.sh` lo salva.

Fatto il 28/10/2026 (meta-opencode-glasses PR #115).

**0.2 Chi c'è prima di noi, per paese.** Le interrogazioni automatiche di Google non sono ammesse dai suoi
termini, quindi niente script. Una volta al mese una sessione Claude controlla a mano, dal browser, le ricerche
"unitree", "unitree [paese]" e "unitree [modello] [prezzo nella lingua]" nei paesi target e aggiorna la tabella
di `seo-sopra-meko.md`. Per tutto il resto fa fede il report per paese della 0.1.

---

## Fase 1: una pagina per ogni ricerca (settimane 1-2, l'impatto più rapido)

Perché: quando più pagine dello stesso sito rispondono alla stessa ricerca, Google divide i segnali e ne mostra
una sola, spesso la meno adatta. Google raccomanda di indicare una sola versione con canonical, link interni
coerenti e sitemap ([Search Central, URL duplicati](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)).
Le guide del settore concordano sul modello hub e pagine collegate, anche se mancano studi controllati recenti
([Ahrefs, cannibalizzazione](https://ahrefs.com/blog/keyword-cannibalization)). Da noi il problema è misurato:
è il punto 1 dei dati.

**Mappa ricerca → pagina** (da rispettare in tutte le attività):

| Ricerca | Pagina che deve vincere |
|---|---|
| unitree, unitree italia, distributore unitree | `catalogo-unitree.html` (diventa la pagina del marchio) |
| dove comprare unitree, unitree italia guida | `blog/unitree-italia-guida-completa.html` |
| unitree X, unitree X prezzo (X = G1, Go2, B2, R1, H2, AS2, A2) | hub `X.html` |
| modello esatto (go2 edu smart, g1 edu u2, b2w) | scheda `prodotti/...` |
| robot quadrupede, cane robot | `quadrupedi.html` e `blog/cane-robot-prezzo.html` |

**1.1 Pagina del marchio `catalogo-unitree`.**
- Titolo: "Unitree Italia: distributore, catalogo e prezzi di tutti i robot | Abra". H1: "Unitree in Italia".
- In cima, sopra l'elenco, un blocco di 80-120 parole: chi siamo nella filiera Unitree, assistenza e formazione
  in Italia, servizio 85 h/6 mesi, consegna, listino pubblico in euro. Poi un indice per famiglia con link
  a ogni hub.
- Schema: `Organization` (con `brand` Unitree), `BreadcrumbList`, `ItemList` delle famiglie.
- Collegarla da home, menu e footer di tutte le pagine italiane con il testo "Unitree Italia".
Fatto quando: link presente in tutte le pagine IT, `lp-unitree` sistemata (1.2) e richiesta di indicizzazione
inviata. Si misura dopo 4 settimane: per "unitree italia" in Italia vince una sola pagina, la posizione migliora.

**1.2 `lp-unitree`.** Prima si verifica con una persona se è la landing di Google Ads **[persona]**. Se non lo
è: `<link rel="canonical">` verso `catalogo-unitree.html`, toglierla dalla sitemap, spostare i testi utili nel
catalogo. Se lo è: `noindex, follow` e via dalla sitemap (gli annunci continuano a funzionare).

**1.3 Hub di famiglia sopra le schede.** Verificato il 28/10/2026: è già quasi tutto in opera.
`genera_hub_modelli.py` (`seo_schede`) mette sotto l'H1 di ogni scheda il link "Tutte le versioni Unitree X a
confronto, con prezzi" verso l'hub, il breadcrumb delle schede passa per l'hub e i titoli delle schede partono
dal nome esatto della versione. Lo schema `ProductGroup` **non** si usa: Google accetta in `variesBy` solo
colore, taglia, materiale, motivo, età e genere, e dichiara che il gruppo non ha un URL canonico
([Search Central, varianti prodotto](https://developers.google.com/search/docs/appearance/structured-data/product-variants)),
quindi non indicherebbe l'hub come pagina principale. Resta da fare solo se il report lo chiede: se dopo 6
settimane per "unitree go2", "unitree b2", "unitree g1" e "unitree go2 edu" in Italia vince ancora una scheda,
si toglie la scheda da `quadrupedi.html`/`umanoidi.html` lasciando solo l'hub. La concorrenza tra pagine per
queste ricerche resta comunque in gran parte un problema di autorità (Fase 4): le posizioni sono tutte tra 40 e 80.

**1.4 URL senza `.html`.** Verificato il 28/10/2026: non è un problema. I link interni usano già la forma
`.html` (gli unici senza estensione sono le home delle lingue, `/de/` ecc.), Search Console registra le pagine
con `.html` e la versione senza estensione che si vede nei risultati è solo il modo in cui Google mostra il percorso.

---

## Fase 2: qualità e risultati in prima pagina (settimane 2-4)

Perché: gli aggiornamenti principali del 2026 (marzo e maggio) hanno colpito soprattutto le pagine prodotto e
categoria povere o copiate dal fornitore, e premiato le pagine con indicazioni d'acquisto: come scegliere,
differenze, spedizione, resi ([Numinix, marzo 2026](https://www.numinix.com/blog/?p=10029);
[analisi di maggio 2026](https://www.pulse.bot/digital-marketing/news/google-may-2026-core-update-analysis-intent-market-fit-and-source-type-drove-the-biggest-visibility-44307231-3073-4929-a4b1-12c4f3565d87/)).
Sono letture di agenzie, non dati di Google, ma sono coerenti con le linee guida sui contenuti utili di Google
([Search Central](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)).

**2.1 Schede accessori povere.** Elencare le schede in `prodotti/` sotto le 400 parole utili e incrociarle con
Search Console (impressioni a 90 giorni e stato di indicizzazione). Regola:
- 0 impressioni e non indicizzata → `noindex, follow`, fuori dalla sitemap; resta nel catalogo e nel feed Merchant;
- con impressioni → nel generatore si aggiungono compatibilità (quali Go2/B2), cosa risolve, alternative e
  FAQ di 3 domande, ricavate dalle schede ufficiali.
Fatto quando: nessuna scheda indicizzabile sotto le 400 parole; la sitemap contiene solo pagine indicizzabili.

**2.2 Hub di famiglia come guida all'acquisto.** In ogni hub, se manca: tabella di confronto delle versioni
(prezzo, carico, autonomia, sensori, a chi serve), "quale scegliere" in 3-4 righe per profilo (università,
industria, sviluppatore), consegna, garanzia e assistenza in Italia, FAQ. La risposta alla domanda "quanto
costa" sta nelle prime 2 righe. È il formato che le AI Overviews citano più spesso.

**2.3 `blog/cane-robot-prezzo` dalla pos. 10 alla 5.** 200 impressioni in Italia e la ricerca è commerciale.
Prezzo e tabella in cima, data di aggiornamento visibile, sezione "giocattolo o robot vero", link agli hub
con il nome del modello come testo, link in entrata dagli hub di Go2, AS2, A2 e B2 con il testo "prezzi dei cani robot".
Fatto quando: posizione media in Italia ≤ 6 dopo 4 settimane.

**2.4 Titoli e descrizioni per il CTR.** Riscrivere titolo e meta description delle pagine con posizione
≤ 10 e CTR sotto il 2% (dal report: `blog/unitree-italia-guida-completa`, `en/blog/unitree-g1-guida-operativa`,
`es/blog/unitree-robotics-chi-e`, `quadrupedi.html`): prezzo o numero concreto nel titolo, meno di 60 caratteri,
un beneficio unico come "listino pubblico" o "assistenza in Italia". Dove compaiono le AI Overviews il CTR
organico è sceso del 58-61% secondo gli studi Ahrefs (febbraio 2026) e Seer
([Search Engine Journal](https://www.pulse.bot/digital-marketing/news/ai-overview-ctr-fell-61-but-clicks-didnt-collapse-via-sejournal-mattgsouthern-a7ef2369-fb1a-480b-bf09-20d55c8c913a/));
conta farsi scegliere tra i pochi clic rimasti. Fatto quando: CTR medio di queste pagine ≥ 3% dopo 4 settimane.

---

## Fase 3: Europa (novembre 2026 - marzo 2027)

Perché: dove abbiamo pagine nella lingua locale e la concorrenza è debole entriamo già tra i primi 10
(Svezia, Danimarca, Rep. Ceca). In molti paesi i rivenditori Unitree sono pochi e hanno siti poveri. Google
raccomanda una pagina per lingua o paese con hreflang reciproco e x-default sulla versione generica
([Search Central, versioni localizzate](https://developers.google.com/search/docs/specialty/international/localized-versions)).

**3.1 x-default sull'inglese.** In tutti gli hreflang: `x-default` verso la versione EN (`en/...-en.html`), non
verso l'italiano. Si fa nei generatori delle pagine tradotte e negli hub. Fatto quando: un controllo
automatico trova hreflang reciproci e x-default EN su tutte le pagine con traduzioni.

**3.2 Pagina del marchio per paese.** `de/unitree.html`, `fr/unitree.html`, `es/unitree.html` e così via:
"Unitree [Deutschland|France|España…]: Händler, Katalog, Preise", con l'impianto di 1.1 tradotto (non
tradotto a macchina riga per riga: termini commerciali locali, IVA del paese, tempi di consegna nel paese).
Collegata dal menu della lingua. Ordine dei paesi in base alle impressioni reali: DE, ES, SE, PL, DK, NL, poi FR,
NO, FI, CZ.

**3.3 Schede dei modelli principali nelle lingue estere.** Oggi all'estero ci sono solo gli hub. Per ogni lingua,
le schede dei modelli base (G1, G1 EDU, Go2 Pro, Go2 EDU, R1, H2, AS2, A2, B2, B2W), circa 10 pagine per lingua,
generate dagli stessi dati delle schede italiane con hreflang reciproco. Niente accessori finché le schede
principali non sono indicizzate.

**3.4 Prezzi e condizioni locali.** Per i paesi fuori dall'euro (PL, SE, DK, NO, CZ) si mostra il prezzo in euro
con il valore indicativo nella valuta locale e la data del cambio. Per ogni paese si indicano IVA e spedizione.
Nello schema `Offer` va `eligibleRegion` con i paesi serviti.

**3.5 Merchant Center per paese [persona per l'account, Claude per il feed].** Claude genera un feed per paese
e lingua (`merchant-feed-de.xml`, ...) dai dati delle schede. Una persona lo registra in Merchant Center. Le schede
gratuite di Shopping occupano posti in prima pagina su "unitree go2 prezzo" in tutti i paesi.

Fatto quando (fase intera): ogni paese target ha pagina del marchio, 7 hub e 10 schede indicizzati, e il
report per paese della Fase 0 mostra impressioni su "unitree [paese]".

---

## Fase 4: autorità (continua, da novembre 2026)

Perché: è il motivo per cui Meko ci sta sopra con meno contenuto. Il traffico e la notorietà del dominio sono
il fattore più legato anche alle citazioni nelle risposte AI, e la maggior parte delle citazioni AI viene da
articoli di terzi ([sintesi di 34 studi sulla ricerca AI 2026](https://jyscauri.substack.com/p/what-34-studies-reveal-about-ai-search)).
Claude non può ottenere link da solo, ma può preparare tutto in modo che una persona debba solo inviare.

**4.1 Dati originali che i giornali possono citare.** Una pagina `osservatorio-prezzi-unitree.html` (IT ed EN):
listino pubblico in euro di tutta la gamma con lo storico dei prezzi, confronto con il prezzo ufficiale in USD,
tempi di consegna in Europa. Si aggiorna ogni mese dal listino del Brain. È il tipo di contenuto che le
testate (HDblog, Wired, Focus, che sono già nei risultati per "unitree") citano con un link.

**4.2 Bozze di contatto [persona per l'invio].** Bozze nella coda Approvazioni del Brain, mai inviate da Claude:
- a Unitree, per l'inserimento nell'elenco dei distributori europei su unitree.com;
- a 5 testate italiane e 2 per ogni paese estero, con il dato dell'osservatorio;
- alle università e ai laboratori clienti, per una pagina "partner/fornitori" con link.

**4.3 Google Business Profile e directory [persona per l'account].** Claude prepara testi, categorie e foto per
Google Business Profile, Europages, Kompass e le directory nazionali di automazione dei paesi target.

**4.4 Video [persona per la pubblicazione].** Nei risultati di "unitree" e "unitree [modello]" ci sono quasi
sempre video. Claude scrive titolo, descrizione con link all'hub e copione per un video per famiglia in italiano
e inglese.

---

## Misura e revisione

- Ogni lunedì: il report della Fase 0 per paese. Se una ricerca della mappa ha 2 o più nostre pagine in
  concorrenza, la si corregge in quella settimana.
- Ogni 4 settimane: per ogni attività chiusa si confronta la metrica del suo "Fatto quando". Se non si è mossa
  dopo 8 settimane, si riapre con un'ipotesi diversa invece di aggiungere altro contenuto.
- Ogni trimestre: si aggiorna la sezione "Dove siamo" di questo file.

Ordine di esecuzione consigliato: 0.1 → 1.1 → 1.2 (fatti il 28/10/2026) → 2.3 → 2.4 → 2.1 → 2.2 → 3.1 →
3.2/3.3 per DE ed ES → 4.1, poi gli altri paesi. La 1.3 si riapre solo se il report lo chiede.
