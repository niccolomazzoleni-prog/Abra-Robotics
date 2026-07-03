// ============================================================
//  Abra Robotics — Google Apps Script
//  Incolla tutto questo file nell'Apps Script Editor,
//  poi crea una NUOVA distribuzione (Deploy > New deployment).
//  Versione 2 — time trap corretta, rate limit, email dedup
// ============================================================

var SHEET_ID         = '1XpXE3odenRl9nlkR3Te_-RjNlOA-5PINxpI14uBdvnY';
var SHEET_LEADS      = 'Contatti';
var SHEET_REJECTED   = 'Scartati';
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
    if (data.type === 'pageview') return ok();
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

function doGet() {
  return ContentService
    .createTextOutput('Abra Robotics — endpoint form attivo.')
    .setMimeType(ContentService.MimeType.TEXT);
}
