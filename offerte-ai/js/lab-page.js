/**
 * Lab Training — Test bot vs Quiz esperto (= domanda cliente casuale, rispondi tu).
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

  function updateComposeUi() {
    if (!ui) return;
    if (trainingMode === 'expert-quiz' && pendingScenario) {
      ui.setComposePlaceholder('Risposta consulente Abra al cliente sopra…');
      ui.setComposeHint('Quiz: la tua risposta → knowledge · Prossima = altra domanda casuale');
    } else if (trainingMode === 'expert-quiz') {
      ui.setComposePlaceholder('Caricamento domanda cliente…');
      ui.setComposeHint('Quiz esperto — domanda casuale in arrivo');
    } else {
      ui.setComposePlaceholder('Scrivi come farebbe un cliente…');
      ui.setComposeHint('Test bot: chiedi → valuta la risposta AI');
    }
  }

  function refreshSidebar() {
    const cfg = AbraLLM.loadConfig();
    document.getElementById('sb-mode').textContent = MODE_LABELS[cfg.mode] || cfg.mode;

    const fb = AbraFeedbackStore.all();
    document.getElementById('sb-fb').textContent = fb.length;
    document.getElementById('sb-kb-pending').textContent = AbraFeedbackStore.pendingKb().length;

    document.querySelectorAll('[data-training-mode]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.trainingMode === trainingMode);
    });

    const modeHint = document.getElementById('sb-training-mode-hint');
    if (modeHint) {
      modeHint.textContent = trainingMode === 'expert-quiz'
        ? 'Domanda cliente casuale — rispondi tu (il bot vendite è spento)'
        : 'Chiedi come un cliente e correggi la risposta AI';
    }

    const nextBtn = document.getElementById('sb-quiz-next');
    if (nextBtn) nextBtn.hidden = trainingMode !== 'expert-quiz';

    updateComposeUi();
  }

  /** Quiz esperto = scenario cliente casuale (sempre). */
  function enterQuizMode(kind) {
    trainingMode = 'expert-quiz';
    localStorage.setItem(TRAINING_MODE_KEY, 'expert-quiz');
    pendingScenario = null;
    refreshSidebar();
    if (kind === 'seed') startSeedScenario();
    else startRandomScenario();
  }

  function enterBotTestMode() {
    trainingMode = 'bot-test';
    localStorage.setItem(TRAINING_MODE_KEY, 'bot-test');
    pendingScenario = null;
    refreshSidebar();
    AbraUI.toast('Test bot — chiedi come un cliente', 'info');
  }

  function showScenario(scenario) {
    pendingScenario = scenario;
    trainingMode = 'expert-quiz';
    localStorage.setItem(TRAINING_MODE_KEY, 'expert-quiz');

    ui.appendBot(
      `**🎭 Cliente** · ${scenario.industry}\n\n${scenario.question}\n\n` +
      '✏️ **Rispondi tu** qui sotto (consulente Abra: prezzi, step, raccomandazione).',
      { isScenario: true, labSystem: true }
    );

    refreshSidebar();
    ui.inputEl?.focus();
    ui.scrollBottom?.();
  }

  function startRandomScenario() {
    if (!global.AbraTrainingScenarios) {
      return AbraUI.toast('Modulo scenari non caricato — ricarica la pagina', 'warn');
    }
    showScenario(AbraTrainingScenarios.generate());
    AbraUI.toast('Domanda cliente casuale', 'info');
  }

  function startSeedScenario() {
    if (!global.AbraTrainingScenarios) return;
    showScenario(AbraTrainingScenarios.nextSeed());
    AbraUI.toast('Domanda curata Abra', 'info');
  }

  function scheduleNextRandom(delayMs = 1400) {
    setTimeout(() => {
      if (trainingMode === 'expert-quiz' && !pendingScenario) startRandomScenario();
    }, delayMs);
  }

  async function handleExpertAnswer(text) {
    const scenario = pendingScenario;
    if (!scenario) {
      startRandomScenario();
      return { silent: true };
    }

    pendingScenario = null;
    const entry = {
      id: 'fb-' + Date.now().toString(36),
      timestamp: new Date().toISOString(),
      question: scenario.question.replace(/\n\n_.*_$/, ''),
      answer: '(risposta consulente — quiz)',
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
    scheduleNextRandom();

    return {
      reply:
        '✓ **Salvato in knowledge** · in coda: ' + AbraFeedbackStore.pendingKb().length + '\n\n' +
        '_Tra poco appare la **prossima domanda casuale** — oppure tocca **Prossima**._',
      skipFeedback: true,
      labSystem: true,
    };
  }

  async function handleSend(q) {
    if (trainingMode === 'expert-quiz') {
      if (pendingScenario) return handleExpertAnswer(q);
      startRandomScenario();
      return { silent: true };
    }
    return rag.ask(q);
  }

  function bindSidebar() {
    document.querySelectorAll('[data-training-mode="bot-test"]').forEach(btn => {
      btn.addEventListener('click', enterBotTestMode);
    });
    document.querySelectorAll('[data-training-mode="expert-quiz"]').forEach(btn => {
      btn.addEventListener('click', () => enterQuizMode('random'));
    });

    document.getElementById('sb-quiz-next')?.addEventListener('click', () => enterQuizMode('random'));
    document.getElementById('sb-scenario-seed')?.addEventListener('click', () => enterQuizMode('seed'));
    document.getElementById('lab-btn-seed')?.addEventListener('click', () => enterQuizMode('seed'));
    document.getElementById('lab-btn-quiz')?.addEventListener('click', () => enterQuizMode('random'));

    document.getElementById('sb-export-all').addEventListener('click', () => {
      const pack = AbraFeedbackStore.exportTrainingPack();
      if (!pack.feedback) return AbraUI.toast('Nessun feedback ancora', 'warn');
      AbraFeedbackStore.download('feedback-export.jsonl', pack.feedback, 'application/x-ndjson');
      if (pack.kbMd) AbraFeedbackStore.download('feedback-knowledge.md', pack.kbMd, 'text/markdown');
      AbraUI.toast('Training scaricato', 'ok');
    });

    document.getElementById('sb-copy-feedback')?.addEventListener('click', async () => {
      const jsonl = AbraFeedbackStore.exportJsonl();
      if (!jsonl) return AbraUI.toast('Nessun feedback', 'warn');
      try {
        await navigator.clipboard.writeText(jsonl);
        AbraUI.toast('Feedback copiato', 'ok');
      } catch {
        AbraFeedbackStore.download('feedback-export.jsonl', jsonl, 'application/x-ndjson');
      }
    });

    document.getElementById('sb-test-ai')?.addEventListener('click', async () => {
      const btn = document.getElementById('sb-test-ai');
      btn.disabled = true;
      const r = await AbraLLM.testConnection({});
      AbraUI.toast(r.ok ? 'AI OK' : ('Errore: ' + r.error), r.ok ? 'ok' : 'warn');
      btn.disabled = false;
      refreshSidebar();
    });

    document.getElementById('sb-clear-chat')?.addEventListener('click', () => {
      rag.clearHistory();
      pendingScenario = null;
      ui.messagesEl.innerHTML = '';
      if (trainingMode === 'expert-quiz') {
        ui.appendBot('Nuova sessione quiz — domanda casuale in arrivo…', { labSystem: true });
        setTimeout(() => startRandomScenario(), 300);
      } else {
        ui.appendBot('Nuova sessione test bot — scrivi una domanda cliente.', { labSystem: true });
      }
      refreshSidebar();
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

    await rag.init();
    await AbraLLM.bootstrapLocalConfig();
    const idx = await fetch('data/knowledge-index.json').then(r => r.json());
    document.getElementById('sb-kb').textContent = idx.chunk_count + ' chunk';
    ui.setStatus('Online', true);
    refreshSidebar();

    if (trainingMode === 'expert-quiz') {
      ui.appendBot('**Quiz esperto** — domanda cliente casuale…', { labSystem: true });
      setTimeout(() => startRandomScenario(), 350);
    } else {
      ui.appendBot(
        '**Test bot** — scrivi come un cliente, correggi l’AI.\n\n' +
        '**Quiz esperto** — tocca il pulsante: appare una **domanda cliente a caso** e **rispondi tu**.',
        { labSystem: true }
      );
    }
  }

  if (window.AbraAdmin?.whenUnlocked) window.AbraAdmin.whenUnlocked(init);
  else init();
})();
