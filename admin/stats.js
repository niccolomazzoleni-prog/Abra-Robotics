/* Dashboard admin — accessi abrarobotics.com + deploy GitHub Pages. */
(function () {
  'use strict';

  const STATS_JSON = '../data/site-stats.json';
  const STATS_KEY_STORAGE = 'abra_stats_key';
  const PERIOD_KEY = 'abra_stats_days';

  const fmt = new Intl.NumberFormat('it-IT');
  const fmtDate = new Intl.DateTimeFormat('it-IT', { dateStyle: 'short', timeStyle: 'short' });
  const fmtDay = new Intl.DateTimeFormat('it-IT', { day: '2-digit', month: 'short' });

  function el(id) { return document.getElementById(id); }

  function getPeriod() {
    return Number(sessionStorage.getItem(PERIOD_KEY) || 30);
  }

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

  async function loadBeaconStats(config, days) {
    const key = getStatsKey(config);
    const base = window.GOOGLE_SCRIPT_URL;
    if (!key || !base) return null;
    const url = `${base}?action=stats&key=${encodeURIComponent(key)}&days=${days}`;
    const r = await fetch(url);
    if (!r.ok) return null;
    const data = await r.json();
    return data.ok ? data : null;
  }

  function renderKpis(beacon, staticData) {
    const site = beacon || null;
    const gh = (staticData && staticData.github) || {};
    const items = [
      {
        value: site ? fmt.format(site.totals.pageviews) : '—',
        label: 'Visite pagine',
        sub: site ? `Ultimi ${site.days} giorni · abrarobotics.com` : 'Beacon — ridistribuisci Apps Script'
      },
      {
        value: site ? fmt.format(site.totals.sessions) : '—',
        label: 'Sessioni',
        sub: site ? `Mobile ~${site.mobile_pct || 0}%` : 'Stima giorno + referrer'
      },
      {
        value: site ? fmt.format(site.totals.leads) : '—',
        label: 'Contatti form',
        sub: site ? `Ultimi ${site.days} giorni` : 'Foglio Google Contatti'
      },
      {
        value: gh.pages_status === 'built' ? 'Online' : (gh.pages_status || '—'),
        label: 'GitHub Pages',
        sub: gh.pages_url ? 'Deploy sito statico' : 'abrarobotics.com'
      }
    ];

    el('kpi-grid').innerHTML = items.map((k) => `
      <div class="kpi">
        <div class="kpi-value">${k.value}</div>
        <div class="kpi-label">${k.label}</div>
        <div class="kpi-sub">${k.sub}</div>
      </div>`).join('');
  }

  function renderBarList(containerId, rows, labelKey, countKey, emptyMsg) {
    const root = el(containerId);
    if (!root) return;
    if (!rows || !rows.length) {
      root.innerHTML = `<p class="stats-empty">${emptyMsg}</p>`;
      return;
    }
    const max = Math.max(...rows.map((r) => r[countKey] || 0), 1);
    root.innerHTML = `<ul class="bar-list">${rows.slice(0, 12).map((r) => {
      const label = r[labelKey] || '(direct)';
      const count = r[countKey] || 0;
      const pct = Math.round((count / max) * 100);
      return `<li>
          <span class="label" title="${label}">${label}</span>
          <span class="count">${fmt.format(count)}</span>
          <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
        </li>`;
    }).join('')}</ul>`;
  }

  function renderDailyChart(beacon) {
    const root = el('site-daily');
    if (!root) return;
    const rows = (beacon && beacon.daily) || [];
    if (!rows.length) {
      root.innerHTML = '<p class="stats-empty">Il grafico giornaliero comparirà dopo il redeploy di apps-script/Code.gs (campo daily).</p>';
      return;
    }
    const max = Math.max(...rows.map((r) => r.count), 1);
    root.innerHTML = `<div class="stats-chart">${rows.map((r) => {
      const h = Math.max(4, Math.round((r.count / max) * 100));
      const label = fmtDay.format(new Date(r.date + 'T12:00:00'));
      return `<div class="stats-chart-col" title="${r.date}: ${r.count} visite">
        <div class="stats-chart-bar" style="height:${h}%"></div>
        <span class="stats-chart-lbl">${label}</span>
      </div>`;
    }).join('')}</div>`;
  }

  function renderSiteSources(beacon) {
    if (beacon && beacon.referrers && beacon.referrers.length) {
      renderBarList('site-referrers', beacon.referrers, 'referrer', 'count', 'Nessun referrer.');
    } else {
      el('site-referrers').innerHTML = `<p class="stats-empty">Nessun dato referrer. Naviga sul sito pubblico per popolare la scheda Analytics del foglio Google.</p>`;
    }
    if (beacon && beacon.pages && beacon.pages.length) {
      renderBarList('site-pages', beacon.pages, 'path', 'count', 'Nessuna pagina.');
    } else {
      el('site-pages').innerHTML = '<p class="stats-empty">Le pagine più visitate compariranno qui.</p>';
    }
    if (beacon && beacon.sources && beacon.sources.length) {
      renderBarList('site-utm', beacon.sources, 'source', 'count', 'Nessuna UTM.');
    } else if (el('site-utm')) {
      el('site-utm').innerHTML = '<p class="stats-empty">Campagne UTM quando presenti negli URL.</p>';
    }
    renderDailyChart(beacon);
  }

  function renderGithubPanel(staticData) {
    const root = el('github-panel');
    if (!root) return;
    const gh = staticData.github || {};
    const wf = staticData.workflows || [];
    const views = (gh.traffic && gh.traffic.views) || [];
    const v7 = views.slice(-7).reduce((a, x) => a + (x.count || 0), 0);
    root.innerHTML = `
      <div class="stats-gh-grid">
        <div><strong>Pages</strong><br>${gh.pages_url ? `<a href="${gh.pages_url}" target="_blank" rel="noopener">${gh.pages_status || 'link'}</a>` : '—'}</div>
        <div><strong>View repo GitHub (7 gg)</strong><br>${fmt.format(v7)} <span class="hint">non = visite sito</span></div>
        <div><strong>Stelle</strong><br>${fmt.format(gh.stars || 0)}</div>
      </div>
      <h3 style="margin:16px 0 8px;font-size:0.92rem">Ultimi workflow (deploy / listini / KB)</h3>
      ${wf.length ? `<ul class="bar-list">${wf.slice(0, 6).map((run) => {
        const cls = run.conclusion === 'success' ? 'ok' : run.status === 'in_progress' ? 'run' : 'fail';
        return `<li>
          <span class="label">${run.name || 'Workflow'}</span>
          <span class="status-pill ${cls}">${run.conclusion || run.status}</span>
          <div class="bar-track" style="opacity:0"></div>
        </li>`;
      }).join('')}</ul>` : '<p class="stats-empty">Dati workflow dal job GitHub Actions giornaliero.</p>'}`;
  }

  function renderSetupNote(config, beacon) {
    const note = el('setup-note');
    if (!note) return;
    const key = getStatsKey(config);
    if (beacon && beacon.totals) {
      note.innerHTML = `Live · chiave <code>${key}</code> · GA <code>${config.site?.ga_property || '—'}</code> · aggiornato ${fmtDate.format(new Date())}`;
      note.className = 'hint stats-ok';
      return;
    }
    note.innerHTML = `Per attivare i numeri: ridistribuisci <code>apps-script/Code.gs</code> come Web App, poi visita il sito pubblico. Chiave: <code>${key}</code>`;
    note.className = 'hint stats-warn';
  }

  function bindPeriodButtons() {
    document.querySelectorAll('[data-stats-days]').forEach((btn) => {
      const days = Number(btn.dataset.statsDays);
      btn.classList.toggle('is-active', days === getPeriod());
      btn.addEventListener('click', () => {
        sessionStorage.setItem(PERIOD_KEY, String(days));
        location.reload();
      });
    });
  }

  function exportPagesCsv(beacon) {
    if (!beacon || !beacon.pages || !beacon.pages.length) {
      alert('Nessuna pagina da esportare.');
      return;
    }
    const lines = ['path,count', ...beacon.pages.map((p) => `"${p.path.replace(/"/g, '""')}",${p.count}`)];
    const blob = new Blob([lines.join('\n')], { type: 'text/csv' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'abra-pagine-piu-visitate.csv';
    a.click();
  }

  async function refreshAll(config, days) {
    const beacon = await loadBeaconStats(config, days);
    renderKpis(beacon, config);
    renderSiteSources(beacon);
    renderGithubPanel(config);
    renderSetupNote(config, beacon);
    el('stats-updated').textContent = 'Aggiornato: ' + fmtDate.format(new Date());
    return beacon;
  }

  async function boot() {
    let config = {};
    try {
      config = await loadSiteConfig();
      el('stats-updated').textContent = 'Config: ' + fmtDate.format(new Date(config.updated_at || Date.now()));
    } catch (e) {
      el('kpi-grid').innerHTML = `<p class="stats-empty">${e.message}</p>`;
    }

    const days = getPeriod();
    sessionStorage.setItem(STATS_KEY_STORAGE, getStatsKey(config));
    bindPeriodButtons();

    const keyInput = el('stats-key-input');
    if (keyInput) keyInput.value = getStatsKey(config);

    let beacon = null;
    try { beacon = await refreshAll(config, days); } catch (_) {}

    el('btn-save-stats-key')?.addEventListener('click', () => {
      const key = keyInput.value.trim();
      if (key) sessionStorage.setItem(STATS_KEY_STORAGE, key);
      else sessionStorage.removeItem(STATS_KEY_STORAGE);
      location.reload();
    });

    el('btn-refresh')?.addEventListener('click', async () => {
      const btn = el('btn-refresh');
      btn.disabled = true;
      btn.textContent = 'Aggiorno…';
      try { await refreshAll(config, days); } catch (ex) { alert(ex.message); }
      finally { btn.disabled = false; btn.textContent = 'Aggiorna dati sito'; }
    });

    el('btn-export-pages')?.addEventListener('click', () => exportPagesCsv(beacon));
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
