/**
 * Lab Training — Quiz esperto = domanda cliente casuale → tu rispondi → knowledge.
 * Generatore scenari integrato (no dipendenze esterne).
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

  /* ── Generatore scenari (inline, sempre disponibile) ── */
  const INDUSTRIES = [
    { id: 'tessile', label: 'Tessile / abbigliamento' },
    { id: 'alimentare', label: 'Alimentare / beverage' },
    { id: 'automotive', label: 'Automotive tier-2' },
    { id: 'logistica', label: 'Logistica / e-commerce' },
    { id: 'farmaceutico', label: 'Farmaceutico / medical device' },
    { id: 'metalmeccanico', label: 'Metalmeccanico' },
    { id: 'elettronica', label: 'Elettronica / EMS' },
    { id: 'packaging', label: 'Packaging / converting' },
  ];

  const USE_CASES = [
    {
      id: 'pick-place',
      templates: [
        'Dobbiamo spostare {object} dal punto A al punto B in {area}. Ciclo {cycle}. Valutiamo {platforms}. Priorità: {priority}. Budget {budget}, tempi {timeline}.',
        'PoC pick-place: {object}, reparto {area}. {platforms}? Budget {budget}.',
      ],
      object: ['scatole fino a 2 kg', 'tray componenti', 'campioni tessuto', 'confezioni singole'],
      area: ['cella 4×5 m', 'linea packaging con operatori', 'magazzino picking', 'area QC'],
      cycle: ['12 pezzi/min', '6 cicli/min', '20 s/ciclo'],
      platforms: ['R1-D su piantana fissa vs mobile', 'G1-D vs G1-U2 bipede', 'G1-U2 vs H2'],
      priority: ['certificazione CE', 'time-to-demo', 'costo contenuto'],
    },
    {
      id: 'surveillance',
      templates: ['Sorveglianza {area} con {sensor}. Quadrupede vs umanoide? Budget {budget}, {timeline}.'],
      area: ['capannone 8000 m²', 'deposito esterno', 'perimetro notturno'],
      sensor: ['termocamera', 'gas + umidità', 'LiDAR aggiuntivo'],
    },
    {
      id: 'university',
      templates: ['Università {dept}: {goal}. ROS2, budget {budget}, entro {timeline}. {platforms}?'],
      dept: ['meccatronica', 'robotica', 'AI lab'],
      goal: ['ricerca locomozione', 'manipolazione bimanuale', 'sim-to-real'],
      platforms: ['R1 EDU vs G1-U1', 'Go2 EDU vs As2 Pro', 'G1-U2 vs G1-U4'],
    },
    {
      id: 'integration',
      templates: ['Integrazione {system} per {goal}. Robot: {robot}. PoC {poc}. {timeline}.'],
      system: ['MES SAP', 'SCADA', 'OPC UA', 'ROS2'],
      goal: ['telemetria', 'mission planning', 'dashboard operatore'],
      robot: ['G1-U2', 'As2 Pro', 'MiR250', 'da definire'],
      poc: ['base lab', 'standard test campo', 'avanzato multi-robot'],
    },
  ];

  const BUDGETS = ['€ 50–80k totale', '€ 120k hw+integrazione', 'sotto € 40k robot', 'da definire'];
  const TIMELINES = ['entro 3 mesi', 'Q3 2026', '6–8 settimane demo', 'fine anno bando PNRR'];

  const SEED_QUESTIONS = [
    {
      id: 'seed-pick-place',
      industry: 'Packaging / manifattura',
      question:
        'Linea packaging: scatole 1,5 kg dal nastro (A) al pallet (B), cella 5×4 m, operatori a 2 m. ' +
        'R1-D e G1-D su piantana fissa/mobile, oppure G1-U2/H2 bipedi. Priorità certificazione. ' +
        'Quale piattaforma per PoC, step e costi?',
    },
    {
      id: 'seed-tessile',
      industry: 'Tessile',
      question:
        'Azienda tessile 120 dipendenti: PoC umanoide ispezione campioni + pick-place leggero QC. ' +
        'Budget € 90k, demo 4 mesi. G1-U1 vs G1-U2 vs quadrupede?',
    },
    {
      id: 'seed-alimentare',
      industry: 'Alimentare',
      question:
        'Cooperativa alimentare: campionamento e ispezione visiva area lavaggio (umido, IP). Quadrupede o umanoide? Finanziamenti 4.0?',
    },
    {
      id: 'seed-assistenza',
      industry: 'Post-vendita',
      question:
        'G1-U2 in garanzia, braccio bloccato dopo caduta 40 cm. Costi riparazione, tempi e step assistenza Abra?',
    },
    {
      id: 'seed-offerta',
      industry: 'Preventivo',
      question:
        'Preventivo formale: PoC pick-place con R1-D su piantana + integrazione standard + formazione 1 giornata.',
    },
  ];

  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function fillTemplate(tpl, ctx) {
    return tpl.replace(/\{(\w+)\}/g, (_, k) => (ctx[k] != null ? ctx[k] : '—'));
  }

  function randomScenario() {
    const industry = pick(INDUSTRIES);
    const useCase = pick(USE_CASES);
    const ctx = {
      object: pick(useCase.object || ['componenti']),
      area: pick(useCase.area || ['reparto produzione']),
      cycle: pick(useCase.cycle || ['10 cicli/min']),
      platforms: pick(useCase.platforms || ['G1 vs R1-D']),
      priority: pick(useCase.priority || ['certificazione']),
      sensor: pick(useCase.sensor || ['termocamera']),
      dept: pick(useCase.dept || ['robotica']),
      goal: pick(useCase.goal || ['PoC']),
      system: pick(useCase.system || ['ROS2']),
      robot: pick(useCase.robot || ['G1-U2']),
      poc: pick(useCase.poc || ['standard']),
      budget: pick(BUDGETS),
      timeline: pick(TIMELINES),
    };
    const question = fillTemplate(pick(useCase.templates), ctx);
    return {
      id: 'sc-' + Date.now().toString(36),
      industry: industry.label,
      question: question + '\n\n_Settore: ' + industry.label + ' · Budget: ' + ctx.budget + ' · ' + ctx.timeline + '_',
      meta: { industry: industry.id, useCase: useCase.id, random: true },
    };
  }

  function seedScenario() {
    const key = 'abra_training_seed_idx';
    const idx = parseInt(localStorage.getItem(key) || '0', 10);
    const item = SEED_QUESTIONS[idx % SEED_QUESTIONS.length];
    localStorage.setItem(key, String(idx + 1));
    return { id: item.id, industry: item.industry, question: item.question, meta: { seed: true } };
  }

  /* ── Stato Lab ── */
  let rag, ui;
  let trainingMode = localStorage.getItem(TRAINING_MODE_KEY) || 'bot-test';
  let pendingScenario = null;

  function updateComposeUi() {
    if (!ui?.setComposePlaceholder) return;
    if (trainingMode === 'expert-quiz' && pendingScenario) {
      ui.setComposePlaceholder('✏️ Scrivi la TUA risposta da consulente Abra…');
      ui.setComposeHint('Invio = salva in knowledge · Poi parte la prossima domanda');
    } else if (trainingMode === 'expert-quiz') {
      ui.setComposePlaceholder('Premi «Quiz» o «Prossima» per la domanda cliente…');
      ui.setComposeHint('Quiz esperto — il bot vendite è spento');
    } else {
      ui.setComposePlaceholder('Scrivi come un cliente…');
      ui.setComposeHint('Test bot — l’AI risponde, tu correggi');
    }
  }

  function refreshSidebar() {
    try {
      const cfg = AbraLLM?.loadConfig?.() || {};
      const modeEl = document.getElementById('sb-mode');
      if (modeEl) modeEl.textContent = MODE_LABELS[cfg.mode] || cfg.mode || '—';

      const fb = AbraFeedbackStore.all();
      const fbEl = document.getElementById('sb-fb');
      const kbEl = document.getElementById('sb-kb-pending');
      if (fbEl) fbEl.textContent = fb.length;
      if (kbEl) kbEl.textContent = AbraFeedbackStore.pendingKb().length;

      document.querySelectorAll('[data-training-mode]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.trainingMode === trainingMode);
      });

      const modeHint = document.getElementById('sb-training-mode-hint');
      if (modeHint) {
        modeHint.textContent = trainingMode === 'expert-quiz'
          ? (pendingScenario ? '✦ Rispondi al cliente simulato qui sotto' : 'Tocca Quiz ↻ per una domanda casuale')
          : 'Scrivi come un cliente — correggi la risposta AI';
      }

      const nextBtn = document.getElementById('sb-quiz-next');
      if (nextBtn) nextBtn.hidden = trainingMode !== 'expert-quiz';

      updateComposeUi();
    } catch (e) {
      console.error('refreshSidebar', e);
    }
  }

  function showClientQuestion(scenario) {
    if (!ui) {
      console.error('Lab: UI non pronta');
      return false;
    }
    pendingScenario = scenario;
    trainingMode = 'expert-quiz';
    localStorage.setItem(TRAINING_MODE_KEY, 'expert-quiz');

    ui.appendBot(
      '**🎭 DOMANDA CLIENTE**\n' +
      '**Settore:** ' + scenario.industry + '\n\n' +
      scenario.question + '\n\n' +
      '---\n' +
      '👇 **Scrivi qui sotto la risposta** che darebbe un consulente Abra (prezzi, step, raccomandazione).',
      { isScenario: true, labSystem: true }
    );

    refreshSidebar();
    ui.inputEl?.focus();
    if (ui.messagesEl) {
      ui.messagesEl.scrollTop = ui.messagesEl.scrollHeight;
    }
    return true;
  }

  function launchQuiz(kind) {
    trainingMode = 'expert-quiz';
    localStorage.setItem(TRAINING_MODE_KEY, 'expert-quiz');
    pendingScenario = null;

    try {
      const scenario = kind === 'seed' ? seedScenario() : randomScenario();
      if (!scenario?.question) throw new Error('Scenario vuoto');
      showClientQuestion(scenario);
      return true;
    } catch (err) {
      console.error('launchQuiz', err);
      ui?.appendBot(
        '⚠️ **Errore generazione domanda:** ' + err.message + '\n\nRicarica la pagina (Ctrl+F5).',
        { labSystem: true }
      );
      return false;
    }
  }

  function enterBotTestMode() {
    trainingMode = 'bot-test';
    localStorage.setItem(TRAINING_MODE_KEY, 'bot-test');
    pendingScenario = null;
    refreshSidebar();
    ui?.appendBot('**Test bot** attivo — scrivi una domanda come cliente.', { labSystem: true });
  }

  function saveExpertAnswer(text) {
    const scenario = pendingScenario;
    if (!scenario) return null;

    pendingScenario = null;
    const entry = {
      id: 'fb-' + Date.now().toString(36),
      timestamp: new Date().toISOString(),
      question: String(scenario.question).replace(/\n\n_.*_$/, '').slice(0, 2000),
      answer: '(quiz esperto — risposta consulente)',
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

    setTimeout(() => launchQuiz('random'), 1200);

    return {
      reply:
        '✅ **Risposta salvata in knowledge** (in coda: **' + AbraFeedbackStore.pendingKb().length + '**)\n\n' +
        'Tra un attimo appare la **prossima domanda casuale**…',
      skipFeedback: true,
      labSystem: true,
    };
  }

  async function handleSend(q) {
    if (trainingMode === 'expert-quiz') {
      if (pendingScenario) return saveExpertAnswer(q);
      launchQuiz('random');
      return { silent: true };
    }
    if (!rag) return { reply: 'Caricamento listini… riprova tra 2 secondi.', skipFeedback: true, labSystem: true };
    return rag.ask(q);
  }

  function bindControls() {
    document.querySelectorAll('[data-training-mode="bot-test"]').forEach(btn => {
      btn.addEventListener('click', e => { e.preventDefault(); enterBotTestMode(); });
    });
    document.querySelectorAll('[data-training-mode="expert-quiz"], #sb-quiz-next').forEach(btn => {
      btn.addEventListener('click', e => { e.preventDefault(); launchQuiz('random'); });
    });
    document.querySelectorAll('#sb-scenario-seed, #lab-btn-seed').forEach(btn => {
      btn.addEventListener('click', e => { e.preventDefault(); launchQuiz('seed'); });
    });

    document.getElementById('sb-export-all')?.addEventListener('click', () => {
      const pack = AbraFeedbackStore.exportTrainingPack();
      if (!pack.feedback) return AbraUI?.toast?.('Nessun feedback', 'warn');
      AbraFeedbackStore.download('feedback-export.jsonl', pack.feedback, 'application/x-ndjson');
      if (pack.kbMd) AbraFeedbackStore.download('feedback-knowledge.md', pack.kbMd, 'text/markdown');
      AbraUI?.toast?.('Scaricato', 'ok');
    });

    document.getElementById('sb-copy-feedback')?.addEventListener('click', async () => {
      const jsonl = AbraFeedbackStore.exportJsonl();
      if (!jsonl) return AbraUI?.toast?.('Nessun feedback', 'warn');
      try {
        await navigator.clipboard.writeText(jsonl);
        AbraUI?.toast?.('Copiato negli appunti', 'ok');
      } catch {
        AbraFeedbackStore.download('feedback-export.jsonl', jsonl, 'application/x-ndjson');
      }
    });

    document.getElementById('sb-clear-chat')?.addEventListener('click', () => {
      rag?.clearHistory?.();
      pendingScenario = null;
      ui.messagesEl.innerHTML = '';
      if (trainingMode === 'expert-quiz') launchQuiz('random');
      else ui.appendBot('Chat resettata — scrivi una domanda cliente.', { labSystem: true });
      refreshSidebar();
    });
  }

  async function init() {
    AbraUI.mountNav('chat');

    ui = new AbraChatUI('#chat-root', {
      title: 'Abra Lab',
      subtitle: trainingMode === 'expert-quiz' ? 'Quiz esperto · rispondi tu' : 'Test bot · correggi AI',
      avatarLetter: '✦',
      variant: 'thread',
      theme: 'platinum',
      feedbackMode: 'lab',
      suggestions: SUGGESTIONS,
      onSend: handleSend,
      onFeedback: refreshSidebar,
    });

    bindControls();
    refreshSidebar();

    /* Quiz subito — non aspettare RAG/OpenAI */
    if (trainingMode === 'expert-quiz') {
      launchQuiz('random');
    } else {
      ui.appendBot(
        '**Test bot** — scrivi come un cliente.\n\n' +
        '**Quiz esperto** — tocca **Quiz ↻**: domanda cliente casuale, **rispondi tu** → knowledge.',
        { labSystem: true }
      );
    }

    /* RAG in background per Test bot */
    rag = new AbraRAGChat({
      indexUrl: 'data/knowledge-index.json',
      pricesUrl: '../listini/pubblico/end-user.json',
      rulesUrl: 'data/offerte-regole.json',
    });
    try {
      await rag.init();
      await AbraLLM.bootstrapLocalConfig();
      const idx = await fetch('data/knowledge-index.json').then(r => r.json());
      const kbEl = document.getElementById('sb-kb');
      if (kbEl) kbEl.textContent = idx.chunk_count + ' chunk';
      ui.setStatus('Online', true);
      refreshSidebar();
    } catch (err) {
      ui.setStatus('Parziale', false);
      if (trainingMode === 'bot-test') {
        ui.appendBot('Listini non caricati: ' + err.message, { labSystem: true });
      }
    }
  }

  if (window.AbraAdmin?.whenUnlocked) window.AbraAdmin.whenUnlocked(init);
  else init();
})();
