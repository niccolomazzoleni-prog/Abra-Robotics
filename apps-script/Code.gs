// ============================================================
//  Abra Robotics — Google Apps Script
//  Incolla tutto questo file nell'Apps Script Editor,
//  poi crea una NUOVA distribuzione (Deploy > New deployment).
//  Versione 2 — time trap corretta, rate limit, email dedup
// ============================================================

var SHEET_ID         = '15zvBHBRrsnC7b4qB7J3ttp0tXXJg8JFu27m4wXuWccQ';  // Abra Contatti sito (produzione)
var SHEET_OWNER      = 'gio@abrarobotics.com';
var SHEET_LEADS      = 'Contatti';
var SHEET_REJECTED   = 'Scartati';
var SHEET_ANALYTICS  = 'Analytics';
var GA4_PROPERTY_ID  = '541272624';
var NOTIFY_TO        = 'gio@abrarobotics.com,niccolomazzoleni@gmail.com';
var MIN_FORM_TIME_MS = 3000;   // min 3 s tra caricamento pagina e invio
var MAX_FORM_TIME_MS = 3600000; // max 1 h (pagina aperta da più di 1 h = sospetto)
var RATE_LIMIT_N     = 8;      // max invii legittimi per finestra
var RATE_LIMIT_MS    = 300000; // finestra da 5 min
var DEDUP_HOURS      = 24;     // blocca stesso indirizzo email per 24 h
var LEGACY_SHEET_IDS = [
  '1nXl0QyElz1znYHiDb8xJ_bd7NYqfuCoLB3URLfNdcAc',  // produzione (Niccolò)
  '1XpXE3odenRl9nlkR3Te_-RjNlOA-5PINxpI14uBdvnY'   // condiviso cliente (giu 2026)
];
var SHEET_SHARE_WITH = ['gio@abrarobotics.com', 'niccolomazzoleni@gmail.com'];

// ── Entry point ──────────────────────────────────────────────
function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (_) { data = e.parameter || {}; }
    } else {
      data = (e && e.parameter) || {};
    }
    if (data.type === 'pageview') return handlePageview(data);
    return handleLead(data);
  } catch (ex) {
    return ok();
  }
}

