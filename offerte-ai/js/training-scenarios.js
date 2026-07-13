/**
 * Generatore scenari cliente realistici per Lab Training (quiz esperto).
 */
(function (global) {
  'use strict';

  const INDUSTRIES = [
    { id: 'tessile', label: 'Tessile / abbigliamento', tags: ['ispezione', 'pick-place leggero', 'telepresenza'] },
    { id: 'alimentare', label: 'Alimentare / beverage', tags: ['igienico', 'pick-place', 'pallet leggeri', 'IP'] },
    { id: 'automotive', label: 'Automotive tier-2', tags: ['pick-place', 'ispezione', 'logistica interna'] },
    { id: 'logistica', label: 'Logistica / e-commerce', tags: ['sorting', 'pick-place', 'AMR'] },
    { id: 'farmaceutico', label: 'Farmaceutico / medical device', tags: ['certificazione', 'tracabilità', 'cella chiusa'] },
    { id: 'metalmeccanico', label: 'Metalmeccanico', tags: ['ispezione', 'perlustrazione', 'ambiente oleoso'] },
    { id: 'elettronica', label: 'Elettronica / EMS', tags: ['pick-place SMD tray', 'ESD', 'vision'] },
    { id: 'packaging', label: 'Packaging / converting', tags: ['scatole', 'pick-place', 'linea continua'] },
  ];

  const USE_CASES = [
    {
      id: 'pick-place-ab',
      templates: [
        'Dobbiamo spostare {object} dal punto A al punto B in reparto {area}. Ciclo target {cycle}. Valutiamo {platforms}. Priorità: {priority}.',
        'PoC pick-place: {object} da nastro A a banco B. Spazio {area}. Budget integrazione circa {budget}. Tempi {timeline}. {platforms}?',
      ],
      objects: ['scatole fino a 2 kg', 'tray con componenti', 'campioni tessuto', 'confezioni singole', 'bin picking leggero'],
      areas: ['cella dedicata 4×5 m', 'linea packaging con operatori vicini', 'magazzino picking', 'area QC separata'],
      cycles: ['12 pezzi/min', '6 cicli/min', '20 secondi/ciclo', 'batch da 50 pezzi/ora'],
      platforms: [
        'R1-D su piantana fissa vs mobile',
        'G1-D montato vs G1-U2 bipede',
        'G1-U2 vs H2 per flessibilità',
        'R1-D dual-arm vs cobot su rail',
      ],
      priorities: ['certificazione CE/safety', 'time-to-demo', 'costo contenuto', 'scalabilità multi-postazione'],
    },
    {
      id: 'surveillance',
      templates: [
        'Sorveglianza {area} con {sensors}. Alternativa quadrupede vs umanoide per telepresenza. Budget {budget}, consegna {timeline}.',
      ],
      areas: ['capannone 8000 m²', 'deposito esterno', 'zona ATEX limitata', 'perimetro notturno'],
      sensors: ['termocamera', 'gas + umidità', 'LiDAR aggiuntivo', 'solo camera RGB'],
    },
    {
      id: 'university',
      templates: [
        'Università {dept}: robot per {goal}. Serve ROS2, budget {budget}, consegna entro {timeline}. Confronto {platforms}.',
      ],
      dept: ['ingegneria meccatronica', 'robotica', 'AI lab', 'PhD sim-to-real'],
      goal: ['ricerca locomozione', 'manipolazione bimanuale', 'dataset raccolta', 'competizione'],
      platforms: ['R1 EDU vs G1-U1', 'Go2 EDU vs As2 Pro', 'G1-U2 vs G1-U4'],
    },
    {
      id: 'integration',
      templates: [
        'Integrazione con {system} per {goal}. Robot già scelto: {robot}. PoC {pocLevel}. Timeline {timeline}.',
      ],
      system: ['MES SAP', 'SCADA Ignition', 'OPC UA', 'solo ROS2'],
      goal: ['telemetria produzione', 'mission planning', 'dashboard operatore'],
      robot: ['G1-U2', 'As2 Pro', 'MiR250 + cobot', 'da definire'],
      pocLevel: ['base lab', 'standard con test campo', 'avanzato multi-robot'],
    },
  ];

  const BUDGETS = ['€ 50–80k totale', '€ 120k hardware+integrazione', 'solo robot sotto € 40k', 'da definire post-PoC'];
  const TIMELINES = ['entro 3 mesi', 'Q3 2026', '6–8 settimane demo', 'fine anno per bando PNRR'];

  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function fill(template, ctx) {
    return template.replace(/\{(\w+)\}/g, (_, k) => ctx[k] || pick(USE_CASES.flatMap(u => u[k] || [])) || '—');
  }

  function generate(opts = {}) {
    const industry = opts.industry
      ? INDUSTRIES.find(i => i.id === opts.industry) || pick(INDUSTRIES)
      : pick(INDUSTRIES);
    const useCase = opts.useCase
      ? USE_CASES.find(u => u.id === opts.useCase) || pick(USE_CASES)
      : pick(USE_CASES);

    const ctx = {
      object: pick(useCase.objects || ['componenti']),
      area: pick(useCase.areas || ['reparto produzione']),
      cycle: pick(useCase.cycles || ['10 cicli/min']),
      platforms: pick(useCase.platforms || ['G1 vs R1-D']),
      priority: pick(useCase.priorities || ['certificazione']),
      sensors: pick(useCase.sensors || ['termocamera']),
      dept: pick(useCase.dept || ['robotica']),
      goal: pick(useCase.goal || ['PoC']),
      system: pick(useCase.system || ['ROS2']),
      robot: pick(useCase.robot || ['G1-U2']),
      pocLevel: pick(useCase.pocLevel || ['standard']),
      budget: pick(BUDGETS),
      timeline: pick(TIMELINES),
    };

    const template = pick(useCase.templates);
    const question = fill(template, ctx);

    const hints = [
      `Settore: **${industry.label}**`,
      `Use case: ${useCase.id.replace(/-/g, ' ')}`,
      `Budget indicativo: ${ctx.budget}`,
      `Timeline: ${ctx.timeline}`,
    ].join(' · ');

    return {
      id: 'sc-' + Date.now().toString(36),
      industry: industry.label,
      industryId: industry.id,
      useCaseId: useCase.id,
      question: `${question}\n\n_${hints}_`,
      hints,
      meta: {
        industry: industry.id,
        useCase: useCase.id,
        budget: ctx.budget,
        timeline: ctx.timeline,
        generated_at: new Date().toISOString(),
      },
    };
  }

  /** Domande curate ad alta priorità — da usare nel quiz sequenziale. */
  const SEED_QUESTIONS = [
    {
      id: 'seed-pick-place',
      industry: 'Packaging / manifattura',
      question:
        'Abbiamo una linea packaging: scatole da 1,5 kg dal nastro (A) al pallet (B), cella 5×4 m con operatori a 2 m. ' +
        'Valutiamo R1-D e G1-D su piantana fissa o mobile, oppure G1-U2/H2 bipedi. Priorità certificazione. ' +
        'Quale piattaforma per un PoC e quali step/costi?',
    },
    {
      id: 'seed-tessile-poc',
      industry: 'Tessile',
      question:
        'Azienda tessile 120 dipendenti: vogliono PoC umanoide per ispezione campioni e pick-place leggero in QC. ' +
        'Budget € 90k, demo entro 4 mesi. G1-U1 vs G1-U2 vs quadrupede?',
    },
    {
      id: 'seed-alimentare',
      industry: 'Alimentare',
      question:
        'Cooperativa alimentare: robot per campionamento e ispezione visiva area lavaggio (umido, IP importante). ' +
        'Quadrupede o umanoide? Finanziamenti 4.0?',
    },
    {
      id: 'seed-assistenza',
      industry: 'Post-vendita',
      question:
        'Cliente con G1-U2 in garanzia: braccio bloccato dopo caduta da 40 cm. Quanto costa riparazione, tempi e step assistenza Abra?',
    },
    {
      id: 'seed-offerta-formale',
      industry: 'Preventivo',
      question:
        'Mi serve preventivo formale: PoC pick-place manifattura con R1-D su piantana + integrazione standard + formazione 1 giornata.',
    },
  ];

  function nextSeed() {
    const key = 'abra_training_seed_idx';
    let idx = parseInt(localStorage.getItem(key) || '0', 10);
    const item = SEED_QUESTIONS[idx % SEED_QUESTIONS.length];
    localStorage.setItem(key, String(idx + 1));
    return {
      id: item.id,
      industry: item.industry,
      question: item.question,
      hints: 'Domanda curata Abra — priorità alta per knowledge',
      meta: { seed: true, seedId: item.id },
    };
  }

  global.AbraTrainingScenarios = { generate, nextSeed, SEED_QUESTIONS, INDUSTRIES };
})(typeof window !== 'undefined' ? window : globalThis);
