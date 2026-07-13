# Form del sito → Google Sheet + notifica email

Tutti i form del sito (form contatti di home/pagine + box "Richiedi informazioni" delle schede
prodotto) inviano allo **stesso endpoint**. L'endpoint è un Web App Google Apps Script che:
1. scrive una riga nel Google Sheet "Contatti";
2. invia un'email di notifica a ogni nuovo contatto (l'automazione).

## Setup (una volta)

### Foglio Google (produzione)

Foglio contatti: **https://docs.google.com/spreadsheets/d/15zvBHBRrsnC7b4qB7J3ttp0tXXJg8JFu27m4wXuWccQ/edit**

1. Condividi il foglio con **gio@abrarobotics.com** → permesso **Editor** (se non sei già gio@).
2. Vai su **https://script.google.com** → progetto Abra Web App → incolla `Code.gs` aggiornato.
3. Seleziona **`bootstrapAbraSheet`** → ▶ **Esegui** (account **gio@abrarobotics.com**).
   - Crea tab **Scartati** / **Analytics** se mancano
   - Condivide con gio@ + niccolomazzoleni@gmail.com
   - Copia righe dai fogli legacy (se gio@ ha accesso)
4. **Servizi** (+) → **Google Analytics Data API** → ON
5. **Deploy** → **Gestisci distribuzioni** → matita → **Nuova versione** → Deploy

> **IMPORTANTE — email che non partono:** se crei una *nuova* distribuzione ma l'URL finisce chiedendo login Google, i form del sito **non arrivano** (il browser mostra "inviato" ma il server non riceve nulla). Usa **Gestisci distribuzioni → matita → Nuova versione** sulla Web App esistente con accesso **Chiunque**, oppure verifica in incognito che l'URL `/exec` risponda `Abra Robotics - endpoint form + analytics attivo.` **senza** pagina di login.

### Web App (se partite da zero)

1. **Distribuisci** → **Nuova distribuzione** → **Applicazione web**:
   - *Esegui come*: **Me stesso** (gio@abrarobotics.com)
   - *Chi ha accesso*: **Chiunque**
   - **Distribuisci** → autorizza i permessi (Fogli + invio email).
6. Copia l'**URL della Web App** (finisce in `/exec`).
7. Nel sito `script.js`:
   - `window.GOOGLE_SCRIPT_URL` — deploy **primario** (storico, non rimuovere)
   - `window.GOOGLE_SCRIPT_URL_SECONDARY` — deploy **secondario** in parallelo (Code.gs nuovo)
   - Ogni form invia a **entrambi**; pageview/analytics resta solo sul primario.

## Test
Invia un form dal sito: deve comparire una riga nel foglio **e** arrivare l'email di notifica
entro pochi secondi. In caso di errore, controlla che la distribuzione sia "Chiunque" e che
l'URL finisca in `/exec`.

## Campi salvati
`Data · Nome · Azienda · Ruolo · Email · Telefono · Messaggio · Origine · Pagina · URL`
(`Origine` indica da quale form/scheda arriva il contatto.)

**Dual-write:** ogni contatto valido viene scritto sul foglio **aggregato** (`15zvBH…`) **e** sui fogli legacy di Niccolò (`1nXl0…`, `1XpXE…`), se lo script ha accesso.

## Smoke test

Da terminale (dopo redeploy Web App):
```powershell
powershell -File scripts/smoke-apps-script.ps1
```

In Apps Script editor: esegui **`runSmokeTests`** (loggato come gio@).

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