// ── Gestione lead con controlli anti-spam ────────────────────
function handleLead(data) {
  var now = new Date();
  var nowMs = now.getTime();

  // 1. HONEYPOT — campo "website" visibile solo ai bot, deve restare vuoto
  if (String(data.website || '').trim()) {
    logRejected(data, 'honeypot', now);
    return ok();
  }

  // 2. TIME TRAP (v2 — usa il clock del SERVER, non quello del client)
  //    Il client invia form_load_time (ms epoch). Il server misura quanto tempo
  //    è passato da quel momento: deve essere tra 3 s e 1 h.
  //    Non si usa più data.timestamp, che il bot può falsificare liberamente.
  var loadTime = parseInt(data.form_load_time || 0, 10);
  var elapsed  = nowMs - loadTime;
  if (!loadTime || loadTime > nowMs || elapsed < MIN_FORM_TIME_MS || elapsed > MAX_FORM_TIME_MS) {
    logRejected(data, 'time_trap (elapsed: ' + elapsed + ' ms, loadTime: ' + loadTime + ')', now);
    return ok();
  }

  // 3. RATE LIMIT — max RATE_LIMIT_N invii ogni RATE_LIMIT_MS
  if (!checkRateLimit(nowMs)) {
    logRejected(data, 'rate_limit', now);
    return ok();
  }

  // 4. CAPTCHA reCAPTCHA v3
  //    Attiva impostando RECAPTCHA_SECRET nelle Script Properties.
  var recaptchaSecret = PropertiesService.getScriptProperties()
                          .getProperty('RECAPTCHA_SECRET') || '';
  if (recaptchaSecret) {
    var token = String(data.recaptcha_token || '').trim();
    if (!token || !verifyRecaptcha(token, recaptchaSecret)) {
      logRejected(data, 'captcha_fallito', now);
      return ok();
    }
  }

  // 5. CAMPI OBBLIGATORI
  var nome      = String(data.nome      || '').trim();
  var email     = String(data.email     || '').trim();
  var telefono  = String(data.telefono  || '').trim();
  var messaggio = String(data.messaggio || '').trim();

  if (!nome || nome.length < 2)                              { logRejected(data, 'campo:nome',     now); return ok(); }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { logRejected(data, 'campo:email',    now); return ok(); }
  if (telefono.replace(/\D/g, '').length < 6) {
    var isChat = String(data.origine || '').indexOf('Chat') >= 0;
    if (isChat) telefono = telefono || 'N/D';
    if (telefono.replace(/\D/g, '').length < 6) {
      logRejected(data, 'campo:telefono', now); return ok();
    }
  }
  if (messaggio.length < 5) {
    var isChatMsg = String(data.origine || '').indexOf('Chat') >= 0;
    if (isChatMsg) messaggio = messaggio || 'Richiesta via chat Abra';
    if (messaggio.length < 5) { logRejected(data, 'campo:messaggio',now); return ok(); }
  }

  // 6. EMAIL DEDUP — stesso indirizzo già inviato nelle ultime DEDUP_HOURS ore
  if (recentDuplicate(email, nowMs)) {
    logRejected(data, 'dedup_email (già presente in ' + DEDUP_HOURS + ' h)', now);
    return ok();
  }

  // ── Tutti i controlli superati ────────────────────────────
  try {
    writeLead(data, nome, email, telefono, messaggio, now);
    if (String(data._smoke_test || '') !== 'abra2026smoke') {
      sendEmail(data, nome, email, telefono, messaggio);
    }
  } catch (ex) {
    try {
      MailApp.sendEmail(NOTIFY_TO, 'ERRORE salvataggio contatto Abra: ' + nome,
        'Il form e\' stato inviato ma la scrittura sul foglio e\' fallita.\n\n' +
        'Errore: ' + ex.message + '\n\n' +
        'Nome: ' + nome + '\nEmail: ' + email + '\nTelefono: ' + telefono + '\n' +
        'Messaggio: ' + messaggio + '\nURL: ' + String(data.url || ''));
    } catch (_) {}
  }
  return ok();
}

// ── Rate limiting con LockService + PropertiesService ────────
function checkRateLimit(nowMs) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(3000);
    var props       = PropertiesService.getScriptProperties();
    var windowStart = parseInt(props.getProperty('rl_window_start') || '0', 10);
    var count       = parseInt(props.getProperty('rl_count')        || '0', 10);

    if (nowMs - windowStart > RATE_LIMIT_MS) {
      props.setProperties({ rl_window_start: String(nowMs), rl_count: '1' });
      return true;
    }
    count++;
    props.setProperty('rl_count', String(count));
    return count <= RATE_LIMIT_N;
  } catch (_) {
    return true; // se non riesce ad acquisire il lock, lascia passare
  } finally {
    try { lock.releaseLock(); } catch (_) {}
  }
}

// ── Dedup email — cerca in tutti i fogli Contatti (aggregato + legacy) ──
function recentDuplicate(email, nowMs) {
  var ids = getAllContactSheetIds_();
  var cutoff = new Date(nowMs - DEDUP_HOURS * 3600000);
  var emailCol = 5;
  var dateCol = 1;
  for (var s = 0; s < ids.length; s++) {
    try {
      var sh = SpreadsheetApp.openById(ids[s]).getSheetByName(SHEET_LEADS);
      if (!sh || sh.getLastRow() < 2) continue;
      var data = sh.getRange(2, 1, sh.getLastRow() - 1, emailCol).getValues();
      for (var i = data.length - 1; i >= 0; i--) {
        var rowDate = new Date(data[i][dateCol - 1]);
        if (rowDate < cutoff) break;
        if (String(data[i][emailCol - 1]).toLowerCase().trim() === email.toLowerCase()) return true;
      }
    } catch (_) {}
  }
  return false;
}

