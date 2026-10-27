# Tipografia v2: una famiglia, due registri

Il logotipo è disegnato a mano e non usa nessun font (vedi `sistema-grafico.md`). Per tutto il resto la direzione usa una sola famiglia libera, Archivo, in sei istanze statiche: tre larghezze per due registri.

## Famiglia

**Archivo** di Omnibus Type (Héctor Gatti e team). Licenza SIL Open Font License 1.1, senza nomi riservati: uso commerciale, web, incorporamento nei PDF e modifica consentiti, costo zero. Il testo della licenza è in `font/OFL.txt`.

File in `font/`, istanze statiche ricavate con fontTools dal file variabile ufficiale (google/fonts), così Chrome e il Company Brain incorporano TrueType veri nei PDF:

| File | Larghezza | Peso | Uso |
|-|-|-|-|
| `Archivo-Regular.ttf` | 100 | 400 | Testo |
| `Archivo-Italic.ttf` | 100 | 400 corsivo | Didascalie e limiti |
| `Archivo-SemiBold.ttf` | 100 | 600 | Enfasi, voci di elenco |
| `Archivo-Bold.ttf` | 100 | 700 | Titoli dei documenti e del sito |
| `ArchivoCondensed-ExtraBold.ttf` | 75 | 800 | Titoli di scena, solo eventi e social |
| `ArchivoExpanded-SemiBold.ttf` | 125 | 600 | Etichette e descrittore "ROBOTICS" |

Nessun CDN: `sistema.css` dichiara tutti i file in locale.

Alternativa commerciale, solo se servirà più carattere nei titoli di scena: GT America di Grilli Type (larghezze Compressed, Condensed, Standard, Extended), costo indicativo da verificare sul listino della fonderia. Non serve per far funzionare il sistema.

## Due registri

| Registro | Titoli | Testo | Etichette |
|-|-|-|-|
| **Documento**: preventivi, post aziendali, biglietto, scheda laboratorio, sito | Archivo Bold 700, interlinea 1,02 | Archivo Regular | Archivo Expanded, maiuscolo, spaziatura 0,12 em |
| **Scena**: reel, totem, livrea, schermi in fiera | Archivo Condensed ExtraBold 800, interlinea 0,9 | Archivo Regular e SemiBold | Archivo Expanded |

La didascalia (corsivo tra parentesi) vale in entrambi i registri: è la forma tipografica dei limiti dichiarati e dei segnaposto. Esempio: *(Batteria circa 2 ore: nel pilota è previsto un cambio a metà turno.)*

## Gerarchia

### Documento (A4 a 96 dpi)

| Livello | Dimensione | Voce |
|-|-|-|
| Titolo di copertina | 46 px (circa 34 pt) | Bold |
| Titolo di capitolo | 38 px (circa 28 pt) | Bold |
| Testo corrente | 12,5 a 13 px (circa 9,5 pt) | Regular |
| Tabelle | 10,5 a 11 px (circa 8 pt) | Regular |
| Etichette, intestazioni | 7,5 a 10 px | Expanded |

### Sito (1440 px)

| Livello | Dimensione | Voce |
|-|-|-|
| H1 | 64 a 72 px | Bold |
| Testo guida | 20 px | Regular |
| Testo | 16 a 18 px | Regular |
| Etichetta | 12 a 13 px | Expanded |

### Scena (1080 px e totem)

| Livello | Dimensione | Voce |
|-|-|-|
| Titolo reel | 112 a 128 px | Condensed ExtraBold |
| Titolo totem | 104 px (10 cm in stampa) | Condensed ExtraBold |
| Battuta del copione | 36 px | SemiBold |
| Testo | 22 a 25 px | Regular |

### Biglietto da visita

Corpo minimo 6,2 pt (26 px nel mockup a 12 px per mm): nome 68 px, ruolo e contatti 28 px, riga del fronte 26 px.

## Regole

- Titoli in tondo minuscolo, mai tutto maiuscolo.
- La Condensed non entra mai in un preventivo o in un post aziendale.
- Il magenta non colora parole dentro i titoli.
- Cifre tabellari per importi, settimane e misure.
- Il logotipo e il descrittore si usano sempre dai file in `logo/`.
