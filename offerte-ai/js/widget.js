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
      if (document.querySelector(`script[src="${src}"]`)) return resolve();
      const s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
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
    await Promise.all([
      loadScript(baseUrl + 'js/prompt-guard.js'),
      loadScript(baseUrl + 'js/kb-search.js'),
      loadScript(baseUrl + 'js/quote-engine.js'),
      loadScript(baseUrl + 'js/offer-builder.js'),
      loadScript(baseUrl + 'js/offer-draft.js'),
      loadScript(baseUrl + 'js/llm-providers.js'),
      loadScript(baseUrl + 'js/rag-chat.js'),
      loadScript(baseUrl + 'js/chat-ui.js'),
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
      ui.appendBot('Ciao! Chiedimi prezzi, tempi di consegna o un preventivo formale — ad esempio sorveglianza con As2.', {});
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