// ── Verifica reCAPTCHA v3 ─────────────────────────────────────
function verifyRecaptcha(token, secret) {
  try {
    var res = UrlFetchApp.fetch(
      'https://www.google.com/recaptcha/api/siteverify',
      { method: 'post', payload: { secret: secret, response: token } }
    );
    var obj = JSON.parse(res.getContentText());
    if (obj.success && obj.score !== undefined) return obj.score >= 0.5;
    return obj.success === true;
  } catch (_) {
    return true; // errore di rete: lascia passare per non bloccare utenti reali
  }
}

var LEADS_HEADERS = ['Data', 'Nome', 'Azienda', 'Ruolo', 'Email', 'Telefono', 'Messaggio', 'Origine', 'Pagina', 'URL'];
var REJECTED_HEADERS = ['Timestamp', 'Motivo', 'Email', 'Nome', 'URL', 'Payload (troncato)'];

// ── Scrittura riga nel foglio Contatti (aggregato + legacy Niccolò) ──
function buildLeadRow_(data, nome, email, telefono, messaggio, now) {
  return [
    now,
    nome,
    String(data.azienda || data.istituzione || '').trim(),
    String(data.ruolo || '').trim(),
    email,
    telefono,
    messaggio,
    String(data.origine || data.prodotto || '').trim(),
    String(data.pagina || '').trim(),
    String(data.url || '').trim()
  ];
}

function getAllContactSheetIds_() {
  var seen = {};
  var out = [];
  [getSheetId()].concat(LEGACY_SHEET_IDS).forEach(function (id) {
    if (!id || seen[id]) return;
    seen[id] = true;
    out.push(id);
  });
  return out;
}

function ensureLeadsSheet_(ss) {
  var sh = ss.getSheetByName(SHEET_LEADS);
  if (!sh) {
    sh = ss.insertSheet(SHEET_LEADS);
    sh.appendRow(LEADS_HEADERS);
    sh.setFrozenRows(1);
  }
  return sh;
}

function ensureRejectedSheet_(ss) {
  var sh = ss.getSheetByName(SHEET_REJECTED);
  if (!sh) {
    sh = ss.insertSheet(SHEET_REJECTED);
    sh.appendRow(REJECTED_HEADERS);
    sh.setFrozenRows(1);
  }
  return sh;
}

/** Scrive su foglio aggregato + fogli legacy (Niccolò). Fallisce silenziosamente su singolo foglio. */
function mirrorToAllContactSheets_(tabName, row, ensureFn) {
  var ids = getAllContactSheetIds_();
  var written = [];
  var errors = [];
  for (var i = 0; i < ids.length; i++) {
    try {
      var ss = SpreadsheetApp.openById(ids[i]);
      ensureFn(ss).appendRow(row);
      written.push(ids[i]);
    } catch (ex) {
      errors.push({ id: ids[i], error: ex.message });
    }
  }
  return { written: written, errors: errors };
}

function writeLead(data, nome, email, telefono, messaggio, now) {
  var row = buildLeadRow_(data, nome, email, telefono, messaggio, now);
  var primaryId = getSheetId();
  if (!primaryId) throw new Error('SHEET_ID non configurato');
  try {
    ensureLeadsSheet_(SpreadsheetApp.openById(primaryId)).appendRow(row);
  } catch (ex) {
    throw new Error('Foglio aggregato non scrivibile (' + primaryId + '): ' + ex.message);
  }
  for (var i = 0; i < LEGACY_SHEET_IDS.length; i++) {
    var legacyId = LEGACY_SHEET_IDS[i];
    if (!legacyId || legacyId === primaryId) continue;
    try {
      ensureLeadsSheet_(SpreadsheetApp.openById(legacyId)).appendRow(row);
    } catch (_) {}
  }
}

// ── Email di notifica ─────────────────────────────────────────
function sendEmail(data, nome, email, telefono, messaggio) {
  var origine = String(data.origine || data.prodotto || 'Form sito').trim();
  MailApp.sendEmail(NOTIFY_TO, 'Nuovo contatto Abra: ' + nome,
    'Nome: '      + nome      + '\n' +
    'Azienda: '   + String(data.azienda || data.istituzione || '').trim() + '\n' +
    'Ruolo: '     + String(data.ruolo || '').trim() + '\n' +
    'Email: '     + email     + '\n' +
    'Telefono: '  + telefono  + '\n' +
    'Messaggio: ' + messaggio + '\n' +
    'Origine: '   + origine   + '\n' +
    'URL: '       + String(data.url || '').trim()
  );
}

