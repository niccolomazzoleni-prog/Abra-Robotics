# Fix HTTPS su GitHub Pages per abrarobotics.com

## Contesto
Il sito abrarobotics.com è ospitato su GitHub Pages (repo: `niccolomazzoleni-prog/Abra-Robotics`, branch `main`).
Il dominio custom `abrarobotics.com` è configurato nel file `CNAME` del repo.
Il problema: GitHub non ha ancora emesso il certificato SSL - il sito risponde HTTP ma non HTTPS.

## Obiettivo
Abilitare HTTPS enforcement su GitHub Pages via GitHub API, senza aprire il browser.

## Step da eseguire

### 1. Verifica token GitHub
Controlla se `GITHUB_TOKEN` è disponibile nell'ambiente:
```bash
echo $GITHUB_TOKEN
```
Se mancante, cercalo in `~/.gitconfig`, `~/.config/gh/hosts.yml`, o chiedi all'utente di fornirlo con `export GITHUB_TOKEN=xxx`.

### 2. Controlla stato attuale Pages
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/niccolomazzoleni-prog/Abra-Robotics/pages
```
Verifica che `custom_domain` sia `abrarobotics.com` e controlla `https_enforced` e `https_certificate.state`.

### 3. Forza re-save del dominio custom (trigger DNS check)
```bash
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/niccolomazzoleni-prog/Abra-Robotics/pages \
  -d '{"cname":"abrarobotics.com","https_enforced":true}'
```

### 4. Verifica risultato
Ri-esegui il check dello step 2 e conferma che `https_enforced: true`.

Poi testa:
```bash
curl -sI https://abrarobotics.com 2>&1 | head -5
```
Deve rispondere `HTTP/2 200` o `HTTP/1.1 301` (redirect a https).

### 5. Se il cert non è ancora pronto
Il certificato Let's Encrypt può impiegare fino a 24h dopo la prima configurazione.
Se `https_certificate.state` è `pending` o `error`, aspetta 15 minuti e riprova lo step 3.

Se lo stato è `approved` ma HTTPS non funziona ancora, il DNS deve propagarsi completamente.
Verifica:
```bash
dig abrarobotics.com A +short
# Deve mostrare: 185.199.108.153 / 109 / 110 / 111
dig www.abrarobotics.com CNAME +short
# Deve mostrare: niccolomazzoleni-prog.github.io.
```

## Info repo
- Owner: `niccolomazzoleni-prog`
- Repo: `Abra-Robotics`
- Branch Pages: `main`
- Dominio: `abrarobotics.com`
- File CNAME: presente e corretto (con newline)
