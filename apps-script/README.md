# Form del sito → Google Sheet + notifica email

Tutti i form del sito (form contatti di home/pagine + box "Richiedi informazioni" delle schede
prodotto) inviano allo **stesso endpoint**. L'endpoint è un Web App Google Apps Script che:
1. scrive una riga nel Google Sheet "Contatti";
2. invia un'email di notifica a ogni nuovo contatto (l'automazione).

## Setup (una volta)

1. **Crea un Google Sheet** (es. "Abra — Contatti sito"). Copia l'**ID** dalla URL:
   `https://docs.google.com/spreadsheets/d/`**`<QUESTO_È_L_ID>`**`/edit`
2. Vai su **https://script.google.com** → **Nuovo progetto**.
3. Incolla il contenuto di `Code.gs` (questa cartella).
4. In alto nel file imposta:
   - `SHEET_ID` = l'ID del foglio del punto 1
   - `NOTIFY_TO` = email dove ricevere le notifiche (es. `gio@abrarobotics.com`)
5. **Distribuisci** → **Nuova distribuzione** → tipo **App web**:
   - *Esegui come*: **Me stesso**
   - *Chi ha accesso*: **Chiunque**
   - **Distribuisci** → autorizza i permessi (Fogli + invio email).
6. Copia l'**URL della Web App** (finisce in `/exec`).
7. Nel sito apri `script.js` (root) e incolla l'URL in **una sola riga**:
   ```js
   window.GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/XXXXX/exec';
   ```
   Tutti i form lo usano automaticamente (anche `prodotti/ecommerce.js` lo legge da lì).
8. Commit + push. Fatto.

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
