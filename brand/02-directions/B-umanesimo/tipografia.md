# Tipografia. Territorio B, Misura d'uomo

Due famiglie, entrambe gratuite con licenza SIL Open Font License 1.1 su Google Fonts: si usano sul sito, si incorporano nei PDF generati dal Company Brain, si installano sui computer del team senza costi.

## Le famiglie

### Newsreader: la voce

- **Fonderia**: Production Type (disegno di Production Type per Google Fonts).
- **Licenza**: SIL OFL 1.1, uso commerciale, web e incorporamento nei PDF ammessi. Costo: zero.
- **Perché**: è un serif contemporaneo di costruzione umanista, con dimensioni ottiche da 6 a 72 punti e un corsivo vero, disegnato a parte. Dà ai titoli il tono di un'edizione curata e regge il testo lungo di manuali e preventivi. Nessun concorrente del settore usa un serif da libro: è lo spazio libero rilevato in `01-competitor.md §6`.
- **Pesi in uso**: 300, 400, 500; corsivo 400 e 500. Asse ottico automatico (`font-optical-sizing:auto`).
- **Ruolo**: titoli, testo corrente di documenti e sito, citazioni, didascalie in corsivo, il "Robotics" del marchio esteso.

### Hanken Grotesk: lo strumento

- **Fonderia**: Hanken Design Co. (Alfredo Marco Pradil).
- **Licenza**: SIL OFL 1.1. Costo: zero.
- **Perché**: un grotesk sobrio con la "a" a doppia pancia, la stessa forma del simbolo. Ha cifre tabellari, quindi tiene allineati importi, durate e misure.
- **Pesi in uso**: 400, 500, 600.
- **Ruolo**: interfaccia, pulsanti, etichette, intestazioni di tabella, numeri e unità di misura, piè di pagina.

Il monospaziato non fa parte del sistema. Il codice nei manuali tecnici usa il monospaziato di sistema dell'editor, fuori dall'identità.

### Il logotipo

"abra" è disegnato a mano, costruito con le tre forme del simbolo: non deriva da un carattere esistente e non va mai ricomposto con un font. "Robotics" nel marchio esteso è Newsreader corsivo 400, convertito in tracciati.

## Gerarchia

Valori per il sito (desktop, px) e per i documenti A4 (pt). Interlinea come rapporto.

| Livello | Famiglia e stile | Sito | A4 | Interlinea | Spaziatura | Note |
|-|-|-|-|-|-|-|
| Titolo d'apertura | Newsreader 400, enfasi in corsivo rosso | 88 | 40 | 0,98 | -0,028 em | Una sola parola o frase in corsivo, mai l'intero titolo |
| Titolo di sezione | Newsreader 400 | 48 | 26 | 1,05 | -0,02 em | |
| Sottotitolo | Newsreader 400 | 30 | 17 | 1,2 | -0,01 em | |
| Testo d'apertura | Newsreader 400, ottica 16 | 21 | 12,5 | 1,48 | 0 | |
| Testo corrente | Newsreader 400 | 18 | 10,5 | 1,5 | 0 | Righe da 60 a 75 battute |
| Didascalia | Newsreader corsivo 400 | 15 | 9 | 1,35 | 0 | Grafite |
| Etichetta | Hanken 600, preceduta dal disco | 13 | 8 | 1,2 | +0,02 em | Maiuscolo iniziale, mai tutto maiuscolo |
| Interfaccia e pulsanti | Hanken 500 o 600 | 15 | 9 | 1,2 | 0 | |
| Numeri e misure | Hanken 500, cifre tabellari | 15 | 9 | 1,4 | 0 | Spazio tra numero e unità: "2 kg", "130 cm" |
| Bollino "Esempio" | Hanken 600 maiuscolo | 11 | 7 | 1 | +0,06 em | L'unico maiuscolo del sistema |

## Regole

- Titoli in tondo, con la parte che dice il beneficio in corsivo rosso: "Prova il robot sul tuo caso *prima di investire*". Su rosso il corsivo diventa ocra chiara.
- Allineamento a sinistra, mai giustificato. Niente sillabazione nei titoli.
- Il tutto maiuscolo esiste solo nel bollino "Esempio".
- Unità di misura sempre in Hanken, staccate dal numero con uno spazio non divisibile.
- Il nome si scrive "Abra Robotics" al primo contatto, poi "Abra". Nel testo mai "ABRA".

## Implementazione

```html
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">
```

Per i PDF del Company Brain conviene ospitare i file TTF nel repository (sono OFL: si possono ridistribuire con il file di licenza) e dichiararli con `@font-face`, così Chrome li incorpora nel PDF senza dipendere dalla rete. Font di ripiego: Georgia per Newsreader, Helvetica Neue o Arial per Hanken Grotesk.
