/**
 * Widget chat del sito — launcher + pannello, caricato da script.js su tutte le pagine.
 *
 * Come risponde (in quest'ordine):
 *  1. AbraSiteAnswers (site-answers.js): prezzi dal listino pubblico listini/pubblico/end-user.json,
 *     famiglie prodotto, consegne, contatti — istantaneo, deterministico, nessun prezzo inventato.
 *  2. Motore RAG esistente (rag-chat.js): risposte consulenziali (PoC, assistenza), preventivi formali,
 *     e — se configurato un LLM (proxy/Ollama/…) — risposta generativa con il system prompt di llm-providers.js.
 *  3. Estratto dalla knowledge base pubblica, altrimenti rimando a WhatsApp / call / modulo.
 *
 * Il motore pesante (knowledge-index.json + script RAG) si carica solo alla prima interazione.
 */
(function () {
  'use strict';

  if (window.AbraChatWidget) return;

  const VERSION = '20260930';
  const script = document.currentScript;
  const base = (script && script.getAttribute('data-base')) || '/offerte-ai/';
  const baseUrl = new URL(base.endsWith('/') ? base : base + '/', location.href).href;
  const siteRoot = new URL('../', baseUrl).href;
  // offer-draft.js carica config/voci da offerte-ai/data/ anche quando il widget gira fuori dal Lab
  if (!window.ABRA_OFFERTE_BASE) window.ABRA_OFFERTE_BASE = baseUrl;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const existing = document.querySelector('script[data-abra-src="' + src + '"]');
      if (existing) {
        if (existing.dataset.abraLoaded === '1') return resolve();
        existing.addEventListener('load', () => resolve(), { once: true });
        existing.addEventListener('error', () => reject(new Error(src)), { once: true });
        return;
      }
      const s = document.createElement('script');
      s.src = src;
      s.async = false;
      s.dataset.abraSrc = src;
      s.onload = () => { s.dataset.abraLoaded = '1'; resolve(); };
      s.onerror = () => reject(new Error('Script non caricato: ' + src));
      document.head.appendChild(s);
    });
  }

  async function loadScriptsSequential(files) {
    for (const file of files) {
      await loadScript(baseUrl + 'js/' + file + '?v=' + VERSION);
    }
  }

  function ensureStyles() {
    if (document.querySelector('link[data-abra-chat]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = baseUrl + 'css/chat-widget.css?v=' + VERSION;
    link.setAttribute('data-abra-chat', '1');
    document.head.appendChild(link);
  }

  function postLead(payload) {
    if (typeof window.postLeadToGoogleScripts === 'function') return window.postLeadToGoogleScripts(payload);
    const url = window.GOOGLE_SCRIPT_URL || 'https://script.google.com/macros/s/AKfycbw1WeoJYZltyorwQ-8Nftg0DdiOXOV-Zl3MlRegJS2ybhAzaRaqZNpTRamEbHJe2NtK/exec';
    const body = new URLSearchParams(Object.entries(payload || {}).map(e => [e[0], String(e[1])])).toString();
    return fetch(url, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body,
    });
  }

  const RFQ_LONG = /preventivo|offerta formale|quotazione|intestat|\bpoc\b|proof of concept|integrazion|sorveglianz|perlustraz|termocamer|payload|pick.?place|noleggi/i;

  async function boot() {
    if (window.__abraWidgetBooted) return;
    window.__abraWidgetBooted = true;
    ensureStyles();
    await loadScriptsSequential(['site-answers.js', 'chat-widget-ui.js']);

    const C = window.AbraSiteAnswers.CONTACT;
    const answers = new window.AbraSiteAnswers();
    const pricesUrl = siteRoot + 'listini/pubblico/end-user.json';

    // --- caricamento dati (lazy) ---
    let pricesP = null;
    let engineP = null;
    const loadPrices = () => (pricesP = pricesP || answers.load(pricesUrl).catch(err => { pricesP = null; throw err; }));
    const loadEngine = () => (engineP = engineP || (async () => {
      await loadScriptsSequential([
        'prompt-guard.js', 'kb-search.js', 'quote-engine.js', 'offer-builder.js',
        'offer-draft.js', 'llm-providers.js', 'rag-chat.js',
      ]);
      if (window.AbraLLM && window.AbraLLM.bootstrapLocalConfig) await window.AbraLLM.bootstrapLocalConfig();
      const rag = new window.AbraRAGChat({
        indexUrl: baseUrl + 'data/knowledge-index.json',
        pricesUrl,
        rulesUrl: baseUrl + 'data/offerte-regole.json',
      });
      await rag.init();
      answers.kb = rag.kb;
      return rag;
    })().catch(err => { engineP = null; throw err; }));
    const warmUp = () => { loadPrices().catch(() => {}); loadEngine().catch(() => {}); };

    function offerCard(offer) {
      const D = window.AbraOfferDraft;
      if (!offer || !D) return null;
      let total = '';
      try {
        const t = D.builder && D.builder.recalculate ? D.builder.recalculate(offer) : null;
        const alternatives = (t && ((t.opzioni && t.opzioni.length > 1) || (t.gruppi && t.gruppi.length > 1)));
        if (t && t.subtotal && !alternatives) total = window.AbraSiteAnswers.formatEuro(t.subtotal);
      } catch (_) {}
      const card = document.createElement('div');
      card.className = 'abra-cw-offer';
      card.innerHTML = '<div><span>Preventivo indicativo · ' + (offer.line_items || []).length + ' righe</span>' +
        (total ? '<strong>' + total + ' IVA esclusa</strong>' : '') + '</div>';
      if (D.downloadPdf) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'abra-cw-btn abra-cw-btn-sm';
        btn.textContent = 'Scarica PDF';
        btn.addEventListener('click', () => { try { D.saveSession && D.saveSession(offer); D.downloadPdf(offer); } catch (_) {} });
        card.appendChild(btn);
      }
      return card;
    }

    async function onSend(q) {
      // 1) risposte istantanee dal listino
      try { await loadPrices(); } catch (_) { /* listino non raggiungibile: si prova col motore */ }
      const local = answers.ready ? answers.answer(q) : null;
      if (local) {
        loadEngine().catch(() => {});
        return local;
      }

      // 2) motore RAG / LLM
      let engine = null;
      try { engine = await loadEngine(); } catch (_) {}
      if (!engine) return { reply: answers.notFound(), actions: [{ type: 'contact', label: 'Lascia i tuoi contatti' }] };

      const cfg = window.AbraLLM ? window.AbraLLM.loadConfig() : { mode: 'offline' };
      const words = q.split(/\s+/).filter(Boolean).length;

      try {
        const guard = window.AbraPromptGuard ? window.AbraPromptGuard.analyzeInput(q) : { cleanQuery: q, flags: {} };
        if (guard.flags && guard.flags.severe) {
          return { reply: window.AbraPromptGuard.hardRefusal(guard.flags, '') };
        }
        const kbHits = engine.kb.search(engine._expandSearchQuery(guard.cleanQuery || q), 8);
        const consulting = engine._tryConsultingReply(q, kbHits);
        if (consulting) return { reply: consulting };

        if (cfg.mode !== 'offline' || (RFQ_LONG.test(q) && words >= 6)) {
          const r = await engine.ask(q);
          if (r && r.offerDraft && window.AbraOfferDraft) {
            return {
              reply: window.AbraOfferDraft.formatChatIntro(r.offerDraft) +
                '\n\nPer confermarlo o adattarlo al tuo caso: [WhatsApp](' +
                window.AbraSiteAnswers.waUrl('Ciao Abra Robotics, vorrei confermare il preventivo generato in chat') +
                ') · [Prenota una call](' + C.BOOKING_URL + ')',
              card: offerCard(r.offerDraft),
            };
          }
          if (cfg.mode !== 'offline' && r && r.reply) return { reply: r.reply };
        }
      } catch (_) { /* si ripiega sulla KB */ }

      const kb = answers.kbAnswer(q);
      if (kb) return { reply: kb };
      return { reply: answers.notFound(), actions: [{ type: 'contact', label: 'Lascia i tuoi contatti' }] };
    }

    const HISTORY_KEY = 'abra_cw_history_v1';
    const history = (() => {
      try { return JSON.parse(sessionStorage.getItem(HISTORY_KEY) || '[]').filter(m => m && typeof m.t === 'string'); } catch (_) { return []; }
    })();
    const saveHistory = () => {
      try { sessionStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(-24))); } catch (_) { /* storage non disponibile */ }
    };

    const ui = new window.AbraChatWidgetUI({
      title: 'Assistente Abra',
      subtitle: 'Online · prezzi dal listino pubblico',
      logoUrl: siteRoot + 'images/chat-g1-face.png',
      linkBase: siteRoot,
      chips: [
        { label: 'Prezzi umanoidi', q: 'Prezzi umanoidi' },
        { label: 'Prezzi quadrupedi', q: 'Prezzi quadrupedi' },
        { label: 'Tempi di consegna', q: 'Tempi di consegna' },
        { label: 'Parla con un tecnico', q: 'Parla con un tecnico' },
      ],
      contact: {
        waUrl: window.AbraSiteAnswers.waUrl('Ciao Abra Robotics, vorrei informazioni'),
        bookingUrl: C.BOOKING_URL,
        privacyUrl: siteRoot + 'privacy-policy.html',
        submit: postLead,
      },
      onFirstIntent: warmUp,
      onOpen: warmUp,
      onSend: async q => {
        const res = await onSend(q);
        history.push({ r: 'u', t: q });
        if (res && res.reply) history.push({ r: 'b', t: res.reply, a: res.actions || null });
        saveHistory();
        return res;
      },
    });

    ui.addBot(
      'Ciao! Sono l\'assistente di **Abra Robotics**, parte della filiera di distribuzione di Unitree Italia.\n' +
      'Chiedimi un prezzo — es. «quanto costa il G1?» o «prezzo H2-D» — e ti rispondo subito con cifra e link alla scheda.'
    );
    // conversazione della sessione: resta disponibile quando si apre una scheda prodotto dal link in chat
    history.forEach(m => (m.r === 'u' ? ui.addUser(m.t) : ui.addBot(m.t, { actions: m.a || [] })));

    window.AbraChatWidget.open = () => ui.open();
    window.AbraChatWidget.close = () => ui.close();
    window.AbraChatWidget.ask = q => ui.send(q);
    window.AbraChatWidget.ui = ui;
  }

  window.AbraChatWidget = { boot, version: VERSION };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => boot().catch(err => console.warn('[AbraChat]', err)));
  } else {
    boot().catch(err => console.warn('[AbraChat]', err));
  }
})();
