/**
 * Widget chat embeddabile — stile messenger + feedback.
 */
(function () {
  'use strict';

  if (window.AbraChatWidget) return;

  const script = document.currentScript;
  const base = (script && script.getAttribute('data-base')) || '/offerte-ai/';
  const baseUrl = base.endsWith('/') ? base : base + '/';

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[src="${src}"]`);
      if (existing) {
        if (existing.dataset.abraLoaded === '1') return resolve();
        existing.addEventListener('load', () => resolve(), { once: true });
        existing.addEventListener('error', () => reject(new Error(src)), { once: true });
        return;
      }
      const s = document.createElement('script');
      s.src = src;
      s.onload = () => { s.dataset.abraLoaded = '1'; resolve(); };
      s.onerror = () => reject(new Error('Script non caricato: ' + src));
      document.head.appendChild(s);
    });
  }

  async function loadScriptsSequential(files) {
    for (const file of files) {
      await loadScript(baseUrl + 'js/' + file);
    }
  }

  function ensureStyles() {
    if (document.querySelector('link[data-abra-chat]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = baseUrl + 'css/offerte-ai.css?v=20260714chat';
    link.setAttribute('data-abra-chat', '1');
    document.head.appendChild(link);
  }

  function siteAsset(path) {
    return baseUrl.replace(/offerte-ai\/$/i, '') + path;
  }

  async function boot() {
    if (window.__abraWidgetBooted) return;
    window.__abraWidgetBooted = true;
    ensureStyles();
    await loadScriptsSequential([
      'prompt-guard.js',
      'kb-search.js',
      'quote-engine.js',
      'offer-builder.js',
      'offer-draft.js',
      'llm-providers.js',
      'rag-chat.js',
      'chat-ui.js',
    ]);
    await AbraLLM.bootstrapLocalConfig();

    const logoUrl = siteAsset('images/chat-g1-face.png');

    const launcher = document.createElement('button');
    launcher.className = 'abra-chat-launcher';
    launcher.type = 'button';
    launcher.title = 'Assistente Abra — prezzi e info';
    launcher.setAttribute('aria-label', 'Apri assistente Abra');
    launcher.innerHTML = `
      <span class="abra-chat-launcher-ring" aria-hidden="true"></span>
      <span class="abra-chat-launcher-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" focusable="false">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
      </span>
      <img class="abra-chat-launcher-logo" src="${logoUrl}" alt="" width="34" height="34" loading="lazy">
    `;

    const panel = document.createElement('div');
    panel.className = 'abra-chat-panel';
    panel.innerHTML = '<div id="abra-widget-root"></div>';

    document.body.appendChild(launcher);
    document.body.appendChild(panel);

    const rag = new AbraRAGChat({
      indexUrl: baseUrl + 'data/knowledge-index.json',
      pricesUrl: baseUrl + '../listini/pubblico/end-user.json',
      rulesUrl: baseUrl + 'data/offerte-regole.json',
    });

    let ui = null;
    let ready = false;

    launcher.addEventListener('click', () => {
      panel.classList.toggle('open');
      if (panel.classList.contains('open') && ui) {
        ui.inputEl?.focus();
      }
    });

    ui = new AbraChatUI(panel.querySelector('#abra-widget-root'), {
      title: 'Assistente Abra',
      subtitle: 'Listino End-User · IVA esclusa',
      avatarLogoUrl: logoUrl,
      showFeedback: false,
      suggestions: ['Quanto costa Go2 EDU?', 'Prezzo G1-U1', 'Tempi di consegna'],
      onSend: async (q) => rag.ask(q),
    });

    rag.init().then(() => {
      ready = true;
      ui.setStatus('Online', true);
      ui.appendBot(
        'Ciao! Posso aiutarti con:\n\n' +
        '• **Prezzi** dal listino pubblico aggiornato (es. «Quanto costa Go2 EDU?», «G1-U1»)\n' +
        '• **Confronti** tra modelli e **tempi di consegna**\n\n' +
        'Per un preventivo su misura usa **WhatsApp** o il **modulo contatto** qui sotto.',
        {}
      );
    }).catch(err => {
      ui.appendBot('Errore: ' + err.message, {});
    });

    window.AbraChatWidget.close = () => panel.classList.remove('open');
    window.AbraChatWidget.open = () => { panel.classList.add('open'); ui?.inputEl?.focus(); };
  }

  window.AbraChatWidget = { boot };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
