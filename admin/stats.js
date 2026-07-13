/* Carica statistiche sito (GA4 + first-party) nell'admin Abra */
(function () {
  'use strict';

  const CONFIG_URL = '../data/analytics-config.json';
  let config = {};

  function el(id) { return document.getElementById(id); }
  function fmt(n) { return (n || 0).toLocaleString('it-IT'); }

  function fetchStatsJsonp(baseUrl, key) {
    return new Promise(function (resolve, reject) {
      var cb = 'abraStatsCb_' + Date.now();
      var script = document.createElement('script');
      var timer = setTimeout(function () {
        cleanup();
        reject(new Error('Timeout API stats (15s)'));
      }, 15000);
      function cleanup() {
        clearTimeout(timer);
        delete window[cb];
        if (script.parentNode) script.parentNode.removeChild(script);
      }
      window[cb] = function (data) {
        cleanup();
        resolve(data);
      };
      script.onerror = function () {
        cleanup();
        reject(new Error('Impossibile contattare Apps Script. Ridistribuisci la Web App.'));
      };
      script.src = baseUrl + '?action=stats&key=' + encodeURIComponent(key) + '&callback=' + cb;
      document.head.appendChild(script);
    });
  }

  function renderBars(container, items, maxItems) {
    if (!items || !items.length) {
      container.innerHTML = '<p class="stats-empty">Nessun dato nel periodo.</p>';
      return;
    }
    var slice = items.slice(0, maxItems || 10);
    var max = slice[0].count || 1;
    container.innerHTML = slice.map(function (item) {
      var pct = Math.round((item.count / max) * 100);
      var label = item.label.length > 40 ? item.label.substring(0, 38) + '…' : item.label;
      return '<div class="stats-bar-row">' +
        '<span class="stats-bar-label" title="' + escapeHtml(item.label) + '">' + escapeHtml(label) + '</span>' +
        '<div class="stats-bar-track"><div class="stats-bar-fill" style="width:' + pct + '%"></div></div>' +
        '<span class="stats-bar-val">' + fmt(item.count) + '</span></div>';
    }).join('');
  }

  function renderTable(container, items, colLabel, colCount) {
    if (!items || !items.length) {
      container.innerHTML = '<p class="stats-empty">Nessun dato.</p>';
      return;
    }
    container.innerHTML = '<div class="stats-table-wrap"><table class="stats-table"><thead><tr><th>' +
      colLabel + '</th><th>' + colCount + '</th></tr></thead><tbody>' +
      items.map(function (r) {
        return '<tr><td>' + escapeHtml(r.label) + '</td><td><strong>' + fmt(r.count) + '</strong></td></tr>';
      }).join('') + '</tbody></table></div>';
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  }

  function renderKpis(data) {
    var ga4 = data.ga4 || {};
    var fp = data.first_party || {};
    el('kpi-grid').innerHTML =
      kpi('ga4', 'Utenti attivi GA4', ga4.active_users, 'Ultimi 30 giorni · Google Analytics') +
      kpi('ga4', 'Visualizzazioni GA4', ga4.page_views, 'screenPageViews') +
      kpi('ga4', 'Sessioni GA4', ga4.sessions, '') +
      kpi('ga4', 'Nuovi utenti GA4', ga4.new_users, '') +
      kpi('ga4', 'Eventi GA4', ga4.events, '') +
      kpi('fp', 'Pageview first-party', fp.pageviews, 'Beacon Abra → foglio Analytics') +
      kpi('fp', 'Pagine tracciate', (fp.top_pages || []).length, 'Percorsi distinti nel periodo');
  }

  function kpi(cls, label, value, sub) {
    return '<div class="stats-kpi ' + cls + '"><div class="stats-kpi-label">' + label +
      '</div><div class="stats-kpi-value">' + fmt(value) + '</div>' +
      (sub ? '<div class="stats-kpi-sub">' + sub + '</div>' : '') + '</div>';
  }

  function renderSetup(data) {
    var notes = [];
    if (!data.first_party || !data.first_party.configured) {
      notes.push('Il foglio <strong>Analytics</strong> è vuoto: ridistribuisci Apps Script (<code>Code.gs</code> aggiornato) e visita il sito live.');
    }
    if (!data.ga4 || !data.ga4.configured) {
      notes.push('GA4 API non attiva in Apps Script: <strong>Servizi → Google Analytics Data API</strong> → ON, poi <strong>Nuova versione Web App</strong>.');
    }
    notes.push('In Search Console invia la sitemap: <a href="' + (config.sitemap_url || '') + '" target="_blank" rel="noopener">' + (config.sitemap_url || 'sitemap.xml') + '</a>');
    el('stats-setup').innerHTML = notes.length
      ? '<strong>Configurazione</strong><ol>' + notes.map(function (n) { return '<li>' + n + '</li>'; }).join('') + '</ol>'
      : '<strong>Tutto collegato.</strong> GA4 + pageview first-party attivi.';
  }

  function renderAll(data) {
    renderKpis(data);
    renderSetup(data);

    var ga4Badge = el('ga4-badge');
    if (data.ga4 && data.ga4.configured) {
      ga4Badge.textContent = 'GA4 connesso';
      ga4Badge.className = 'stats-badge ok';
    } else {
      ga4Badge.textContent = 'GA4 da collegare in Apps Script';
      ga4Badge.className = 'stats-badge warn';
    }
    if (data.ga4 && data.ga4.note) el('ga4-note').textContent = data.ga4.note;

    var fpBadge = el('fp-badge');
    if (data.first_party && data.first_party.configured) {
      fpBadge.textContent = 'Beacon attivo';
      fpBadge.className = 'stats-badge ok';
    } else {
      fpBadge.textContent = 'In attesa dati';
      fpBadge.className = 'stats-badge warn';
    }
    if (data.first_party && data.first_party.note) el('fp-note').textContent = data.first_party.note;

    renderTable(el('ga4-pages'), data.ga4 && data.ga4.top_pages, 'Pagina', 'Views');
    renderBars(el('ga4-sources'), data.ga4 && data.ga4.sources, 8);
    renderTable(el('fp-pages'), data.first_party && data.first_party.top_pages, 'Path', 'Views');
    renderBars(el('fp-referrers'), data.first_party && data.first_party.referrers, 8);

    var links = data.links || config.links || {};
    el('stats-links').innerHTML = [
      ['GA4 completo', links.ga4 || config.links.ga4_dashboard],
      ['Search Console', links.gsc || config.links.search_console],
      ['Tag Manager', links.gtm || config.links.tag_manager],
      ['Foglio Google', links.sheet]
    ].filter(function (x) { return x[1]; }).map(function (x) {
      return '<a href="' + x[1] + '" target="_blank" rel="noopener">' + x[0] + ' ↗</a>';
    }).join('');

    el('stats-meta').textContent = 'Aggiornato: ' + (data.generated_at ? new Date(data.generated_at).toLocaleString('it-IT') : '—');
    el('stats-loading').style.display = 'none';
    el('stats-content').style.display = 'block';
  }

  function showError(msg) {
    el('stats-loading').innerHTML = '<p style="color:#b91c1c">' + escapeHtml(msg) + '</p>' +
      '<p class="stats-empty">Verifica che Apps Script sia ridistribuito con il nuovo <code>Code.gs</code> (analytics).</p>';
  }

  async function init() {
    try {
      config = await fetch(CONFIG_URL).then(function (r) { return r.json(); });
    } catch (_) {
      config = { stats_read_key: 'abra2026stats', google_script_url: window.GOOGLE_SCRIPT_URL || '' };
    }
    var url = config.google_script_url || 'https://script.google.com/a/macros/abrarobotics.com/s/AKfycbwdJ4taKMGrLP79eQDujrx7vxhbmGI-qhkvlD9k9kLqyUGDOWW-_3_HFMAxqvooPaY1/exec';
    var key = config.stats_read_key || 'abra2026stats';
    try {
      var data = await fetchStatsJsonp(url, key);
      if (!data.ok) throw new Error(data.error || 'Risposta non valida');
      renderAll(data);
    } catch (ex) {
      showError(ex.message);
    }
    el('btn-refresh').addEventListener('click', function () {
      location.reload();
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
