# Dati privati vs sito pubblico

## Cosa resta pubblico (serve al sito)

- Pagine HTML, CSS, JS, immagini
- `listini/pubblico/end-user.json` (prezzi vendita)
- URL Web App form in `script.js` (solo l’endpoint `…/exec`)
- Stripe publishable key + Payment Link (normali in frontend)

## Cosa resta sul PC (gitignore)

| Percorso | Contenuto |
|----------|-----------|
| `listini/interno/` | FOB, Gold, audit margini, confronti competitor |
| `offerte-ai/samples/` | Preventivi nominativi HTML/PDF |
| `admin/` | Tool interni listini / immagini / publish |
| `data/admin-auth.json` | Hash password admin |
| `apps-script/Code.gs` | Sheet ID, email notify (il deploy live resta su Google) |
| `.env*` / AI locale / feedback | Segreti e training locale |

**Traccia operativa:** continui a modificarli in queste cartelle locali. Per backup/versioning sicuro, crea una repo GitHub **privata** tipo `Abra-Robotics-interno` e fai push solo di queste cartelle — **non** mescolarle di nuovo nella repo del sito.

## Commit vecchi

`.gitignore` e `git rm --cached` **non cancellano la storia**: i file sensibili restano nei commit già pushati finché qualcuno clona/forka la repo pubblica.

Opzioni:

1. **Repo → Private** (nasconde a chi non ha accesso; la history resta per chi aveva già clonato)
2. **Nuova repo privata “pulita”** senza history + migrate hosting (Vercel/Pages) — più sicuro
3. **Rewrite history** (`git filter-repo` / BFG) sulla repo attuale — distruttivo, richiede force-push e collaborazione

Finché la repo è pubblica, considera i preventivi/sheet ID già esposti come **compromessi a livello di riservatezza** (non necessariamente di password).
