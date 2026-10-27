# Tipografia: una famiglia, tre larghezze

La segnaletica dei grandi eventi culturali lavora con poche lettere molto grandi e molte lettere piccolissime, leggibili da lontano. Prova generale ottiene questo contrasto con una sola famiglia variabile, usata su tre larghezze: stretta per i titoli di scena, normale per il testo, larga per le etichette. Il ritmo nasce dal passaggio tra le larghezze, e il team gestisce un solo file di font.

## Famiglia

**Archivo** (Omnibus Type, Héctor Gatti e team), font variabile con due assi: larghezza da 62 a 125 e peso da 100 a 900, in tondo e corsivo.

- Licenza: SIL Open Font License 1.1. Uso commerciale, web, incorporamento nei PDF e modifica consentiti, costo zero.
- File nella cartella: `font/Archivo-VF.ttf`, `font/Archivo-Italic-VF.ttf`, `font/OFL.txt` (scaricati dal repository ufficiale google/fonts).
- Web: stessi file con `@font-face` (vedi `sistema.css`) oppure Google Fonts (`family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900`).
- PDF dal Company Brain: Chrome headless incorpora il TTF variabile con le istanze usate. Verificato sui mockup del preventivo.

Alternativa commerciale, solo se un giorno serve più carattere nei titoli: **GT America** di Grilli Type (famiglia con larghezze Compressed, Condensed, Standard, Extended), licenza desktop più web per una piccola azienda, costo indicativo tra 1.000 e 1.500 euro da verificare sul listino della fonderia. Il sistema non ne ha bisogno: Archivo resta la scelta raccomandata.

## Le tre voci

| Voce | Impostazione CSS | Uso |
|-|-|-|
| **Titolo di scena** | `font-stretch:68%; font-weight:800; line-height:.9` | Headline, numeri delle fasi (P0 a P5), nomi delle unità sui flight case, nome sul biglietto |
| **Testo** | `font-stretch:100%; font-weight:400` (600 per enfasi) | Paragrafi, tabelle, voci di elenco |
| **Etichetta** | `font-stretch:125%; font-weight:600; uppercase; letter-spacing:.14em` | Sezioni, date, didascalie di servizio, segnaletica |
| **Didascalia** | corsivo, `font-stretch:90%; font-weight:400`, sempre tra parentesi | Limiti dichiarati, indicazioni di regia, segnaposto |

La didascalia è la forma tipografica della franchezza: nei copioni teatrali le indicazioni di regia stanno in corsivo tra parentesi, e in Abra lo stesso stile porta i limiti del robot nella stessa pagina delle prestazioni. Esempio: *(Batteria circa 2 ore: nel pilota è previsto un cambio a metà turno.)*

## Gerarchia

### Scena (web 1440 px, social, totem)

| Livello | Dimensione | Interlinea | Voce |
|-|-|-|-|
| H1 hero | 96 a 128 px | 0,9 | Titolo di scena |
| H1 social 1080 | 108 a 138 px | 0,9 | Titolo di scena |
| H2 | 56 a 64 px | 0,95 | Titolo di scena |
| Numero di fase | 40 px | 0,9 | Titolo di scena |
| Testo guida | 20 a 25 px | 1,4 | Testo |
| Testo | 16 a 18 px | 1,5 | Testo |
| Etichetta | 12 a 17 px | 1,3 | Etichetta |
| Didascalia | 13 a 18 px | 1,4 | Didascalia |

### Documento (A4, 96 dpi)

| Livello | Dimensione | Interlinea | Voce |
|-|-|-|-|
| Titolo di copertina | 74 px (circa 55 pt) | 0,9 | Titolo di scena |
| Titolo di capitolo | 46 px (circa 34 pt) | 0,9 | Titolo di scena |
| Numero di fase in tabella | 26 px | 0,9 | Titolo di scena |
| Testo corrente | 12,5 px (circa 9,5 pt) | 1,55 | Testo |
| Tabella | 10,5 px (circa 8 pt) | 1,4 | Testo |
| Intestazioni e piè di pagina | 8 a 9,5 px | 1,3 | Etichetta |

## Regole

- I titoli di scena sono in tondo, mai tutto maiuscolo: la forma minuscola tiene il tono calmo anche a 130 px.
- Una parola o una frase del titolo può passare in Luce (su Velluto) per indicare il beneficio: "prima di investire", "dal primo giorno".
- Le etichette larghe non superano mai le 8 parole.
- Cifre tabellari (`font-feature-settings:"tnum"`) per importi, settimane e misure.
- Il logotipo non si compone con il font: si usano sempre i file in `logo/`, dove la A è disegnata a mano e il resto della parola è convertito in tracciati con spaziatura corretta.