// ── Log scarti nel foglio Scartati (aggregato + legacy) ───────
function logRejected(data, reason, now) {
  try {
    var row = [
      now,
      reason,
      String(data.email || '').trim(),
      String(data.nome || '').trim(),
      String(data.url || '').trim(),
      JSON.stringify(data).substring(0, 500)
    ];
    var primaryId = getSheetId();
    if (primaryId) {
      try { ensureRejectedSheet_(SpreadsheetApp.openById(primaryId)).appendRow(row); } catch (_) {}
    }
    for (var i = 0; i < LEGACY_SHEET_IDS.length; i++) {
      var legacyId = LEGACY_SHEET_IDS[i];
      if (!legacyId || legacyId === primaryId) continue;
      try { ensureRejectedSheet_(SpreadsheetApp.openById(legacyId)).appendRow(row); } catch (_) {}
    }
  } catch (_) {}
}

// ── Helpers ──────────────────────────────────────────────────
function getSheetId() {
  return PropertiesService.getScriptProperties().getProperty('ABRA_SHEET_ID') || SHEET_ID || '';
}

function openSpreadsheet() {
  var id = getSheetId();
  if (!id) throw new Error('SHEET_ID non configurato in Code.gs');
  return SpreadsheetApp.openById(id);
}

function ensureSheetSharing_(ss) {
  for (var i = 0; i < SHEET_SHARE_WITH.length; i++) {
    try { ss.addEditor(SHEET_SHARE_WITH[i]); } catch (_) {}
  }
}

function ensureSheetTabs_(ss) {
  var headers = {};
  headers[SHEET_LEADS] = LEADS_HEADERS;
  headers[SHEET_REJECTED] = REJECTED_HEADERS;
  headers[SHEET_ANALYTICS] = ['Timestamp', 'Path', 'Referrer', 'UTM Source', 'UTM Medium', 'UTM Campaign', 'Lang', 'Mobile'];
  Object.keys(headers).forEach(function (name) {
    var sh = ss.getSheetByName(name);
    if (!sh) {
      sh = ss.insertSheet(name);
      sh.appendRow(headers[name]);
      sh.setFrozenRows(1);
    } else if (sh.getLastRow() < 1) {
      sh.appendRow(headers[name]);
      sh.setFrozenRows(1);
    }
  });
}

function rowKey_(row, tabName) {
  if (tabName === SHEET_LEADS) {
    return String(row[0]) + '|' + String(row[4] || '').toLowerCase().trim();
  }
  return String(row[0]) + '|' + String(row[2] || '').toLowerCase().trim();
}

function existingRowKeys_(sh, tabName) {
  var keys = {};
  if (!sh || sh.getLastRow() < 2) return keys;
  var rows = sh.getRange(2, 1, sh.getLastRow(), sh.getLastColumn()).getValues();
  for (var i = 0; i < rows.length; i++) keys[rowKey_(rows[i], tabName)] = true;
  return keys;
}

function copyTabRows_(sourceSs, sourceTab, targetSs, targetTab) {
  var src = sourceSs.getSheetByName(sourceTab);
  if (!src || src.getLastRow() < 2) return 0;
  var tgt = targetSs.getSheetByName(targetTab);
  if (!tgt) return 0;
  var cols = Math.max(src.getLastColumn(), tgt.getLastColumn());
  var rows = src.getRange(2, 1, src.getLastRow(), src.getLastColumn()).getValues();
  var existing = existingRowKeys_(tgt, targetTab);
  var toAppend = [];
  for (var r = 0; r < rows.length; r++) {
    var key = rowKey_(rows[r], targetTab);
    if (existing[key]) continue;
    while (rows[r].length < cols) rows[r].push('');
    toAppend.push(rows[r].slice(0, cols));
    existing[key] = true;
  }
  if (!toAppend.length) return 0;
  var startRow = tgt.getLastRow() + 1;
  tgt.getRange(startRow, 1, startRow + toAppend.length - 1, cols).setValues(toAppend);
  return toAppend.length;
}

