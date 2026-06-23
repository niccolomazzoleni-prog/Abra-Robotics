/**
 * Lab Training — sidebar, export, test AI.
 */
(function () {
  'use strict';

  const SUGGESTIONS = [
    'Prezzo G1-U1',
    'Go2 EDU per università',
    'Preventivo formale sorveglianza As2 con termocamera e sensori gas',
    'MiR250 quanto costa?',
    'Tempi consegna umanoidi',
    'Finanziamenti Industria 4.0',
  ];

  const MODE_LABELS = {
    offline: 'Offline (RAG gratis)',
    ollama: 'Ollama · Gemma locale',
    google: 'Google AI free tier',
    deepseek: 'DeepSeek API',
    proxy: 'Proxy sicuro',
  };

  let rag, ui;

  function refreshSidebar() {
    const cfg = AbraLLM.loadConfig();
    const modeEl = document.getElementById('sb-mode');
    modeEl.textContent = MODE_LABELS[cfg.mode] || cfg.mode;
    modeEl.title = cfg.mode === 'ollama' ? `${cfg.ollamaUrl} · ${cfg.ollamaModel}` : '';

    const fb = AbraFeedbackStore.all();
    document.getElementById('sb-fb').textContent = fb.length;
    document.getElementById('sb-kb-pending').textContent = AbraFeedbackStore.pendingKb().length;
  }

  function bindSidebar() {
    document.getElementById('sb-export-all').addEventListener('click', () => {
      const pack = AbraFeedbackStore.exportTrainingPack();
      if (!pack.feedback) {
        return AbraUI.toast('Nessun feedback — valuta almeno una risposta in chat', 'warn');
      }
      const saved = [];
      AbraFeedbackStore.download('feedback-export.jsonl', pack.feedback, 'application/x-ndjson');
      saved.push('feedback');
      if (pack.finetune) {
        AbraFeedbackStore.download('finetune-export.jsonl', pack.finetune, 'application/x-ndjson');
        saved.push('finetune');
      }
      if (pack.kbMd) {
        AbraFeedbackStore.download('feedback-knowledge.md', pack.kbMd, 'text/markdown');
        saved.push('knowledge');
      }
      AbraUI.toast(`Scaricati: ${saved.join(', ')}`, 'ok');
    });

    document.getElementById('sb-test-ai').addEventListener('click', async () => {
      const btn = document.getElementById('sb-test-ai');
      btn.disabled = true;
      btn.textContent = '…';
      const r = await AbraLLM.testConnection({});
      AbraUI.toast(r.ok ? ('AI OK: ' + (r.preview || '').slice(0, 60)) : ('AI errore: ' + r.error), r.ok ? 'ok' : 'warn');
      btn.disabled = false;
      btn.textContent = 'Test AI';
      refreshSidebar();
    });

    document.getElementById('sb-clear-chat').addEventListener('click', () => {
      rag.clearHistory();
      ui.messagesEl.innerHTML = '';
      ui.appendBot(
        'Nuova conversazione. Fai una domanda, poi sotto la risposta scegli **Va bene**, **Da correggere** o **Integra in knowledge**.',
        {}
      );
      AbraUI.toast('Chat resettata', 'info');
    });
  }

  async function init() {
    AbraUI.mountNav('chat');

    rag = new AbraRAGChat({
      indexUrl: 'data/knowledge-index.json',
      pricesUrl: '../listini/pubblico/end-user.json',
      rulesUrl: 'data/offerte-regole.json',
    });

    ui = new AbraChatUI('#chat-root', {
      title: 'Abra Lab',
      subtitle: 'Training · feedback · KB',
      avatarLetter: '✦',
      variant: 'thread',
      theme: 'platinum',
      feedbackMode: 'lab',
      suggestions: SUGGESTIONS,
      onSend: async (q) => rag.ask(q),
      onFeedback: refreshSidebar,
    });

    bindSidebar();

    try {
      await rag.init();
      await AbraLLM.bootstrapLocalConfig();
      const idx = await fetch('data/knowledge-index.json').then(r => r.json());
      document.getElementById('sb-kb').textContent = idx.chunk_count + ' chunk';
      refreshSidebar();
      ui.setStatus('Online', true);

      const cfg = AbraLLM.loadConfig();
      const aiNote = cfg.mode === 'offline'
        ? 'Modalità **offline** (solo listini, nessun Gemma).'
        : `Modalità **${MODE_LABELS[cfg.mode] || cfg.mode}** attiva.`;

      ui.appendBot(
        'Benvenuto nel **Lab Training**.\n\n' +
        '**Come funziona:** fai una domanda → sotto ogni risposta compare *Com\'è andata questa risposta?* con tre scelte.\n\n' +
        aiNote + '\n\n' +
        'Se chiedi un prezzo compare la **card preventivo** → clic → **Crea offerta PDF**.',
        {}
      );
    } catch (err) {
      ui.appendBot('Errore avvio: ' + err.message, {});
      ui.setStatus('Offline', false);
    }
  }

  init();
})();
