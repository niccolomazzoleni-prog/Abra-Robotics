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
    link.href = baseUrl + 'css/offerte-ai.css';
    link.setAttribute('data-abra-chat', '1');
    document.head.appendChild(link);
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

    const launcher = document.createElement('button');
    launcher.className = 'abra-chat-launcher';
    launcher.type = 'button';
    launcher.title = 'Chat Abra Robotics';
    launcher.setAttribute('aria-label', 'Apri chat');
    launcher.innerHTML = '💬';

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
      subtitle: 'Prodotti & preventivi',
      showFeedback: false,
      suggestions: ['Prezzo Go2 EDU', 'G1-U1', 'Tempi consegna'],
      onSend: async (q) => rag.ask(q),
    });

    rag.init().then(() => {
      ready = true;
      ui.setStatus('Online', true);
      ui.appendBot('Ciao! Chiedimi prezzi o un preventivo. Oppure **WhatsApp** / **Modulo contatto** in basso.', {});
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
