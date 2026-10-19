# Revisione editoriale dei post del blog (italiano)

Brief per chi (persona o agente) rivede i post in `blog/*.html`. L'obiettivo è che ogni post si
legga come lo scriverebbe un giornalista tecnico di robotica con vent'anni di mestiere: fatti
verificati, frasi concrete, niente riempitivo. I post italiani sono la fonte delle traduzioni,
quindi ogni correzione qui si propaga alle 11 lingue.

## Cosa NON fare

- **Non inventare.** Niente esperienze sul campo, clienti, casi, tempi di consegna, aneddoti o
  numeri che non abbiano una fonte (scheda ufficiale Unitree/Fairino, listino, documento citato).
  Se un dato non si verifica, si toglie: non si attenua con "circa" o "secondo alcuni".
- **Prezzi solo da `listini/pubblico/end-user.json`** (cobot: `data/cobot-products.json`). Mai
  ricalcolare o arrotondare in modo diverso. AS2 Pro e AS2-W restano "su preventivo".
- Non cambiare slug, struttura HTML, classi, id, `product-strip`, `article-cta`, immagini.
  Non aggiungere sezioni nuove. Si può togliere un paragrafo o una domanda FAQ inutile.
- Niente git: niente commit, branch o push.

## Cosa correggere

1. **Contraddizioni.** Testo, tabelle, card prodotto, FAQ e JSON-LD devono dire la stessa cosa.
   Se il testo dice che il modello d'ingresso è l'R1 Air, la card mostra l'R1 Air.
   Se due prezzi sembrano non tornare (es. robot + workstation ≠ cella), si spiega in una frase
   cosa include il prezzo più alto, guardando la scheda in `prodotti/`.
2. **Fatti da verificare.** Specifiche, date e nomi si controllano sulla fonte citata
   (WebFetch sulla pagina ufficiale). Versioni che non esistono a listino (es. "G1 Pro") si tolgono.
3. **Ripetizioni.** La FAQ non copia il corpo parola per parola: risposta di 1-3 frasi, autonoma,
   con il dato essenziale. Lo stesso fatto non compare più di due volte nel post (corpo + FAQ).
   Via le frasi meta ("Questa pagina raccoglie...", "In questa guida vediamo...") e i doppioni.
4. **Link.** Al massimo un link per destinazione nel testo (card e CTA escluse). Niente frasi che
   elencano più di tre link: si tiene il più utile.
5. **Gergo e calchi.**
   - "sviluppo secondario" (calco del cinese 二次开发) → "sviluppo software proprio" o
     "programmazione con SDK"; nelle card prodotto → "SDK" (es. "SDK, 23 DoF, dock di calcolo").
   - "investimento angelico" → "il capitale di un business angel".
   - Articoli: "l'Unitree G1", "dell'H2", "l'R1" (non "il Unitree", "del H2", "il R1").
   - Niente "fondamentale", "cruciale", "a 360 gradi", "panorama", "rivoluzionario", "vale la pena".
6. **"Filiera Unitree Italia".** È il posizionamento ufficiale di Abra (pagina Chi siamo): si usa
   al massimo una volta per post, nella forma "parte della filiera di distribuzione di Unitree
   Italia", e solo dove risponde a "dove si compra". Altrove basta "Abra Robotics".
7. **Tempo.** Oggi è il 19 ottobre 2026. Frasi come "consegne dal 2026" o "uscirà nel 2026"
   vanno riscritte al presente o al passato, se la fonte lo consente; altrimenti "a ottobre 2026
   la fonte indica...".
8. **Fonti.** Wikipedia non basta per dati societari o economici: se c'è una fonte primaria
   (sito Unitree, Borsa di Shanghai, stampa economica) si usa quella, altrimenti il dato si toglie.
   Il link di ogni fonte deve corrispondere alla data e al contenuto citati.
9. **Stile.** Una idea per frase, verbi concreti, numeri con unità. Niente lineette lunghe (—),
   niente punti esclamativi, niente domande retoriche nel corpo. Tono da rivista tecnica, non da
   brochure: si dicono anche i limiti ("non ha grado IP", "non è un robot domestico").

## Dopo ogni post

- Aggiorna `dateModified` nel JSON-LD a `2026-10-19` e la data "Aggiornato" visibile.
- La FAQ nel JSON-LD (`FAQPage`) deve essere identica, domanda per domanda, alla FAQ visibile.
- Controlla che l'HTML sia valido: `python -I -c "import html.parser,sys;html.parser.HTMLParser().feed(open(sys.argv[1],encoding='utf-8').read())" blog/<slug>.html`
  e che il JSON-LD si parsifichi (`json.loads` su ogni blocco `application/ld+json`).
- Scrivi un registro delle modifiche (vedi sotto) per chi aggiornerà le traduzioni.

## Registro delle modifiche

Un file per post: `<cartella indicata>/<slug>.md`, con elenco puntato:
`- [tipo] prima: "..." → dopo: "..."` (tipo = fatto, prezzo, ripetizione, gergo, link, stile, tolto).
Serve a riportare le stesse modifiche nelle 11 traduzioni senza ritradurre tutto.

## Glossario per le traduzioni

| Italiano | en | de | fr | es | pl | nl | cs | sv | da | no | fi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sviluppo software proprio / con SDK | custom software development (SDK) | eigene Softwareentwicklung (SDK) | développement logiciel sur SDK | desarrollo de software propio (SDK) | własne oprogramowanie (SDK) | eigen softwareontwikkeling (SDK) | vlastní vývoj softwaru (SDK) | egen mjukvaruutveckling (SDK) | egen softwareudvikling (SDK) | egen programvareutvikling (SDK) | oma ohjelmistokehitys (SDK) |
| nelle card: "SDK" | SDK | SDK | SDK | SDK | SDK | SDK | SDK | SDK | SDK | SDK | SDK |
| dock di calcolo | compute dock | Rechenmodul | module de calcul | módulo de cálculo | moduł obliczeniowy | rekenmodule | výpočetní modul | beräkningsmodul | beregningsmodul | beregningsmodul | laskentamoduuli |
