/**
 * Lab Training v20260625fix2 — Quiz esperto = domanda cliente casuale → tu rispondi → knowledge.
 */
(function () {
  'use strict';

  window.ABRA_LAB_VERSION = '20260625gamma3';

  const SUGGESTIONS = [
    'G1 in ordine di costo',
    'PoC pick-place: R1-D vs G1-D vs G1-U2',
    'H2 Air vs H2 EDU per ricerca',
    'As2 Pro vs A2 Pro sorveglianza',
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
  const QUIZ_RECENT_KEY = 'abra_quiz_recent_ids';

  const BUDGETS = ['€ 50–80k totale', '€ 90–120k hw+integrazione', 'sotto € 40k solo robot', 'da definire post-brief'];
  const TIMELINES = ['3 mesi', '4–6 mesi PoC', '6–8 settimane demo hardware', 'Q3 2026', 'entro fine anno (bando)'];

  const SCENARIO_POOL = [
    {
      id: 'quad-sorveglianza',
      family: 'Quadrupede · sorveglianza / ispezione',
      industries: ['Logistica / capannone', 'Metalmeccanico', 'Farmaceutico', 'Oil & gas'],
      build(c) {
        return `${c.industry}: perlustrazione **${c.area}** con **${c.sensor}**. Confronto quadrupedi **${c.compare}**. Budget ${c.budget}, timeline ${c.timeline}.`;
      },
      vars: () => ({
        area: pick(['capannone 12.000 m²', 'deposito esterno', 'zona umida', 'perimetro notturno']),
        sensor: pick(['termocamera radiometrica', 'multi-gas + umidità', 'LiDAR aggiuntivo', 'camera + AI']),
        compare: pick(['As2 Pro vs A2 Pro', 'Go2 EDU Smart vs As2 Pro', 'As2 EDU vs A2 Standard']),
      }),
    },
    {
      id: 'uni-locomozione',
      family: 'Umanoide bipede · università / ROS2',
      industries: ['Università / ricerca'],
      build(c) {
        return `${c.industry}, ${c.dept}: ricerca **${c.goal}** con ROS2. Budget ${c.budget}, ${c.timeline}. Confronto **${c.compare}** (umanoide, non quadrupede).`;
      },
      vars: () => ({
        dept: pick(['meccatronica', 'robotica', 'AI lab']),
        goal: pick(['locomozione dinamica', 'sim-to-real', 'teleoperazione', 'acquisizione dataset']),
        compare: pick(['G1-U1 vs R1-U1', 'G1-U2 vs R1-U2', 'R1-U2 vs G1-U2']),
      }),
    },
    {
      id: 'uni-bimanuale',
      family: 'Dual-arm · manipolazione bimanuale',
      industries: ['Università / ricerca applied', 'Packaging / manifattura', 'Automotive tier-2'],
      build(c) {
        return `${c.industry}: PoC **${c.goal}**. Piattaforme **${c.compare}** — non Go2/As2. Priorità ${c.priority}. Budget ${c.budget}, PoC ${c.timeline}.`;
      },
      vars: () => ({
        goal: pick(['manipolazione bimanuale', 'pick-place scatole A→B', 'assemblaggio leggero due mani']),
        compare: pick(['R1-D vs G1-D su piantana fissa', 'R1-D mobile vs G1-D fisso', 'R1-D vs G1-U2 mono-arm']),
        priority: pick(['certificazione cella', 'time-to-demo', 'budget contenuto']),
      }),
    },
    {
      id: 'manif-pickplace',
      family: 'Industrial PoC · pick & place',
      industries: ['Packaging / converting', 'Elettronica / EMS', 'Tessile / QC', 'Alimentare'],
      build(c) {
        return `${c.industry}: **${c.object}** da A a B in **${c.area}**, ciclo ${c.cycle}. **${c.compare}**. Priorità ${c.priority}. Budget ${c.budget}, PoC ${c.timeline}.`;
      },
      vars: () => ({
        object: pick(['scatole fino a 2 kg', 'tray componenti', 'confezioni singole', 'campioni tessuto']),
        area: pick(['cella 5×4 m con operatori', 'linea packaging', 'area QC']),
        cycle: pick(['12 pezzi/min', '6 cicli/min', 'batch 50 pezzi/ora']),
        compare: pick(['R1-D piantana vs G1-D', 'R1-D vs G1-U2 bipede', 'G1-D mobile vs G1-U2']),
        priority: pick(['certificazione CE/safety', 'costo PoC', 'scalabilità']),
      }),
    },
    {
      id: 'h2-fullsize',
      family: 'H2 full-size · top gamma umanoide',
      industries: ['Università / ricerca', 'R&D corporate', 'Demo / innovation hub'],
      build(c) {
        return `${c.industry}: **${c.goal}**. Confronto **${c.compare}**. Budget ${c.budget}, ${c.timeline}. (H2 Plus: verificare con Abra.)`;
      },
      vars: () => ({
        goal: pick(['manipolazione alta coppia', 'locomozione full-size', 'showcase internazionale']),
        compare: pick(['H2 Air vs H2 EDU', 'H2 EDU vs G1-U7', 'H2 EDU vs R1-D']),
      }),
    },
    {
      id: 'g1-r1-lab',
      family: 'G1 / R1 · mono-manipolazione lab',
      industries: ['Università / ricerca', 'Tessile / QC', 'Startup deep-tech'],
      build(c) {
        return `${c.industry}: **${c.task}** (mono-arm). **${c.compare}**. PoC ${c.timeline}, budget ${c.budget}.`;
      },
      vars: () => ({
        task: pick(['ispezione qualità', 'pick-place leggero', 'telepresenza reparto']),
        compare: pick(['G1-U1 vs G1-U2', 'R1-U1 vs G1-U1', 'R1-U2 vs G1-U2']),
      }),
    },
    {
      id: 'integrazione-poc',
      family: 'PoC integrazione software',
      industries: ['Automotive tier-2', 'Logistica / capannone', 'Farmaceutico'],
      build(c) {
        return `${c.industry}: integrare **${c.robot}** con **${c.system}**. Fascia PoC ${c.poc}. ${c.timeline}. Quale robot per questo stack?`;
      },
      vars: () => ({
        robot: pick(['G1-U2', 'R1-D', 'As2 Pro', 'H2 EDU']),
        system: pick(['MES / SAP', 'SCADA Ignition', 'OPC UA', 'ROS2 + dashboard']),
        poc: pick(['base ~€ 10.560', 'standard ~€ 19.360', 'avanzata ~€ 30.800']),
      }),
    },
    {
      id: 'trap-quad-bimanual',
      family: '⚠️ Training — correggere richiesta errata',
      industries: ['Packaging / converting', 'Università / ricerca'],
      build(c) {
        return `${c.industry}: il cliente chiede **"${c.wrongAsk}"** (budget ${c.budget}). Come riformuli e cosa proponi?`;
      },
      vars: () => ({
        wrongAsk: pick([
          'Go2 EDU vs As2 Pro per manipolazione bimanuale',
          'As2 Pro per pick-place scatole in cella',
          'quadrupede per assemblaggio bimanuale',
        ]),
      }),
    },
  ];

  const SEED_QUESTIONS = [
    {
      id: 'seed-pick-place',
      industry: 'Packaging / manifattura',
      family: 'Dual-arm · pick & place',
      question:
        'Linea packaging: scatole 1,5 kg A→B, cella 5×4 m, operatori a 2 m. R1-D / G1-D piantana vs G1-U2/H2 bipedi. Certificazione. PoC 3–6 mesi, step e costi?',
    },
    {
      id: 'seed-bimanual-uni',
      industry: 'Università / ricerca',
      family: 'Dual-arm · università',
      question:
        'Lab robotica: manipolazione bimanuale. Budget € 80k, PoC 4–6 mesi. R1-D vs G1-D vs G1-U2 — non quadrupedi.',
    },
    {
      id: 'seed-quad-sorv',
      industry: 'Logistica / capannone',
      family: 'Quadrupede · sorveglianza',
      question: 'Capannone 10.000 m², umidità: sorveglianza termocamera + gas. As2 Pro vs A2 Pro vs Go2 EDU.',
    },
    {
      id: 'seed-h2',
      industry: 'Università / ricerca',
      family: 'H2 full-size',
      question: 'Robotica: piattaforma full-size. H2 Air vs H2 EDU vs G1-U7. Budget € 120k.',
    },
    {
      id: 'seed-assistenza',
      industry: 'Post-vendita',
      family: 'Assistenza',
      question: 'G1-U2 in garanzia, braccio bloccato post-caduta 40 cm. Costi, tempi, step assistenza Abra?',
    },
  ];

  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function pickScenarioFromPool() {
    const recent = JSON.parse(sessionStorage.getItem(QUIZ_RECENT_KEY) || '[]');
    let pool = SCENARIO_POOL.filter(s => !recent.includes(s.id));
    if (pool.length < 4) pool = SCENARIO_POOL.slice();
    const sc = pick(pool);
    sessionStorage.setItem(QUIZ_RECENT_KEY, JSON.stringify([sc.id, ...recent.filter(x => x !== sc.id)].slice(0, 14)));
    const industry = pick(sc.industries);
    const ctx = { industry, budget: pick(BUDGETS), timeline: pick(TIMELINES), ...(sc.vars ? sc.vars() : {}) };
    return {
      id: sc.id + '-' + Date.now().toString(36),
      industry,
      family: sc.family,
      question: sc.build(ctx),
      meta: { scenarioId: sc.id, family: sc.family },
    };
  }

  function randomScenario() {
    return pickScenarioFromPool();
  }

  function seedScenario() {
    const key = 'abra_training_seed_idx';
    const idx = parseInt(localStorage.getItem(key) || '0', 10);
    const item = SEED_QUESTIONS[idx % SEED_QUESTIONS.length];
    localStorage.setItem(key, String(idx + 1));
    return { id: item.id, industry: item.industry, family: item.family || 'Curata', question: item.question, meta: { seed: true } };
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
      const verEl = document.getElementById('sb-lab-ver');
      if (verEl) verEl.textContent = window.ABRA_LAB_VERSION || '?';
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
      if (nextBtn) nextBtn.disabled = trainingMode !== 'expert-quiz';

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
      '**Famiglia:** ' + (scenario.family || '—') + '\n' +
      '**Contesto:** ' + scenario.industry + '\n\n' +
      scenario.question + '\n\n' +
      '---\n👇 **Risposta consulente Abra** (prezzi listino, gamma corretta, step PoC).',
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