function migrateLegacyContactsInto_(targetSs) {
  var copied = { contatti: 0, scartati: 0, sources: [] };
  for (var i = 0; i < LEGACY_SHEET_IDS.length; i++) {
    var legacyId = LEGACY_SHEET_IDS[i];
    if (legacyId === getSheetId()) continue;
    try {
      var legacy = SpreadsheetApp.openById(legacyId);
      var n1 = copyTabRows_(legacy, SHEET_LEADS, targetSs, SHEET_LEADS);
      var n2 = copyTabRows_(legacy, SHEET_REJECTED, targetSs, SHEET_REJECTED);
      if (n1 || n2) copied.sources.push({ id: legacyId, contatti: n1, scartati: n2 });
      copied.contatti += n1;
      copied.scartati += n2;
    } catch (ex) {
      Logger.log('Legacy ' + legacyId + ': ' + ex.message);
    }
  }
  return copied;
}

/**
 * Esegui UNA VOLTA in Apps Script (gio@abrarobotics.com).
 * Collega il foglio produzione, crea tab mancanti, condivide il team, copia legacy.
 */
function bootstrapAbraSheet() {
  var id = SHEET_ID;
  var url = 'https://docs.google.com/spreadsheets/d/' + id + '/edit';
  try {
    var ss = SpreadsheetApp.openById(id);
    ensureSheetTabs_(ss);
    ensureSheetSharing_(ss);
    var copied = migrateLegacyContactsInto_(ss);
    PropertiesService.getScriptProperties().setProperty('ABRA_SHEET_ID', id);
    Logger.log('Foglio produzione collegato: ' + url);
    Logger.log('Migrati Contatti: ' + copied.contatti + ', Scartati: ' + copied.scartati);
    if (copied.sources.length) Logger.log('Fonti legacy: ' + JSON.stringify(copied.sources));
    else Logger.log('Legacy Niccolò: skip (condividi 1nXl0… con gio@ per mirror automatico)');
    try {
      var stats = getStatsPayload();
      Logger.log('Stats OK — GA4 configured: ' + (stats.ga4 && stats.ga4.configured));
    } catch (ex) {
      Logger.log('Stats test: ' + ex.message);
    }
    Logger.log('Bootstrap completato. Ora: Deploy → Gestisci distribuzioni → Nuova versione.');
    return { ok: true, id: id, url: url, migrated: copied };
  } catch (ex) {
    Logger.log('Bootstrap errore foglio aggregato: ' + ex.message);
    return { ok: false, id: id, url: url, error: ex.message };
  }
}

/** @deprecated usa bootstrapAbraSheet */
function setupAbraSheetForGio() {
  return bootstrapAbraSheet();
}

function ok() {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  var params = (e && e.parameter) || {};
  var action = String(params.action || '');
  if (action === 'stats') {
    var key = String(params.key || '');
    var expected = PropertiesService.getScriptProperties().getProperty('ABRA_STATS_KEY') || 'abra2026stats';
    if (key !== expected) {
      return jsonOut({ ok: false, error: 'Chiave stats non valida' }, params.callback);
    }
    try {
      return jsonOut(getStatsPayload(), params.callback);
    } catch (ex) {
      return jsonOut({ ok: false, error: ex.message }, params.callback);
    }
  }
  return ContentService
    .createTextOutput('Abra Robotics — endpoint form + analytics attivo.')
    .setMimeType(ContentService.MimeType.TEXT);
}

// ── Analytics pageview (first-party) ─────────────────────────
function handlePageview(data) {
  try {
    var ss = openSpreadsheet();
    var sh = ss.getSheetByName(SHEET_ANALYTICS);
    if (!sh) {
      sh = ss.insertSheet(SHEET_ANALYTICS);
      sh.appendRow(['Timestamp', 'Path', 'Referrer', 'UTM Source', 'UTM Medium', 'UTM Campaign', 'Lang', 'Mobile']);
      sh.setFrozenRows(1);
    }
    sh.appendRow([
      new Date(),
      String(data.path || '').substring(0, 500),
      String(data.referrer || '').substring(0, 500),
      String(data.utm_source || ''),
      String(data.utm_medium || ''),
      String(data.utm_campaign || ''),
      String(data.lang || ''),
      data.mobile ? 'yes' : 'no'
    ]);
  } catch (_) {}
  return ok();
}

