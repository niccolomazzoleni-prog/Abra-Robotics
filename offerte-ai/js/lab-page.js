/**
 * Lab Training — sidebar, export, quiz esperto, test bot.
 */
(function () {
  'use strict';

  const SUGGESTIONS = [
    'G1 in ordine di costo',
    'PoC pick-place scatole A→B: R1-D vs G1-D vs G1 bipede',
    'Preventivo formale PoC manifattura R1-D',
    'Assistenza e riparazione: costi e tempi',
  ];

  const MODE_LABELS = {
    offline: 'Offline (RAG gratis)',
    ollama: 'Ollama · Gemma locale',
    google: 'Google AI free tier',
    openai: 'OpenAI API',
    deepseek: 'DeepSeek API',
    proxy: 'Proxy sicuro',
  };

  const TRAINING_MODE_KEY = 'abra_lab_training_mode';

  let rag, ui;
  let trainingMode = localStorage.getItem(TRAINING_MODE_KEY) || 'bot-test';
  let pendingScenario = null;

  function refreshSidebar() {
    const cfg = AbraLLM.loadConfig();
    const modeEl = document.getElementById('sb-mode');
    modeEl.textContent = MODE_LABELS[cfg.mode] || cfg.mode;
    modeEl.title = cfg.mode === 'ollama' ? `${cfg.ollamaUrl} · ${cfg.ollamaModel}` : '';

    const fb = AbraFeedbackStore.all();
    document.getElementById('sb-fb').textContent = fb.length;
    document.getElementById('sb-kb-pending').textContent = AbraFeedbackStore.pendingKb().length;

    document.querySelectorAll('[data-training-mode]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.trainingMode === trainingMode);
    });
    const modeHint = document.getElementById('sb-training-mode-hint');
    if (modeHint) {
      modeHint.textContent = trainingMode === 'expert-quiz'
        ? 'Quiz: rispondi tu come consulente Abra'
        : 'Test bot: chiedi e correggi la risposta AI';
    }
  }

  function setTrainingMode(mode) {
    trainingMode = mode;
    localStorage.setItem(TRAINING_MODE_KEY, mode);
    pendingScenario = null;
    refreshSidebar();
    AbraUI.toast(mode === 'expert-quiz' ? 'Modalità Quiz esperto' : 'Modalità Test bot', 'info');
  }

  function showScenario(scenario) {
    pendingScenario = scenario;
    ui.appendBot(
      `**🎭 Cliente simulato** · ${scenario.industry}\n\n${scenario.question}\n\n` +
      '— *Scrivi sotto la risposta che darebbe un consulente Abra (prezzi, step, raccomandazioni).*',
      { isScenario: true }
    );
    ui.inputEl?.focus();
    document.getElementById('lab-mobile-bar')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function startRandomScenario() {
    if (!global.AbraTrainingScenarios) {
      return AbraUI.toast('Modulo scenari non caricato', 'warn');
    }
    showScenario(AbraTrainingScenarios.generate());
  }

  function startSeedScenario() {
    if (!global.AbraTrainingScenarios) return;
    showScenario(AbraTrainingScenarios.nextSeed());
  }

  async function handleExpertAnswer(text) {
    const scenario = pendingScenario;
    pendingScenario = null;
    const fbId = 'fb-' + Date.now().toString(36);
    const entry = {
      id: fbId,
      timestamp: new Date().toISOString(),
      question: scenario.question.replace(/\n\n_.*_$/, ''),
      answer: '(risposta generata da consulente — quiz)',
      correction: text,
      sources: [],
      quote: null,
      model_mode: 'expert-quiz',
      rating: 1,
      action: 'expert_quiz',
      scenario_meta: scenario.meta || {},
    };
    AbraFeedbackStore.save(entry);
    AbraFeedbackStore.queueForKb(entry);
    refreshSidebar();
    return {
      reply:
        '✓ **Risposta esperto salvata** e messa in coda knowledge.\n\n' +
        'Puoi generare un altro scenario dal pannello **Training** o passare a **Test bot** per verificare cosa risponderebbe l’AI.\n\n' +
        '_Tip: da mobile usa **Copia feedback**; da PC **Scarica pacchetto** + `merge_feedback_to_kb.py`._',
      sources: [],
      quote: null,
    };
  }

  async function handleSend(q) {
    if (trainingMode === 'expert-quiz' && pendingScenario) {
      return handleExpertAnswer(q);
    }
    return rag.ask(q);
  }

  function bindSidebar() {
    document.querySelectorAll('[data-training-mode]').forEach(btn => {
      btn.addEventListener('click', () => setTrainingMode(btn.dataset.trainingMode));
    });

    document.getElementById('sb-scenario-random')?.addEventListener('click', () => {
      setTrainingMode('expert-quiz');
      startRandomScenario();
    });
    document.getElementById('sb-scenario-seed')?.addEventListener('click', () => {
      setTrainingMode('expert-quiz');
      startSeedScenario();
    });
    document.getElementById('lab-btn-scenario')?.addEventListener('click', startRandomScenario);
    document.getElementById('lab-btn-seed')?.addEventListener('click', startSeedScenario);

    document.getElementById('sb-export-all').addEventListener('click', () => {
      const pack = AbraFeedbackStore.exportTrainingPack();
      if (!pack.feedback) {
        return AbraUI.toast('Nessun feedback — valuta o completa almeno un quiz', 'warn');
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

    document.getElementById('sb-copy-feedback')?.addEventListener('click', async () => {
      const jsonl = AbraFeedbackStore.exportJsonl();
      if (!jsonl) return AbraUI.toast('Nessun feedback da copiare', 'warn');
      try {
        await navigator.clipboard.writeText(jsonl);
        AbraUI.toast('Feedback copiato — incollalo in un file .jsonl sul PC', 'ok');
      } catch {
        AbraFeedbackStore.download('feedback-export.jsonl', jsonl, 'application/x-ndjson');
        AbraUI.toast('Download avviato (clipboard non disponibile)', 'info');
      }
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
      pendingScenario = null;
      ui.messagesEl.innerHTML = '';
      ui.appendBot(
        'Nuova conversazione.\n\n' +
        '**Test bot:** fai una domanda → **Da correggere** o **Integra in knowledge**.\n' +
        '**Quiz esperto:** genera uno scenario cliente e rispondi tu.',
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
      onSend: handleSend,
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
        ? 'Modalità **offline** (solo listini).'
        : `Modalità **${MODE_LABELS[cfg.mode] || cfg.mode}** attiva.`;

      ui.appendBot(
        '**Lab Training** — due modalità:\n\n' +
        '1. **Test bot** — chiedi come un cliente, correggi la risposta\n' +
        '2. **Quiz esperto** — scenario casuale, rispondi tu → va in knowledge\n\n' +
        aiNote + '\n\n' +
        'Da **cellulare**: https://abrarobotics.com/offerte-ai/ (password admin)',
        {}
      );
    } catch (err) {
      ui.appendBot('Errore avvio: ' + err.message, {});
      ui.setStatus('Offline', false);
    }
  }

  if (window.AbraAdmin?.whenUnlocked) window.AbraAdmin.whenUnlocked(init);
  else init();
})();
