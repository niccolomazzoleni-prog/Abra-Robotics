// ============================================================
//  Abra Robotics — Google Apps Script
//  Incolla tutto questo file nell'Apps Script Editor,
//  poi crea una NUOVA distribuzione (Deploy > New deployment).
//  Versione 2 — time trap corretta, rate limit, email dedup
// ============================================================

var SHEET_ID         = '1nXl0QyElz1znYHiDb8xJ_bd7NYqfuCoLB3URLfNdcAc';
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
  if (telefono.replace(/\D/g, '').length < 6)               { logRejected(data, 'campo:telefono', now); return ok(); }
  if (messaggio.length < 5)                                  { logRejected(data, 'campo:messaggio',now); return ok(); }

  // 6. EMAIL DEDUP — stesso indirizzo già inviato nelle ultime DEDUP_HOURS ore
  if (recentDuplicate(email, nowMs)) {
    logRejected(data, 'dedup_email (già presente in ' + DEDUP_HOURS + ' h)', now);
    return ok();
  }

  // ── Tutti i controlli superati ────────────────────────────
  writeLead(data, nome, email, telefono, messaggio, now);
  sendEmail(data, nome, email, telefono, messaggio);
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

// ── Dedup email — cerca nel foglio Contatti ──────────────────
function recentDuplicate(email, nowMs) {
  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sh = ss.getSheetByName(SHEET_LEADS);
    if (!sh || sh.getLastRow() < 2) return false;
    var cutoff  = new Date(nowMs - DEDUP_HOURS * 3600000);
    var emailCol = 5; // colonna E = Email (1-based)
    var dateCol  = 1; // colonna A = Data
    var data    = sh.getRange(2, 1, sh.getLastRow() - 1, emailCol).getValues();
    for (var i = data.length - 1; i >= 0; i--) {
      var rowDate = new Date(data[i][dateCol - 1]);
      if (rowDate < cutoff) break; // righe ordinate per data, possiamo uscire
      if (String(data[i][emailCol - 1]).toLowerCase().trim() === email.toLowerCase()) return true;
    }
  } catch (_) {}
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

// ── Scrittura riga nel foglio Contatti ───────────────────────
function writeLead(data, nome, email, telefono, messaggio, now) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(SHEET_LEADS);
  if (!sh) {
    sh = ss.insertSheet(SHEET_LEADS);
    sh.appendRow(['Data','Nome','Azienda','Ruolo','Email','Telefono','Messaggio','Origine','Pagina','URL']);
    sh.setFrozenRows(1);
  }
  sh.appendRow([
    now,
    nome,
    String(data.azienda   || data.istituzione || '').trim(),
    String(data.ruolo     || '').trim(),
    email,
    telefono,
    messaggio,
    String(data.origine   || data.prodotto || '').trim(),
    String(data.pagina    || '').trim(),
    String(data.url       || '').trim()
  ]);
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

// ── Log scarti nel foglio Scartati ───────────────────────────
function logRejected(data, reason, now) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(SHEET_REJECTED);
  if (!sh) {
    sh = ss.insertSheet(SHEET_REJECTED);
    sh.appendRow(['Timestamp', 'Motivo', 'Email', 'Nome', 'URL', 'Payload (troncato)']);
    sh.setFrozenRows(1);
  }
  sh.appendRow([
    now,
    reason,
    String(data.email || '').trim(),
    String(data.nome  || '').trim(),
    String(data.url   || '').trim(),
    JSON.stringify(data).substring(0, 500)
  ]);
}

// ── Helpers ──────────────────────────────────────────────────
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
    return jsonOut(getStatsPayload(), params.callback);
  }
  return ContentService
    .createTextOutput('Abra Robotics — endpoint form + analytics attivo.')
    .setMimeType(ContentService.MimeType.TEXT);
}

// ── Analytics pageview (first-party) ─────────────────────────
function handlePageview(data) {
  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
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
      sheet_id: SHEET_ID,
      sheet_tab: SHEET_ANALYTICS
    },
    links: {
      ga4: 'https://analytics.google.com/analytics/web/#/p' + GA4_PROPERTY_ID + '/reports/intelligenthome',
      gsc: 'https://search.google.com/search-console',
      gtm: 'https://tagmanager.google.com/#/container/accounts/~/containers/GTM-MNLWZSN7/workspaces/1',
      sheet: 'https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/edit'
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
    var ss = SpreadsheetApp.openById(SHEET_ID);
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