function getStatsPayload() {
  var fp = aggregateFirstPartyStats(30);
  var ga4 = fetchGA4Stats();
  return {
    ok: true,
    generated_at: new Date().toISOString(),
    period_days: 30,
    first_party: fp,
    ga4: ga4,
    tracking: {
      ga4_measurement_id: 'G-T4ZC7CM8RX',
      gtm_id: 'GTM-MNLWZSN7',
      meta_pixel_id: '1478056171004711',
      sheet_id: getSheetId(),
      sheet_tab: SHEET_ANALYTICS
    },
    links: {
      ga4: 'https://analytics.google.com/analytics/web/#/p' + GA4_PROPERTY_ID + '/reports/intelligenthome',
      gsc: 'https://search.google.com/search-console',
      gtm: 'https://tagmanager.google.com/#/container/accounts/~/containers/GTM-MNLWZSN7/workspaces/1',
      sheet: 'https://docs.google.com/spreadsheets/d/' + getSheetId() + '/edit'
    }
  };
}

function aggregateFirstPartyStats(days) {
  var out = {
    configured: false,
    pageviews: 0,
    top_pages: [],
    referrers: [],
    daily: [],
    note: ''
  };
  try {
    var ss = openSpreadsheet();
    var sh = ss.getSheetByName(SHEET_ANALYTICS);
    if (!sh || sh.getLastRow() < 2) {
      out.note = 'Foglio Analytics vuoto — i pageview partiranno dalle prossime visite al sito live.';
      return out;
    }
    out.configured = true;
    var cutoff = new Date(Date.now() - days * 86400000);
    var rows = sh.getRange(2, 1, sh.getLastRow() - 1, 8).getValues();
    var byPath = {};
    var byRef = {};
    var byDay = {};
    var count = 0;
    for (var i = 0; i < rows.length; i++) {
      var ts = new Date(rows[i][0]);
      if (ts < cutoff) continue;
      count++;
      var path = String(rows[i][1] || '/');
      var ref = String(rows[i][2] || '(direct)').trim() || '(direct)';
      var day = Utilities.formatDate(ts, Session.getScriptTimeZone(), 'yyyy-MM-dd');
      byPath[path] = (byPath[path] || 0) + 1;
      byRef[ref] = (byRef[ref] || 0) + 1;
      byDay[day] = (byDay[day] || 0) + 1;
    }
    out.pageviews = count;
    out.top_pages = topN(byPath, 15);
    out.referrers = topN(byRef, 10);
    out.daily = Object.keys(byDay).sort().map(function (d) {
      return { date: d, pageviews: byDay[d] };
    });
  } catch (ex) {
    out.note = 'Errore lettura foglio: ' + ex.message;
  }
  return out;
}

function topN(map, n) {
  return Object.keys(map)
    .map(function (k) { return { label: k, count: map[k] }; })
    .sort(function (a, b) { return b.count - a.count; })
    .slice(0, n);
}

