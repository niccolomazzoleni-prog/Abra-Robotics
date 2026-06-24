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

  function updateComposeUi() {
    if (!ui) return;
    if (trainingMode === 'expert-quiz') {
      if (pendingScenario) {
        ui.setComposePlaceholder('Scrivi la risposta da consulente Abra per il cliente sopra…');
        ui.setComposeHint('Quiz attivo: la tua risposta va in knowledge (non chiedere al bot)');
      } else {
        ui.setComposePlaceholder('Premi Scenario o Curata per la domanda cliente…');
        ui.setComposeHint('Quiz esperto — genera prima uno scenario');
      }
    } else {
      ui.setComposePlaceholder('Scrivi come farebbe un cliente…');
      ui.setComposeHint('Test bot: chiedi → valuta la risposta AI sotto');
    }
  }

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
        ? (pendingScenario ? 'Quiz attivo — rispondi al cliente simulato' : 'Quiz: premi Scenario o Curata')
        : 'Test bot: chiedi e correggi la risposta AI';
    }
    updateComposeUi();
  }

  function setTrainingMode(mode, opts = {}) {
    trainingMode = mode;
    localStorage.setItem(TRAINING_MODE_KEY, mode);
    if (mode !== 'expert-quiz') pendingScenario = null;
    refreshSidebar();
    AbraUI.toast(mode === 'expert-quiz' ? 'Modalità Quiz esperto' : 'Modalità Test bot', 'info');
    if (mode === 'expert-quiz' && opts.startScenario !== false && !pendingScenario) {
      startSeedScenario();
    }
  }

  function showScenario(scenario) {
    pendingScenario = scenario;
    trainingMode = 'expert-quiz';
    localStorage.setItem(TRAINING_MODE_KEY, 'expert-quiz');
    ui.appendBot(
      `**🎭 DOMANDA CLIENTE** · ${scenario.industry}\n\n${scenario.question}\n\n` +
      '👇 **Tu rispondi sotto** come consulente Abra (prezzi listino, step, raccomandazioni). ' +
      'Non chiedere nulla al bot — scrivi la risposta al cliente.',
      { isScenario: true, labSystem: true }
    );
    refreshSidebar();
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
    if (!scenario) {
      return {
        reply: 'Errore interno quiz — rigenera lo scenario.',
        skipFeedback: true,
      };
    }
    pendingScenario = null;
    refreshSidebar();
    const fbId = 'fb-' + Date.now().toString(36);
    const entry = {
      id: fbId,
      timestamp: new Date().toISOString(),
      question: scenario.question.replace(/\n\n_.*_$/, ''),
      answer: '(risposta consulente — quiz esperto)',
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
        '✓ **Salvato in knowledge** (' + AbraFeedbackStore.pendingKb().length + ' in coda)\n\n' +
        'Prossimo passo: **Scenario** / **Curata** per un’altra domanda, oppure **Test bot** per verificare l’AI.\n\n' +
        '_Da mobile: sidebar → **Copia feedback** quando hai finito la sessione._',
      skipFeedback: true,
      labSystem: true,
    };
  }

  async function handleSend(q) {
    if (trainingMode === 'expert-quiz') {
      if (pendingScenario) {
        return handleExpertAnswer(q);
      }
      if (/^(scenario|curata|aiuto|help)$/i.test(q.trim())) {
        startSeedScenario();
        return { silent: true };
      }
      return {
        reply:
          '**Sei in Quiz esperto** — il bot commerciale è disattivato.\n\n' +
          '1. Tocca **Scenario** o **Curata** (barra in basso su mobile)\n' +
          '2. Leggi la **domanda cliente** che appare sopra\n' +
          '3. Scrivi **la tua risposta** da consulente\n\n' +
          '_«Preventivo ufficiale» è jargon interno del bot vendite — qui non serve. Tu sei il consulente._',
        skipFeedback: true,
        labSystem: true,
      };
    }
    return rag.ask(q);
  }

  function bindSidebar() {
    document.querySelectorAll('[data-training-mode]').forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.dataset.trainingMode;
        setTrainingMode(mode, { startScenario: mode === 'expert-quiz' });
      });
    });

    document.getElementById('sb-scenario-random')?.addEventListener('click', () => {
      setTrainingMode('expert-quiz', { startScenario: false });
      startRandomScenario();
    });
    document.getElementById('sb-scenario-seed')?.addEventListener('click', () => {
      setTrainingMode('expert-quiz', { startScenario: false });
      startSeedScenario();
    });
    document.getElementById('lab-btn-scenario')?.addEventListener('click', () => {
      setTrainingMode('expert-quiz', { startScenario: false });
      startRandomScenario();
    });
    document.getElementById('lab-btn-seed')?.addEventListener('click', () => {
      setTrainingMode('expert-quiz', { startScenario: false });
      startSeedScenario();
    });

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
        'Chat resettata.\n\n' +
        '• **Test bot** — scrivi una domanda cliente\n' +
        '• **Quiz esperto** — premi Scenario, poi rispondi tu',
        { labSystem: true }
      );
      if (trainingMode === 'expert-quiz') startSeedScenario();
      refreshSidebar();
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

      ui.appendBot(
        '**Come funziona**\n\n' +
        '**Test bot** — scrivi come un cliente; sotto la risposta: Va bene / Da correggere.\n\n' +
        '**Quiz esperto** — premi **Scenario** o **Curata**: appare una domanda cliente e **rispondi tu** (va in knowledge). Il bot vendite **non** risponde in quiz.\n\n' +
        (trainingMode === 'expert-quiz' ? '_Caricamento primo scenario…_' : '_Suggerimento: prova **Quiz** + **Curata**._'),
        { labSystem: true }
      );

      if (trainingMode === 'expert-quiz') {
        setTimeout(() => startSeedScenario(), 400);
      }
    } catch (err) {
      ui.appendBot('Errore avvio: ' + err.message, { labSystem: true });
      ui.setStatus('Offline', false);
    }
  }

  if (window.AbraAdmin?.whenUnlocked) window.AbraAdmin.whenUnlocked(init);
  else init();
})();
