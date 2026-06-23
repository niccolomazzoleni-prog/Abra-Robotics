/* Dashboard statistiche admin — GitHub, beacon sito, link GA/Meta. */
(function () {
  'use strict';

  const OWNER = 'niccolomazzoleni-prog';
  const REPO = 'Abra-Robotics';
  const STATS_JSON = '../data/site-stats.json';
  const STATS_KEY_STORAGE = 'abra_stats_key';

  const fmt = new Intl.NumberFormat('it-IT');
  const fmtDate = new Intl.DateTimeFormat('it-IT', { dateStyle: 'short', timeStyle: 'short' });

  function el(id) { return document.getElementById(id); }

  function sumDays(items, days) {
    if (!items || !items.length) return { count: 0, uniques: 0 };
    const slice = items.slice(-days);
    return slice.reduce(
      (acc, row) => ({
        count: acc.count + (row.count || 0),
        uniques: acc.uniques + (row.uniques || 0)
      }),
      { count: 0, uniques: 0 }
    );
  }

  function ghApi(path, token) {
    return fetch(`https://api.github.com/repos/${OWNER}/${REPO}${path}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
      }
    });
  }

  async function loadStaticStats() {
    const r = await fetch(`${STATS_JSON}?t=${Date.now()}`);
    if (!r.ok) throw new Error('Impossibile caricare site-stats.json');
    return r.json();
  }

  async function refreshLiveGithub(token) {
    const endpoints = [
      ['/traffic/views', 'views'],
      ['/traffic/clones', 'clones'],
      ['/traffic/popular/referrers', 'referrers'],
      ['/traffic/popular/paths', 'paths']
    ];
    const out = {};
    for (const [path, key] of endpoints) {
      const r = await ghApi(path, token);
      if (r.ok) out[key] = await r.json();
    }
    const repoR = await ghApi('', token);
    if (repoR.ok) out.repo = await repoR.json();
    const runsR = await fetch(
      `https://api.github.com/repos/${OWNER}/${REPO}/actions/runs?per_page=6`,
      { headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json' } }
    );
    if (runsR.ok) out.workflow_runs = (await runsR.json()).workflow_runs || [];
    return out;
  }

  async function loadBeaconStats() {
    const key = sessionStorage.getItem(STATS_KEY_STORAGE);
    const base = window.GOOGLE_SCRIPT_URL;
    if (!key || !base) return null;
    const url = `${base}?action=stats&key=${encodeURIComponent(key)}&days=30`;
    const r = await fetch(url);
    if (!r.ok) return null;
    return r.json();
  }

  function renderKpis(staticData, beacon) {
    const gh = staticData.github || {};
    const traffic = gh.traffic || {};
    const views7 = sumDays(traffic.views, 7);
    const clones14 = sumDays(traffic.clones, 14);
    const site = beacon && beacon.ok ? beacon : null;

    const items = [
      {
        value: site ? fmt.format(site.totals.pageviews) : '—',
        label: 'Visite sito',
        sub: site ? `Ultimi ${site.days} giorni · ${fmt.format(site.totals.sessions)} sessioni` : 'Attiva beacon Apps Script'
      },
      {
        value: site ? fmt.format(site.totals.leads) : '—',
        label: 'Contatti',
        sub: site ? `Ultimi ${site.days} giorni dal sito` : 'Vedi foglio Contatti'
      },
      {
        value: fmt.format(gh.stars || 0),
        label: 'Stelle GitHub',
        sub: 'Repository Abra-Robotics'
      },
      {
        value: fmt.format(clones14.count),
        label: 'Clone repo',
        sub: `${fmt.format(clones14.uniques)} unici · 14 gg`
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
    root.innerHTML = `<ul class="bar-list">${rows.slice(0, 8).map((r) => {
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

  function renderSiteSources(beacon, staticData) {
    if (beacon && beacon.ok && beacon.referrers && beacon.referrers.length) {
      renderBarList(
        'site-referrers',
        beacon.referrers.map((r) => ({ referrer: r.referrer, count: r.count })),
        'referrer',
        'count',
        'Nessun dato referrer.'
      );
    } else {
      el('site-referrers').innerHTML = `
        <p class="stats-empty">
          Attiva il tracking first-party: ridistribuisci <code>apps-script/Code.gs</code> e imposta la chiave sotto.
          Nel frattempo usa <a href="https://analytics.google.com/" target="_blank" rel="noopener">Google Analytics</a>.
        </p>`;
    }

    if (beacon && beacon.ok && beacon.pages && beacon.pages.length) {
      renderBarList('site-pages', beacon.pages, 'path', 'count', 'Nessuna pagina registrata.');
    } else {
      el('site-pages').innerHTML = `<p class="stats-empty">Le pagine più visitate compariranno dopo il beacon.</p>`;
    }

    const ghRef = (staticData.github && staticData.github.referrers) || [];
    renderBarList(
      'gh-referrers',
      ghRef.map((r) => ({ referrer: r.referrer || '(direct)', count: r.count })),
      'referrer',
      'count',
      'Dati GitHub non ancora raccolti (workflow giornaliero).'
    );
  }

  function renderWorkflows(runs) {
    const root = el('workflow-list');
    if (!runs || !runs.length) {
      root.innerHTML = '<p class="stats-empty">Nessuna esecuzione recente.</p>';
      return;
    }
    root.innerHTML = `<ul class="bar-list">${runs.map((run) => {
      const cls = run.conclusion === 'success' ? 'ok' : run.status === 'in_progress' ? 'run' : 'fail';
      const label = run.conclusion || run.status || 'unknown';
      return `
        <li>
          <span class="label">${run.name || run.display_title || 'Workflow'}</span>
          <span class="status-pill ${cls}">${label}</span>
          <div class="bar-track" style="opacity:0"></div>
        </li>`;
    }).join('')}</ul>`;
  }

  function renderUpdated(ts) {
    const node = el('stats-updated');
    if (node && ts) node.textContent = 'Aggiornato: ' + fmtDate.format(new Date(ts));
  }

  async function boot() {
    let staticData = {};
    try {
      staticData = await loadStaticStats();
      renderUpdated(staticData.updated_at);
    } catch (e) {
      el('kpi-grid').innerHTML = `<p class="stats-empty">${e.message}</p>`;
    }

    let beacon = null;
    try { beacon = await loadBeaconStats(); } catch (_) {}

    renderKpis(staticData, beacon);
    renderSiteSources(beacon, staticData);
    renderWorkflows(staticData.workflows || []);

    const keyInput = el('stats-key-input');
    const savedKey = sessionStorage.getItem(STATS_KEY_STORAGE);
    if (keyInput && savedKey) keyInput.value = savedKey;

    el('btn-save-stats-key')?.addEventListener('click', async () => {
      const key = keyInput.value.trim();
      if (key) sessionStorage.setItem(STATS_KEY_STORAGE, key);
      else sessionStorage.removeItem(STATS_KEY_STORAGE);
      location.reload();
    });

    el('btn-refresh')?.addEventListener('click', async () => {
      const btn = el('btn-refresh');
      const token = window.AbraAdmin && window.AbraAdmin.getGithubToken();
      if (!token) {
        alert('Serve il token GitHub (esci e rientra incollandolo al login).');
        return;
      }
      btn.disabled = true;
      btn.textContent = 'Aggiorno…';
      try {
        const live = await refreshLiveGithub(token);
        const views7 = sumDays(live.views, 7);
        el('live-gh-note').textContent =
          `Live GitHub: ${fmt.format(views7.count)} view repo (7 gg), ${fmt.format((live.repo && live.repo.stargazers_count) || 0)} stelle.`;
        if (live.referrers) {
          renderBarList(
            'gh-referrers',
            live.referrers.map((r) => ({ referrer: r.referrer || '(direct)', count: r.count })),
            'referrer',
            'count',
            'Nessun referrer GitHub.'
          );
        }
        if (live.workflow_runs) renderWorkflows(live.workflow_runs);
      } catch (ex) {
        alert(ex.message || 'Errore refresh GitHub');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Aggiorna da GitHub';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
