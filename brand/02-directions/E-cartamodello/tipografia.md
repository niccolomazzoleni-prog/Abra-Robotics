# Tipografia: Cartamodello (v3)

## Una famiglia, sei tagli statici

**Bricolage Grotesque** (Mathieu Triay, Atelier Triay), licenza **SIL Open Font License 1.1**, costo 0 euro, uso commerciale, web e incorporamento nei PDF consentiti. La licenza non dichiara nomi riservati, quindi le istanze statiche derivate possono portare il nome della famiglia.

Nella v1 il font era variabile e il titolo stava a peso 700 e larghezza 86, con l'effetto "cartellone" e gli ink trap di tendenza notati dai revisori. Nella v2:

- il titolo scende a **peso 640, larghezza 94**, più calmo e meno condensato;
- dal file variabile sono state ricavate **sei istanze statiche TrueType** in `fonts/`, così il Company Brain incorpora nei PDF dei preventivi font veri e non Type 3, e il sito carica file locali senza CDN.

| File | Uso | Peso | Larghezza | Dimensione ottica |
|-|-|-|-|-|
| `BricolageGrotesque-Titolo.ttf` | Display e titoli | 640 | 94 | 72 |
| `BricolageGrotesque-Sottotitolo.ttf` | Sommari, attacchi | 400 | 96 | 24 |
| `BricolageGrotesque-Testo.ttf` | Corpo del testo | 400 | 100 | 14 |
| `BricolageGrotesque-Medio.ttf` | Bottoni, citazioni, enfasi | 560 | 88 | 24 |
| `BricolageGrotesque-Etichetta.ttf` | Etichette in maiuscolo, "Esempio" | 600 | 75 | 14 |
| `BricolageGrotesque-Misura.ttf` | Numeri, quote, prezzi | 680 | 80 | 48 |

Il file variabile è stato spostato in `_lavoro/`, insieme agli script di generazione (fontTools, `instantiateVariableFont`): in `fonts/` restano solo le istanze statiche, così nessun PDF può caricare per errore il variabile e tornare a font Type 3.

## Il marchio non usa il font

Nel logotipo "abra" tutte le lettere sono disegnate a mano con costruzioni geometriche (superellissi, aste calcolate) e convertite in tracciati. La a e la b condividono l'asta nella legatura ab, con la tacca di piega in cima. Solo il descrittore "robotics" deriva da Bricolage Grotesque (peso 470, larghezza 94), con l'altezza x uguale a quella di "abra" e un peso più leggero, così che "abra" resti la parola principale.

## Gerarchia

| Livello | Taglio | Schermo 1440 px | A4 | Interlinea | Spaziatura |
|-|-|-|-|-|-|
| Display | Titolo | 84 a 98 px | 44 a 54 pt | 0,98 | -2% |
| Titolo | Titolo | 23 a 46 px | 18 a 38 pt | 1,05 | -1,2% |
| Sottotitolo | Sottotitolo | 20 a 26 px | 13 a 16 pt | 1,34 | 0 |
| Testo | Testo | 15 a 17 px | 10,5 a 11,5 pt | 1,5 | 0 |
| Etichetta | Etichetta, maiuscolo | 11 a 16 px | 8 a 10,5 pt | 1,2 | +9% |
| Misura | Misura, cifre tabellari | libero | libero | 1 | -1% |

Regole:
- Titoli all'imperativo, in tondo, mai tutto maiuscolo; il maiuscolo è solo per le etichette.
- `font-synthesis:none`: nessun grassetto finto.
- Corpo minimo: 13 px a schermo, 8 pt nei documenti, **6 pt sul biglietto da visita** (26 px nella scala di lavoro 12 px per mm).

## CSS

```css
@font-face{font-family:"Abra Bricolage";src:url(fonts/BricolageGrotesque-Titolo.ttf) format("truetype");font-weight:640;font-stretch:94%}
@font-face{font-family:"Abra Bricolage";src:url(fonts/BricolageGrotesque-Testo.ttf) format("truetype");font-weight:400;font-stretch:100%}
/* altri quattro tagli in assets/sistema.css */
.t-display{font-family:"Abra Bricolage";font-weight:640;font-stretch:94%;letter-spacing:-0.02em;line-height:.98}
```

## Alternativa

Per i manuali tecnici con molte pagine di testo corrente: **Source Serif 4** (OFL) a 10,5 pt per il solo testo; titoli ed etichette restano Bricolage. Fallback di sistema: `system-ui, sans-serif`.
