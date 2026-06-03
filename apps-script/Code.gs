/**
 * Abra Robotics — endpoint UNICO dei form del sito.
 * Riceve i POST da tutti i form (contatti + box "Richiedi informazioni" delle schede),
 * scrive una riga nel Google Sheet e invia un'email di notifica a OGNI nuovo contatto.
 *
 * Deploy: vedi README.md in questa cartella.
 */

// ── CONFIG ──────────────────────────────────────────────────────────────
var SHEET_ID    = '1nXl0QyElz1znYHiDb8xJ_bd7NYqfuCoLB3URLfNdcAc';  // Foglio "Abra Robotics — Contatti sito" (gia creato)
var SHEET_NAME  = 'Contatti';               // nome del tab
var NOTIFY_TO   = 'gio@abrarobotics.com';   // dove ricevere la notifica di nuovo contatto
// ────────────────────────────────────────────────────────────────────────

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try { data = JSON.parse(e.postData.contents); }
      catch (err) { data = e.parameter || {}; }
    } else {
      data = (e && e.parameter) || {};
    }

    var ss = SHEET_ID ? SpreadsheetApp.openById(SHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sh.getLastRow() === 0) {
      sh.appendRow(['Data', 'Nome', 'Azienda', 'Ruolo', 'Email', 'Telefono',
                    'Messaggio', 'Origine', 'Pagina', 'URL']);
    }
    sh.appendRow([
      new Date(),
      data.nome || '', data.azienda || '', data.ruolo || '',
      data.email || '', data.telefono || '',
      data.messaggio || '', data.origine || data.prodotto || '',
      data.pagina || '', data.url || ''
    ]);

    // ── AUTOMAZIONE: notifica email a ogni nuovo contatto ──
    var subject = 'Nuovo contatto sito Abra: ' + (data.nome || 'senza nome');
    var body =
      'Nuovo contatto dal sito Abra Robotics\n\n' +
      'Nome:      ' + (data.nome || '') + '\n' +
      'Azienda:   ' + (data.azienda || '') + '\n' +
      'Ruolo:     ' + (data.ruolo || '') + '\n' +
      'Email:     ' + (data.email || '') + '\n' +
      'Telefono:  ' + (data.telefono || '') + '\n' +
      'Messaggio: ' + (data.messaggio || '') + '\n\n' +
      'Origine:   ' + (data.origine || data.prodotto || '') + '\n' +
      'Pagina:    ' + (data.pagina || '') + '\n' +
      'URL:       ' + (data.url || '');
    MailApp.sendEmail(NOTIFY_TO, subject, body);
    // Estendibile: webhook Slack/Make/Zapier, aggiunta a CRM, autorisposta al cliente, ecc.

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('Abra Robotics — endpoint form attivo.');
}