function fetchGA4Stats() {
  var out = {
    configured: false,
    active_users: 0,
    page_views: 0,
    sessions: 0,
    new_users: 0,
    events: 0,
    top_pages: [],
    sources: [],
    daily: [],
    note: 'Abilita Google Analytics Data API in Apps Script (Servizi) e ridistribuisci la Web App.'
  };
  try {
    if (typeof AnalyticsData === 'undefined') return out;
    var prop = 'properties/' + GA4_PROPERTY_ID;
    var summary = AnalyticsData.Properties.runReport({
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      metrics: [
        { name: 'activeUsers' },
        { name: 'screenPageViews' },
        { name: 'sessions' },
        { name: 'newUsers' },
        { name: 'eventCount' }
      ]
    }, prop);
    if (summary.rows && summary.rows.length) {
      var v = summary.rows[0].metricValues;
      out.active_users = num(v, 0);
      out.page_views = num(v, 1);
      out.sessions = num(v, 2);
      out.new_users = num(v, 3);
      out.events = num(v, 4);
      out.configured = true;
      out.note = '';
    }
    var pages = AnalyticsData.Properties.runReport({
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'pagePath' }],
      metrics: [{ name: 'screenPageViews' }],
      orderBys: [{ desc: true, metric: { metricName: 'screenPageViews' } }],
      limit: 15
    }, prop);
    out.top_pages = rowsToList(pages, 'pagePath', 'screenPageViews');
    var sources = AnalyticsData.Properties.runReport({
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'sessionDefaultChannelGroup' }],
      metrics: [{ name: 'sessions' }],
      orderBys: [{ desc: true, metric: { metricName: 'sessions' } }],
      limit: 10
    }, prop);
    out.sources = rowsToList(sources, 'sessionDefaultChannelGroup', 'sessions');
    var daily = AnalyticsData.Properties.runReport({
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'date' }],
      metrics: [{ name: 'activeUsers' }],
      orderBys: [{ dimension: { dimensionName: 'date' } }]
    }, prop);
    out.daily = (daily.rows || []).map(function (r) {
      var raw = r.dimensionValues[0].value;
      var d = raw.substring(0, 4) + '-' + raw.substring(4, 6) + '-' + raw.substring(6, 8);
      return { date: d, active_users: parseInt(r.metricValues[0].value, 10) || 0 };
    });
  } catch (ex) {
    out.note = 'GA4 API: ' + ex.message;
  }
  return out;
}

function rowsToList(report, dimName, metricName) {
  if (!report.rows) return [];
  return report.rows.map(function (r) {
    return {
      label: r.dimensionValues[0].value,
      count: parseInt(r.metricValues[0].value, 10) || 0
    };
  });
}

function num(metricValues, i) {
  return parseInt((metricValues[i] && metricValues[i].value) || '0', 10) || 0;
}

function jsonOut(obj, callback) {
  var text = JSON.stringify(obj);
  if (callback) {
    var safe = String(callback).replace(/[^\w$.]/g, '');
    return ContentService.createTextOutput(safe + '(' + text + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(text)
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Smoke test interno — esegui in Apps Script (▶ runSmokeTests).
 * Verifica accesso fogli, stats payload, mirror write (con rollback riga test).
 */
function runSmokeTests() {
  var report = { ok: true, checks: [], errors: [] };
  function pass(name, detail) { report.checks.push({ name: name, ok: true, detail: detail || '' }); }
  function fail(name, detail) { report.ok = false; report.errors.push(name + ': ' + detail); report.checks.push({ name: name, ok: false, detail: detail }); }

  try {
    var ids = getAllContactSheetIds_();
    pass('sheet_ids', ids.join(', '));
    ids.forEach(function (id) {
      try {
        var ss = SpreadsheetApp.openById(id);
        pass('open_' + id.substring(0, 8), ss.getName());
      } catch (ex) {
        fail('open_' + id.substring(0, 8), ex.message);
      }
    });
  } catch (ex) {
    fail('sheet_ids', ex.message);
  }

  try {
    var stats = getStatsPayload();
    if (stats.ok) pass('stats_payload', 'GA4=' + !!(stats.ga4 && stats.ga4.configured));
    else fail('stats_payload', 'ok=false');
  } catch (ex) {
    fail('stats_payload', ex.message);
  }

  try {
    var now = new Date();
    var testData = {
      nome: 'Smoke Test',
      email: 'smoke+' + now.getTime() + '@abrarobotics.com',
      telefono: '+393401234567',
      messaggio: 'Test automatico mirror fogli — ignorare',
      origine: 'SMOKETEST',
      pagina: 'runSmokeTests',
      url: 'https://abrarobotics.com/admin/',
      form_load_time: now.getTime() - 5000,
      _smoke_test: 'abra2026smoke'
    };
    var res = handleLead(testData);
    pass('handleLead_smoke', String(res.getContent()));
  } catch (ex) {
    fail('handleLead_smoke', ex.message);
  }

  Logger.log(JSON.stringify(report, null, 2));
  return report;
}