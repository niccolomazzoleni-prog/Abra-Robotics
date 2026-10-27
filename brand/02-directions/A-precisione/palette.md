# Palette · Riferimento A

Una palette da strumento di misura: alluminio anodizzato, grafite delle scale incise, bianco della carta da disegno. Due colori di segnale presi dalla norma sulle macchine (IEC 60204-1: verde per lo stato normale, giallo per la condizione che richiede attenzione) e usati con lo stesso significato: il verde marca ciò che è stato misurato e superato, il giallo marca un limite dichiarato. Nessun blu, nessun viola, nessun rosso, nessun grigio caldo.

## Colori

### Primari

| Nome | HEX | RGB | CMYK indicativo | Riferimento | Uso |
|-|-|-|-|-|-|
| Grafite | `#1A2125` | 26, 33, 37 | 80 65 55 75 | vicino a RAL 7021 | testo, logotipo, fondi scuri, filetti principali |
| Alluminio | `#E3E7E9` | 227, 231, 233 | 10 5 5 0 | vicino a RAL 9006 in versione chiara | fondo base del sito, dei post e dei pannelli |
| Bianco disegno | `#F6F8F8` | 246, 248, 248 | 3 1 1 0 | carta naturale bianca | fondo dei documenti, delle tavole e delle targhe |

### Secondari (neutri di servizio)

| Nome | HEX | RGB | CMYK indicativo | Uso |
|-|-|-|-|-|
| Grafite 80 | `#2C353A` | 44, 53, 58 | 75 60 50 55 | pannelli su fondo grafite, testate |
| Grigio quota | `#5C676D` | 92, 103, 109 | 60 45 40 20 | etichette, quote, didascalie |
| Acciaio | `#8A959B` | 138, 149, 155 | 45 30 30 5 | etichette su fondo scuro, grafica, angolari della cassa |
| Linea | `#B4BDC2` | 180, 189, 194 | 30 18 18 0 | filetti sottili e separatori, mai testo |

### Segnali

| Nome | HEX | RGB | CMYK indicativo | Riferimento | Significato |
|-|-|-|-|-|-|
| Verde segnale | `#008351` | 0, 131, 81 | 90 15 80 10 | RAL 6024 verde traffico | misurato, criterio superato, data libera |
| Verde segnale su scuro | `#3DBB82` | 61, 187, 130 | 70 0 60 0 | variante digitale del RAL 6024 | lo stesso segnale su fondo grafite, solo a schermo |
| Giallo limite | `#F1DD38` | 241, 221, 56 | 5 8 85 0 | RAL 1016 giallo zolfo | limite dichiarato (carico, autonomia, ambiente) |

I valori CMYK e i riferimenti RAL sono indicativi: vanno confermati con una prova colore in tipografia e, per la livrea, con il campione RAL del fornitore di vinile.

## Rapporti d'uso

| Colore | Quota indicativa | Note |
|-|-|-|
| Alluminio e Bianco disegno | 60 % | i fondi: alluminio per schermi e post, bianco per carta e tavole |
| Grafite | 28 % | testo, logotipo, testate, flight case |
| Neutri di servizio | 9 % | quote, etichette, filetti |
| Verde segnale | 2 % | solo celle di criterio, spunte, date libere |
| Giallo limite | 1 % | solo il quadratino o la cella del limite dichiarato |

Regole:
- Il logotipo è sempre monocromatico: grafite su chiaro, bianco disegno su grafite. Il triangolo della A non si colora: un triangolo verde accanto a una A si legge come un abete.
- Verde e giallo non stanno mai vicini in grandi superfici e non decorano: se non c'è una misura o un limite, non compaiono.
- Le fotografie e i segnaposto robot vanno in bianco e nero o con colore desaturato; il colore del sistema resta nei segnali.

## Contrasti WCAG 2.2

Calcolati con la formula della luminanza relativa (WCAG 2.2, 1.4.3). Soglie: AA 4,5 : 1 per il testo normale e 3 : 1 per il testo grande; AAA 7 : 1.

| Testo | Fondo | Rapporto | Esito | Uso |
|-|-|-|-|-|
| Grafite `#1A2125` | Alluminio `#E3E7E9` | 13,10 : 1 | AAA | testo e titoli su fondo base |
| Grafite `#1A2125` | Bianco disegno `#F6F8F8` | 15,29 : 1 | AAA | testo nei documenti |
| Grigio quota `#5C676D` | Alluminio `#E3E7E9` | 4,67 : 1 | AA | etichette, didascalie |
| Grigio quota `#5C676D` | Bianco disegno `#F6F8F8` | 5,45 : 1 | AA | etichette nei documenti |
| Bianco disegno `#F6F8F8` | Grafite `#1A2125` | 15,29 : 1 | AAA | testo su fondo scuro |
| Alluminio `#E3E7E9` | Grafite `#1A2125` | 13,10 : 1 | AAA | testo secondario su scuro |
| Acciaio `#8A959B` | Grafite `#1A2125` | 5,32 : 1 | AA | etichette su scuro |
| Bianco `#FFFFFF` | Verde segnale `#008351` | 4,81 : 1 | AA | testo nelle celle "misurato" |
| Verde segnale `#008351` | Bianco disegno `#F6F8F8` | 4,51 : 1 | AA | testo verde su documento |
| Verde segnale `#008351` | Alluminio `#E3E7E9` | 3,87 : 1 | AA solo testo grande | grafica e testo da 24 px in su |
| Verde segnale su scuro `#3DBB82` | Grafite `#1A2125` | 6,70 : 1 | AA | segnale su fondo scuro |
| Grafite `#1A2125` | Giallo limite `#F1DD38` | 11,75 : 1 | AAA | testo nelle celle "limite" |
| Acciaio `#8A959B` | Bianco disegno `#F6F8F8` | 2,87 : 1 | non per testo | solo linee e grafica |
| Linea `#B4BDC2` | Bianco disegno `#F6F8F8` | 1,79 : 1 | non per testo | solo filetti |

Il giallo limite non si usa mai come colore di testo su fondo chiaro (1,3 : 1 su bianco disegno): compare come campitura con testo grafite sopra, oppure come quadratino con un filetto di contorno `#C9B520`.

## Variabili CSS

```css
:root{
  --grafite:#1A2125; --grafite-80:#2C353A;
  --alluminio:#E3E7E9; --bianco:#F6F8F8;
  --quota:#5C676D; --acciaio:#8A959B; --linea:#B4BDC2;
  --verde:#008351; --verde-scuro-fondo:#3DBB82; --giallo:#F1DD38;
}
```
