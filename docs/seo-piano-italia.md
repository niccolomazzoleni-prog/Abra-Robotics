# Piano SEO: primi in Italia

Scritto il 09/11/2026. Viene prima delle fasi 3 e 4 di `seo-piano-europa-2027.md`: finché l'Italia non è
a posto, le sessioni Claude lavorano qui. Le regole per chi esegue sono le stesse del piano Europa (una PR
per attività, pagine prodotto dai generatori, prezzi solo dal listino, richiesta di indicizzazione dopo ogni
deploy). Le attività segnate **[persona]** le fa Gio o Nico; Claude prepara il materiale.

## Cosa vuol dire "primi"

Su "unitree" da solo unitree.com, Wikipedia e YouTube restano sopra qualsiasi rivenditore. "Primi in Italia" vuol
dire quindi:

- **1° su "unitree italia"** e primo rivenditore su "unitree";
- **top 3 su "unitree [modello] prezzo"** per G1, Go2, R1, H2, B2, A2 e AS2, e su "cane robot prezzo" e
  "robot umanoide prezzo";
- **primo rivenditore su "unitree [modello]"**, cioè sopra Meko, Generation Robots e Drone-store.

Tappe:
- entro il 31/12/2026: "unitree italia" ≤ 3 e tutte le ricerche "[modello] prezzo" con impressioni in Italia;
- entro il 31/03/2027: 1° su "unitree italia" e sopra Meko su 8 delle 12 ricerche di `seo-sopra-meko.md`;
- entro il 30/06/2027: top 3 su tutte.

## Dove siamo (Search Console, Italia, dal 11/10 al 07/11/2026)

1.142 impressioni e 30 clic in Italia, di cui 22 sulla ricerca "abra robotics". Il resto del traffico viene
dall'estero.

| Ricerca | Posizione | Impressioni | Note |
|---|---|---|---|
| unitree italia | 6,2 | 54 | 0 clic |
| unitree g1 prezzo | 6,5 | 28 | 0 clic |
| cane robot prezzo | 10,3 | 124 | la ricerca generica più vista |
| quanto costa il cane robot | 9,6 | 27 | |
| unitree r1 | 8,8 | 6 | |
| unitree a2 | 16,3 | 43 | |
| unitree go2 edu | 18,9 | 64 | |
| unitree b2 | 36,4 | 49 | |
| unitree g1 | 46,0 | 46 | |
| unitree go2 | 49,6 | 47 | |
| robot umanoide prezzo | 34,0 | 3 | |
| unitree go2/r1/h2/b2/a2 prezzo, unitree as2 | nessuna impressione | 0 | Meko è 1°-3° |

Indicizzazione delle 153 pagine italiane della sitemap: 125 indicizzate. Le pagine "scansionate ma non
indicizzate" sono 13:
- blog: `finanziamento-robot-industria-40`, `poc-robot-umanoide-azienda`, `umanoidi-vs-robotica-tradizionale`;
- landing: `lp-amr`, `lp-cobot`, `lp-unitree`;
- prodotti: `cobot-fairino-fr16`, `cobot-fairino-fr5`, `cobot-fairino-palletizing-fr10`,
  `cobot-fairino-palletizing-fr20`, `unitree-d1-arm`, `unitree-go2w-u4`, `unitree-go2w-u5`.

Cosa blocca, in ordine di peso:
1. Le correzioni principali non sono online: PR #73 (pagina del marchio), #71 (hreflang), #77 (home e link interni).
2. Sulle ricerche con "prezzo" non compariamo: nessuna pagina risponde in modo chiaro a "quanto costa il [modello]".
3. Sui nomi dei modelli siamo oltre la 35ª posizione: pagine in concorrenza tra loro e poca autorità rispetto a Meko.
4. Ci sono pagine povere che Google scarta, e questo pesa su tutto il sito.

## Attività, nell'ordine

**IT-0 [persona] Pubblicare le PR aperte.** Unire #73, #71 e #77 (e #74 e #76 se approvate). Poi Claude richiede
l'indicizzazione di home, `catalogo-unitree` e degli hub, in quest'ordine.
Fatto quando: le tre PR sono su `main` e il sito pubblicato le contiene.

