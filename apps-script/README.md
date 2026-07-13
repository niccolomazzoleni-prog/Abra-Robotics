# Form del sito → Google Sheet + notifica email

Tutti i form del sito (form contatti di home/pagine + box "Richiedi informazioni" delle schede
prodotto) inviano allo **stesso endpoint**. L'endpoint è un Web App Google Apps Script che:
1. scrive una riga nel Google Sheet "Contatti";
2. invia un'email di notifica a ogni nuovo contatto (l'automazione).

## Setup (una volta)

### Foglio Google (account gio@)

1. Vai su **https://script.google.com** → progetto Abra Web App.
2. Incolla il contenuto aggiornato di `Code.gs`.
3. Nel menu funzioni seleziona **`setupAbraSheetForGio`** → ▶ **Esegui** (loggato come **gio@abrarobotics.com**).
4. Autorizza i permessi → in **Visualizza → Log** trovi l’URL del foglio nuovo (tab Contatti, Scartati, Analytics).
5. **Deploy** → **Gestisci distribuzioni** → matita → **Nuova versione** → Deploy.

Il foglio si chiama *Abra Robotics — Contatti sito (gio@abrarobotics.com)* ed è di proprietà di gio@.
Niccolò (`niccolomazzoleni@gmail.com`) viene aggiunto come editor automaticamente.

### Web App (se partite da zero)

1. **Distribuisci** → **Nuova distribuzione** → **Applicazione web**:
   - *Esegui come*: **Me stesso** (gio@abrarobotics.com)
   - *Chi ha accesso*: **Chiunque**
   - **Distribuisci** → autorizza i permessi (Fogli + invio email).
6. Copia l'**URL della Web App** (finisce in `/exec`).
7. Nel sito `script.js` → `window.GOOGLE_SCRIPT_URL` (già configurato se usi il deploy Abra).

## Test
Invia un form dal sito: deve comparire una riga nel foglio **e** arrivare l'email di notifica
entro pochi secondi. In caso di errore, controlla che la distribuzione sia "Chiunque" e che
l'URL finisca in `/exec`.

## Campi salvati
`Data · Nome · Azienda · Ruolo · Email · Telefono · Messaggio · Origine · Pagina · URL`
(`Origine` indica da quale form/scheda arriva il contatto.)

## Estensioni possibili dell'automazione
Nel `doPost`, dopo l'invio email, si può aggiungere: webhook Slack/Telegram, invio a
Make/Zapier, creazione lead in un CRM, autorisposta automatica al cliente.

---

# Statistiche sito (admin `/admin/statistiche.html`)

La dashboard admin legge dati da **due fonti**:

1. **Google Analytics 4** — property `541272624` (measurement `G-T4ZC7CM8RX`) via Analytics Data API
2. **Pageview first-party** — beacon dal sito → foglio Google **Analytics** (tab nel Sheet contatti)

## Setup analytics (una volta, dopo il form)

1. Nel **Google Sheet** esistente (`SHEET_ID` in `Code.gs`) verifica che esista il tab **Analytics**  
   (viene creato automaticamente al primo pageview dopo il redeploy).
2. In **Apps Script** → icona **Servizi** (+) → aggiungi **Google Analytics Data API** → ON.
3. **Deploy** → **Manage deployments** → matita sulla Web App → **New version** → **Deploy**  
   (serve una nuova versione dopo ogni modifica a `Code.gs`).
4. Autorizza i permessi aggiuntivi se richiesti (Analytics + Fogli).
5. Apri **https://abrarobotics.com/admin/statistiche.html** (password admin) → **Aggiorna**.

### Endpoint stats (JSONP)

```
GET .../exec?action=stats&key=abra2026stats&callback=abraStatsCb
```

Chiave di default: `abra2026stats`. Per cambiarla: Script Property `ABRA_STATS_KEY` in Apps Script.

### Cosa vedi nella dashboard

| Sezione | Contenuto |
|---------|-----------|
| KPI | Utenti attivi, pageview, sessioni, nuovi utenti, eventi (GA4) + pageview beacon |
| Top pagine GA4 | Ultimi 30 giorni da Google Analytics |
| Canali acquisizione | Organic, Direct, Social, ecc. |
| Pageview first-party | Path e referrer salvati nel foglio Analytics |
| Tracking installato | GA4, GTM, Meta Pixel, GSC, sitemap |

### Se GA4 mostra "da collegare"

- Servizio **Google Analytics Data API** non abilitato in Apps Script, oppure
- Web App non ridistribuita con la versione aggiornata di `Code.gs`, oppure
- L'account Google dello script non ha accesso alla property GA4 (stesso account Analytics).

### Search Console

Invia manualmente in GSC → Sitemap: `https://abrarobotics.com/sitemap.xml`
