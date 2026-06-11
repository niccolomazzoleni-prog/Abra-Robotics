var SHEET_ID   = '1XpXE3odenRl9nlkR3Te_-RjNlOA-5PINxpI14uBdvnY';
var SHEET_NAME = 'Contatti';
var NOTIFY_TO  = 'gio@abrarobotics.com,niccolomazzoleni@gmail.com';

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try {
        data = JSON.parse(e.postData.contents);
      } catch (err) {
        data = e.parameter || {};
      }
    } else {
      data = (e && e.parameter) || {};
    }

    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

    if (sh.getLastRow() === 0) {
      sh.appendRow(['Data','Nome','Azienda','Ruolo','Email','Telefono','Messaggio','Origine','Pagina','URL']);
    }

    sh.appendRow([
      new Date(),
      data.nome      || '',
      data.azienda   || '',
      data.ruolo     || '',
      data.email     || '',
      data.telefono  || '',
      data.messaggio || '',
      data.origine   || data.prodotto || '',
      data.pagina    || '',
      data.url       || ''
    ]);

    var corpo =
      'Nome: '      + (data.nome      || '') + '\n' +
      'Azienda: '   + (data.azienda   || '') + '\n' +
      'Ruolo: '     + (data.ruolo     || '') + '\n' +
      'Email: '     + (data.email     || '') + '\n' +
      'Telefono: '  + (data.telefono  || '') + '\n' +
      'Messaggio: ' + (data.messaggio || '') + '\n' +
      'Origine: '   + (data.origine   || data.prodotto || '') + '\n' +
      'URL: '       + (data.url       || '');

    MailApp.sendEmail(NOTIFY_TO, 'Nuovo contatto Abra: ' + (data.nome || '---'), corpo);

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
