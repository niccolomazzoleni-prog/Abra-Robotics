/* Dashboard statistiche — accessi al sito abrarobotics.com (beacon first-party). */
(function () {
  'use strict';

  const STATS_JSON = '../data/site-stats.json';
  const STATS_KEY_STORAGE = 'abra_stats_key';

  const fmt = new Intl.NumberFormat('it-IT');
  const fmtDate = new Intl.DateTimeFormat('it-IT', { dateStyle: 'short', timeStyle: 'short' });

  function el(id) { return document.getElementById(id); }

  async function loadSiteConfig() {
    const r = await fetch(`${STATS_JSON}?t=${Date.now()}`);
    if (!r.ok) throw new Error('Impossibile caricare site-stats.json');
    return r.json();
  }

  function getStatsKey(config) {
    return sessionStorage.getItem(STATS_KEY_STORAGE)
      || (config.beacon && config.beacon.stats_key)
      || 'abra-stats-2026';
  }

  async function loadBeaconStats(config) {
    const key = getStatsKey(config);
    const base = window.GOOGLE_SCRIPT_URL;
    if (!key || !base) return null;
    const url = `${base}?action=stats&key=${encodeURIComponent(key)}&days=30`;
    const r = await fetch(url);
    if (!r.ok) return null;
    const data = await r.json();
    if (!data.ok) return null;
    return data;
  }

  function renderKpis(beacon) {
    const site = beacon && beacon.ok !== false ? beacon : null;
    const items = [
      {
        value: site ? fmt.format(site.totals.pageviews) : '—',
        label: 'Visite pagine',
        sub: site ? `Ultimi ${site.days} giorni sul sito` : 'Beacon non attivo o script da ridistribuire'
      },
      {
        value: site ? fmt.format(site.totals.sessions) : '—',
        label: 'Sessioni',
        sub: site ? 'Stima giorno + provenienza' : 'Vedi setup sotto'
      },
      {
        value: site ? fmt.format(site.totals.leads) : '—',
        label: 'Contatti',
        sub: site ? `Form inviati · ultimi ${site.days} gg` : 'Foglio Contatti Google'
      },
      {
        value: site && site.pages ? fmt.format(site.pages.length) : '—',
        label: 'Pagine in top',
        sub: 'Path più visitati registrati'
      }
    ];

    el('kpi-grid').innerHTML = items.map((k) => `
      <div class="kpi">
        <div class="kpi-value">${k.value}</div>
        <div class="kpi-label">${k.label}</div>
        <div class="kpi-sub">${k.sub}</div>
      </div>
    `).join('');
  }

  function renderBarList(containerId, rows, labelKey, countKey, emptyMsg) {
    const root = el(containerId);
    if (!rows || !rows.length) {
      root.innerHTML = `<p class="stats-empty">${emptyMsg}</p>`;
      return;
    }
    const max = Math.max(...rows.map((r) => r[countKey] || 0), 1);
    root.innerHTML = `<ul class="bar-list">${rows.slice(0, 12).map((r) => {
      const label = r[labelKey] || '(direct)';
      const count = r[countKey] || 0;
      const pct = Math.round((count / max) * 100);
      return `
        <li>
          <span class="label" title="${label}">${label}</span>
          <span class="count">${fmt.format(count)}</span>
          <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
        </li>`;
    }).join('')}</ul>`;
  }

  function renderSiteSources(beacon) {
    if (beacon && beacon.referrers && beacon.referrers.length) {
      renderBarList('site-referrers', beacon.referrers, 'referrer', 'count', 'Nessun referrer.');
    } else {
      el('site-referrers').innerHTML = `
        <p class="stats-empty">
          Nessun dato ancora. Ogni visita sul sito pubblico invia un beacon (tab <code>Analytics</code> nel foglio Contatti).
          Se vedi sempre zero: ridistribuisci <code>apps-script/Code.gs</code> come Web App e verifica che
          <code>script.js</code> abbia l'URL corretto.
        </p>`;
    }

    if (beacon && beacon.pages && beacon.pages.length) {
      renderBarList('site-pages', beacon.pages, 'path', 'count', 'Nessuna pagina registrata.');
    } else {
      el('site-pages').innerHTML = `<p class="stats-empty">Le pagine più visitate compariranno dopo le prime visite sul sito.</p>`;
    }

    if (beacon && beacon.sources && beacon.sources.length) {
      renderBarList('site-utm', beacon.sources, 'source', 'count', 'Nessuna campagna UTM.');
    } else {
      el('site-utm').innerHTML = `<p class="stats-empty">I parametri utm_source compariranno quando il traffico arriva da campagne taggate.</p>`;
    }
  }

  function renderUpdated(ts) {
    const node = el('stats-updated');
    if (node && ts) node.textContent = 'Config aggiornata: ' + fmtDate.format(new Date(ts));
  }

  function renderSetupNote(config, beacon) {
    const note = el('setup-note');
    if (!note) return;
    const key = getStatsKey(config);
    if (beacon && beacon.totals) {
      note.innerHTML = `Dati live dal foglio Google · chiave <code>${key}</code> · property GA <code>${config.site?.ga_property || '—'}</code>`;
      note.className = 'hint stats-ok';
      return;
    }
    note.innerHTML = `
      Per vedere i numeri: (1) ridistribuisci <code>apps-script/Code.gs</code> come Web App,
      (2) verifica <code>STATS_KEY</code> = <code>${key}</code>,
      (3) naviga sul sito pubblico per generare pageview.
      Intanto usa i link rapidi sotto per GA e Meta.`;
    note.className = 'hint stats-warn';
  }

  async function boot() {
    let config = {};
    try {
      config = await loadSiteConfig();
      renderUpdated(config.updated_at);
    } catch (e) {
      el('kpi-grid').innerHTML = `<p class="stats-empty">${e.message}</p>`;
    }

    const defaultKey = getStatsKey(config);
    sessionStorage.setItem(STATS_KEY_STORAGE, defaultKey);

    let beacon = null;
    try { beacon = await loadBeaconStats(config); } catch (_) {}

    renderKpis(beacon);
    renderSiteSources(beacon);
    renderSetupNote(config, beacon);

    const keyInput = el('stats-key-input');
    if (keyInput) keyInput.value = defaultKey;

    el('btn-save-stats-key')?.addEventListener('click', async () => {
      const key = keyInput.value.trim();
      if (key) sessionStorage.setItem(STATS_KEY_STORAGE, key);
      else sessionStorage.removeItem(STATS_KEY_STORAGE);
      location.reload();
    });

    el('btn-refresh')?.addEventListener('click', async () => {
      const btn = el('btn-refresh');
      btn.disabled = true;
      btn.textContent = 'Aggiorno…';
      try {
        const fresh = await loadBeaconStats(config);
        renderKpis(fresh);
        renderSiteSources(fresh);
        renderSetupNote(config, fresh);
        el('stats-updated').textContent = 'Dati sito aggiornati: ' + fmtDate.format(new Date());
      } catch (ex) {
        alert(ex.message || 'Errore aggiornamento');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Aggiorna dati sito';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
