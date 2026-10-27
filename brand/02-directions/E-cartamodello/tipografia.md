# Tipografia: Cartamodello

## Una famiglia, larghezze su misura

**Bricolage Grotesque**, variabile su tre assi: peso 200 a 800, larghezza 75 a 100, dimensione ottica 12 a 96. Disegnata da Mathieu Triay (Atelier Triay), pubblicata su Google Fonts.

- **Licenza**: SIL Open Font License 1.1. Uso commerciale, web, incorporamento nei PDF e modifica consentiti senza costi. Il file e la licenza sono in `fonts/` (`BricolageGrotesque-VF.ttf`, `OFL.txt`).
- **Costo**: 0 euro.
- **Perché**: è un grotesk con carattere, lontano dal grotesk neutro di categoria (Helvetica, Inter, Diatype). Gli ink trap nei pesi alti sembrano le tacche di un cartamodello. L'asse della larghezza permette di comporre "su misura": il titolo si stringe per stare nella colonna invece di andare a capo male, le etichette usano la larghezza 75 come le scritte a pennarello sui pezzi di carta.
- **Una sola famiglia** semplifica il lavoro del team: un file da caricare nel sito statico, un file da incorporare nel PDF del Company Brain.

Nel logotipo le lettere "bra" e la parola "Robotics" partono dalle forme di Bricolage, sono convertite in tracciati e spaziate a mano; la A è disegnata da zero. Il marchio non richiede il font installato.

## Gerarchia

Valori per schermo a 1440 px e per A4. Il parametro `opsz` segue la dimensione.

| Livello | Uso | Peso | Larghezza | Corpo schermo | Corpo A4 | Interlinea | Spaziatura |
|-|-|-|-|-|-|-|-|
| Display | Titoli hero, post, copertine | 700 | 86 | 88 a 112 px | 44 a 62 pt | 0,95 | -1,2% |
| Titolo | Titoli di sezione | 680 | 86 | 24 a 46 px | 19 a 38 pt | 1,02 | -1,5% |
| Sottotitolo | Attacchi, sommari | 420 | 96 | 20 a 26 px | 13 a 16 pt | 1,32 | 0 |
| Testo | Corpo | 400 | 100 | 15 a 17 px | 10,5 a 11,5 pt | 1,5 | 0 |
| Etichetta | Nomi dei pezzi, intestazioni di tabella, "Esempio" | 600 | 75 | 11 a 16 px, maiuscolo | 8 a 10,5 pt | 1,2 | +9% |
| Misura | Numeri del metro, quote, prezzi | 640 | 75 | libero | libero | 1 | -1%, cifre tabellari |

Regole:
- Titoli all'imperativo, in tondo, mai tutto maiuscolo. Il maiuscolo è riservato alle etichette.
- Le cifre in tabella usano `font-feature-settings: "tnum"`.
- Il corsivo non esiste nella famiglia: per le citazioni si usa il peso 560 a larghezza 88 tra virgolette basse « ».
- Corpo minimo a schermo 13 px; nei documenti stampati 8 pt per le note.

## CSS di base

```css
@font-face{font-family:"Bricolage Grotesque";src:url(fonts/BricolageGrotesque-VF.ttf) format("truetype");font-weight:200 800;font-stretch:75% 100%}
.t-display{font-weight:700;font-stretch:86%;font-variation-settings:"opsz" 96;letter-spacing:-0.012em;line-height:.95}
.t-etichetta{font-weight:600;font-stretch:75%;text-transform:uppercase;letter-spacing:.09em}
```

## Alternativa e fallback

- Se in futuro servisse un secondo carattere per testi lunghi (manuali tecnici di 80 pagine): **Source Serif 4** (OFL, Adobe) a corpo 10,5 pt, solo per il testo corrente dei manuali.
- Fallback di sistema: `system-ui, sans-serif`.
- Nessun font commerciale necessario.
