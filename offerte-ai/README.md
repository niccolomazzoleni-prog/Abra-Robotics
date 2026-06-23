# Assistente Offerte AI (beta)

## Due chat diverse

| | **Lab Training** (interna) | **Widget sito** (pubblica) |
|---|---|---|
| URL locale | http://127.0.0.1:8765/offerte-ai/ | http://127.0.0.1:8765/offerte-ai/demo.html |
| Stile | Tema Platinum olografico (Lab) | Brand Abra viola/bianco |
| Feedback / training | ✅ Sì | ❌ No (solo assistenza visitatori) |
| Chi la usa | Tu / team commerciale | Clienti sul sito |

## Avvio locale

```powershell
.\scripts\deploy-offerte-ai-local.ps1
```

| URL | Cosa fa |
|-----|---------|
| http://127.0.0.1:8765/offerte-ai/ | **Lab Training** — feedback, correzioni, export |
| http://127.0.0.1:8765/offerte-ai/demo.html | Anteprima widget embeddabile sul sito |
| http://127.0.0.1:8765/offerte-ai/offerta.html | Crea offerta PDF |
| http://127.0.0.1:8765/admin/offerte-ai.html | Config LLM + export feedback |

## Come dare feedback e trainare

### 1. Chatta nel Lab
Apri **Lab Training** → fai domande (prezzi, bundle, FAQ).

### 2. Correggi le risposte
Sotto ogni risposta del bot:
- **Utile** / **Non utile**
- **Correggi** → scrivi la risposta giusta
- **+ KB** → mette in coda per la knowledge base

I dati restano in `localStorage` del browser (`abra_feedback_log`).

### 3. Esporta
- Sidebar Lab → **Esporta feedback**
- Oppure Admin → **Esporta feedback.jsonl** / **fine-tune.jsonl** / **KB markdown**

### 4. Merge in knowledge base (RAG)
```powershell
python scripts/merge_feedback_to_kb.py offerte-ai/data/feedback/feedback-export.jsonl
python scripts/build_knowledge_index.py
```

## Setup AI locale (Ollama + Gemma — stesso modello online)

**Prima volta** (installa Ollama, scarica Gemma ~9 GB, crea modello `abra-assistente`):

```powershell
.\scripts\setup-abra-ai-local.ps1
```

Su localhost la chat usa automaticamente `offerte-ai/data/local-ai-config.json` (modalità Ollama, modello `abra-assistente`).

| Step | Comando |
|------|---------|
| Avvio sito + Lab | `.\scripts\deploy-offerte-ai-local.ps1` |
| Training GPU (dopo export feedback) | `.\scripts\train-abra-gemma.ps1 -Dataset finetune-export.jsonl` |
| Solo prompt custom (no GPU) | `.\scripts\train-abra-gemma.ps1 -PromptOnly` |

**Online (stesso modello del PC):** copia `offerte-ai/models/abra-assistente-ft/` sul server, `ollama create abra-assistente-ft -f Modelfile`, avvia `offerte-ai/server/proxy.py`, widget in modalità **Proxy** con la stessa API key.

Google AI Studio è un fallback API cloud — **non** è lo stesso peso del modello Ollama fine-tunato.

### 5. Fine-tuning modello (Gemma locale → Ollama)
1. Lab → **Scarica finetune.jsonl** → copia in `offerte-ai/data/feedback/finetune-dataset.jsonl`
2. `.\scripts\train-abra-gemma.ps1`
3. In Admin imposta modello: `abra-assistente-ft`

Alternativa manuale: [Unsloth](https://github.com/unslothai/unsloth) / [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

## Embed widget sul sito (senza training UI)

```html
<script src="/offerte-ai/js/widget.js" data-base="/offerte-ai/" defer></script>
```

Il widget usa lo stile Abra standard, non il tema Lab Platinum.

## Knowledge base

Dopo `python scripts/build_knowledge_index.py`:

| Fonte | Contenuto |
|-------|-----------|
| `listini/pubblico/end-user.json` | 98 SKU Unitree + prezzi |
| `listini/pubblico/catalogo-manifest.json` | Specs tecniche |
| `data/amr-products.json` | AMR |
| `data/cobot-products.json` | Cobot |
| `index.html` | FAQ sito |
| `offerte-ai/data/knowledge/*.md` | Note vendita custom |

## Pipeline preventivo formale (tua, non AI)

Il PDF/offerta **non** lo genera il modello LLM. Flusso deterministico nel browser:

```
Messaggio utente
  → rag-chat.js (AbraRAGChat.ask)
  → AbraOfferDraft.isFormalRfq()  — regex su testo
  → AbraOfferDraft.build()       — listini + voci-extra + manifest
  → offer-builder.js             — HTML anteprima + PDF
```

- **Lab / widget / sito** usano lo stesso codice (`offer-draft.js` + `offer-builder.js`).
- `preview-sample.html` è solo una pagina demo statica per debug — **non** è la pipeline.
- L'LLM (Ollama/proxy) serve solo al testo conversazionale; i prezzi e le righe vengono dal listino JSON.

## Produzione cloud (compromesso velocità / costo)

| Modalità | Costo | Velocità | Quando usarla |
|----------|-------|----------|---------------|
| **offline** | € 0 | Istantanea | Preventivi formali, prezzi SKU, FAQ — **consigliata default sito** |
| **proxy + Ollama** | ~€25–40/mese VPS | 2–8 s | Risposte narrative + modello fine-tunato `abra-assistente-ft` |
| **DeepSeek API** | ~€0.001/risposta | 1–3 s | Fallback cloud se VPS down |
| **Google Gemma free** | € 0 (limiti) | 2–5 s | Solo dev / basso traffico |

### Deploy sul sito (abrarobotics.com)

1. **Statico** — carica tutto il repo (inclusi `offerte-ai/`, `listini/`, `data/knowledge-index.json`).
2. **Widget** — già in `index.html`:
   ```html
   <script src="/offerte-ai/js/widget.js" data-base="/offerte-ai/" defer></script>
   ```
3. **Config produzione** — `offerte-ai/data/production-ai-config.json`:
   - `mode: "offline"` → zero backend, preventivi funzionano subito.
   - `mode: "proxy"` → punta a `https://ai.abrarobotics.com/v1/chat` (vedi sotto).
4. **Dopo ogni training** — sul server di build:
   ```powershell
   python scripts/merge_feedback_to_kb.py feedback-export.jsonl
   python scripts/build_knowledge_index.py
   ```
   Poi redeploy statico (o solo `knowledge-index.json`).

### VPS AI (proxy + Ollama)

```bash
# Sul VPS (es. Hetzner CPX31 — 4 vCPU, 16 GB RAM)
curl -fsSL https://ollama.com/install.sh | sh
ollama create abra-assistente-ft -f Modelfile   # copiato da training locale

export ABRA_PROXY_KEY="chiave-segreta-lunga"
export OLLAMA_MODEL="abra-assistente-ft"
python offerte-ai/server/proxy.py
```

Nginx: `ai.abrarobotics.com` → proxy porta 8787. In Admin sito imposta **Proxy** + API key.

### Ciclo training consigliato

1. Lab → correggi risposte → export JSONL
2. `merge_feedback_to_kb.py` → arricchisce RAG (effetto immediato, gratis)
3. Opzionale: `train-abra-gemma.ps1` → modello Ollama più “Abra”
4. Redeploy `knowledge-index.json` + modello sul VPS

**Regola pratica:** per RFQ complesse (sorveglianza, PoC) tieni `offline` sul widget pubblico — è più veloce e non sbaglia prezzi. Usa LLM solo dove serve prosa commerciale.
