var SHEET_ID   = '1XpXE3odenRl9nlkR3Te_-RjNlOA-5PINxpI14uBdvnY';
var SHEET_NAME = 'Contatti';
var NOTIFY_TO  = 'gio@abrarobotics.com,niccolomazzoleni@gmail.com';

// reCAPTCHA v3 secret key — inserisci dopo registrazione su https://www.google.com/recaptcha/admin
// Lascia vuoto per disabilitare la verifica (non consigliato in produzione)
var RECAPTCHA_SECRET = '';

function verifyRecaptcha(token) {
  if (!RECAPTCHA_SECRET) return true;
  if (!token) return false;
  var res = UrlFetchApp.fetch('https://www.google.com/recaptcha/api/siteverify', {
    method: 'post',
    payload: { secret: RECAPTCHA_SECRET, response: token }
  });
  var result = JSON.parse(res.getContentText());
  return result.success === true && (result.score === undefined || result.score >= 0.5);
}

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); } catch (_) { data = e.parameter || {}; }
    } else {
      data = (e && e.parameter) || {};
    }

    // Honeypot
    if (data._gotcha && String(data._gotcha).trim()) {
      return ok();
    }

    // Validazione campi obbligatori
    var nome     = String(data.nome     || '').trim();
    var email    = String(data.email    || '').trim();
    var telefono = String(data.telefono || '').trim();
    var messaggio = String(data.messaggio || '').trim();

    if (!nome || nome.length < 2)      return err('missing_nome');
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return err('invalid_email');
    if (!telefono || telefono.replace(/\D/g, '').length < 6)     return err('missing_telefono');
    if (!messaggio || messaggio.length < 5)                       return err('missing_messaggio');

    // reCAPTCHA
    if (!verifyRecaptcha(data.recaptcha_token)) return err('captcha_failed');

    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

    if (sh.getLastRow() === 0) {
      sh.appendRow(['Data','Nome','Azienda','Ruolo','Email','Telefono','Messaggio','Origine','Pagina','URL']);
    }

    sh.appendRow([
      new Date(),
      nome,
      String(data.azienda   || '').trim(),
      String(data.ruolo     || '').trim(),
      email,
      telefono,
      messaggio,
      String(data.origine   || data.prodotto || '').trim(),
      String(data.pagina    || '').trim(),
      String(data.url       || '').trim()
    ]);

    var corpo =
      'Nome: '      + nome + '\n' +
      'Azienda: '   + (data.azienda   || '') + '\n' +
      'Ruolo: '     + (data.ruolo     || '') + '\n' +
      'Email: '     + email + '\n' +
      'Telefono: '  + telefono + '\n' +
      'Messaggio: ' + messaggio + '\n' +
      'Origine: '   + (data.origine || data.prodotto || '') + '\n' +
      'URL: '       + (data.url || '');

    MailApp.sendEmail(NOTIFY_TO, 'Nuovo contatto Abra: ' + nome, corpo);

    return ok();

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function ok()      { return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON); }
function err(code) { return ContentService.createTextOutput(JSON.stringify({ ok: false, error: code })).setMimeType(ContentService.MimeType.JSON); }

function doGet() {
  return ContentService.createTextOutput('Abra Robotics — endpoint form attivo.');
}