**IT-1 "unitree italia" dalla 6ª alla 1ª posizione.** `catalogo-unitree` è la pagina del marchio (PR #73).
Bisogna aggiungere:
- un link dalla home e da ogni hub italiano con il testo "Unitree Italia";
- un titolo sotto i 60 caratteri con un vantaggio concreto, per esempio "listino pubblico" o "assistenza in Italia";
- nelle prime righe: chi siamo, cosa vendiamo, consegna e assistenza in Italia.

"Rivenditore ufficiale" si scrive solo se è vero e documentato. **[persona]** Il profilo Google Business di
Abra Robotics deve avere un link a `catalogo-unitree`.
Fatto quando: posizione media in Italia ≤ 3 dopo 4 settimane dalla pubblicazione.

**IT-2 Gli hub di modello rispondono a "prezzo".** Hub: `g1`, `go2`, `r1`, `h2`, `b2`, `a2`, `as2`. Non si
creano pagine nuove per il prezzo, perché si farebbero concorrenza con quelle che esistono. In ogni hub:
- titolo e H1 con "prezzo", per esempio "Unitree Go2 prezzo in Italia: listino 2026";
- nelle prime 2 righe, il prezzo di partenza dal listino;
- una tabella delle versioni con prezzo, a chi serve e consegna;
- dati strutturati Product/Offer con il prezzo del listino;
- link dalle guide `cane-robot-prezzo` e `robot-umanoide-prezzo`, con il nome del modello come testo.

È l'attività 2.2 del piano Europa, fatta prima e solo in italiano.
Fatto quando: ogni "unitree [modello] prezzo" ha impressioni in Italia dopo 4 settimane e posizione ≤ 10 dopo 8.

**IT-3 `blog/cane-robot-prezzo` dalla 10ª alla 5ª posizione.** È l'attività 2.3 del piano Europa. Vale anche per
"quanto costa il cane robot" (posizione 9,6).
Fatto quando: posizione media in Italia ≤ 6 dopo 4 settimane.

**IT-4 CTR delle pagine già in prima pagina.** È l'attività 2.4 del piano Europa, applicata a "unitree italia" e a
"unitree g1 prezzo": siamo in 6ª posizione e prendiamo 0 clic.
Fatto quando: CTR ≥ 3% dopo 4 settimane.

**IT-5 Pagine italiane povere.** È l'attività 2.1 del piano Europa, applicata alle 13 pagine "scansionate ma non
indicizzate" elencate in "Dove siamo". Per ognuna si decide se:
- riscriverla con contenuto vero (specifiche ufficiali, casi d'uso, FAQ);
- unirla a una pagina più forte con un redirect 301;
- metterla in `noindex` e toglierla dalla sitemap.
Le landing `lp-*` per gli annunci restano in `noindex`.
Fatto quando: nessuna pagina italiana "scansionata ma non indicizzata" nella sitemap.

**IT-6 Autorità in Italia** (**[persona]** per i contatti; Claude prepara testi e pagine).
- Link da siti italiani: università e centri di ricerca clienti (una pagina caso studio per chi lo permette),
  riviste di settore (Innovation Post è primo su "cane robot prezzo": proporre un articolo con dati veri),
  associazioni e fiere, competence center Industria 4.0.
- Ogni caso studio è una pagina del sito, collegata dall'hub del modello.
Fatto quando: 10 domini italiani nuovi nel rapporto Link di Search Console entro il 31/03/2027.

## Misura

- Ogni lunedì: `company-brain/seo-monitor/posizioni_italia.py` da WSL (posizioni Italia sulle ricerche qui sopra,
  ultimi 28 giorni), più `report_unitree.py`. Il report settimanale (`run_weekly.sh`) va messo in cron in WSL:
  al 09/11/2026 non ha mai girato.
- Ogni 4 settimane: audit di indicizzazione delle pagine italiane (URL Inspection API) e confronto con la
  tabella "Dove siamo"; si aggiorna la tabella.
- Se una metrica non si muove dopo 8 settimane, si riapre l'attività con un'ipotesi diversa.

Ordine: IT-0 → IT-1 → IT-2 → IT-3 → IT-4 → IT-5, con IT-6 in parallelo. Le fasi 3 e 4 del piano Europa
ripartono quando "unitree italia" è ≤ 3 e IT-2 ha impressioni su tutte le ricerche "prezzo".
