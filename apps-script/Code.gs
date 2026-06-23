var SHEET_ID   = '1XpXE3odenRl9nlkR3Te_-RjNlOA-5PINxpI14uBdvnY';
var SHEET_NAME = 'Contatti';
var ANALYTICS_SHEET = 'Analytics';
var NOTIFY_TO  = 'gio@abrarobotics.com,niccolomazzoleni@gmail.com';
/** Cambia prima di ridistribuire; la stessa chiave va incollata in admin/statistiche.html */
var STATS_KEY  = 'abra-stats-2026';

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

    if (data.type === 'pageview') {
      return handlePageview(data);
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

    return jsonOut({ ok: true });

  } catch (err) {
    return jsonOut({ ok: false, error: String(err) });
  }
}

function handlePageview(data) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(ANALYTICS_SHEET) || ss.insertSheet(ANALYTICS_SHEET);
  if (sh.getLastRow() === 0) {
    sh.appendRow(['Data','Path','Referrer','UTM Source','UTM Medium','UTM Campaign','Lang','Mobile']);
  }
  sh.appendRow([
    new Date(),
    data.path || '',
    data.referrer || '',
    data.utm_source || '',
    data.utm_medium || '',
    data.utm_campaign || '',
    data.lang || '',
    data.mobile ? 'sì' : 'no'
  ]);
  return jsonOut({ ok: true });
}

function doGet(e) {
  e = e || { parameter: {} };
  if (e.parameter.action === 'stats') {
    if (e.parameter.key !== STATS_KEY) {
      return jsonOut({ ok: false, error: 'Chiave non valida' });
    }
    var days = parseInt(e.parameter.days, 10) || 30;
    return jsonOut(buildStats(days));
  }
  return ContentService.createTextOutput('Abra Robotics — endpoint form attivo.');
}

function buildStats(days) {
  var cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);

  var ss = SpreadsheetApp.openById(SHEET_ID);
  var analytics = aggregateSheet(ss.getSheetByName(ANALYTICS_SHEET), cutoff, 1, 2);
  var contacts = ss.getSheetByName(SHEET_NAME);
  var leads = 0;
  if (contacts && contacts.getLastRow() > 1) {
    var rows = contacts.getDataRange().getValues();
    for (var i = 1; i < rows.length; i++) {
      var d = rows[i][0];
      if (d instanceof Date && d >= cutoff) leads++;
    }
  }

  return {
    ok: true,
    days: days,
    totals: {
      pageviews: analytics.total,
      sessions: analytics.sessions,
      leads: leads
    },
    referrers: analytics.referrers,
    pages: analytics.pages,
    sources: analytics.sources
  };
}

function aggregateSheet(sh, cutoff, dateCol, valueCol) {
  var referrers = {};
  var pages = {};
  var sources = {};
  var sessions = {};
  var total = 0;

  if (!sh || sh.getLastRow() < 2) {
    return { total: 0, sessions: 0, referrers: [], pages: [], sources: [] };
  }

  var rows = sh.getDataRange().getValues();
  for (var i = 1; i < rows.length; i++) {
    var d = rows[i][dateCol - 1];
    if (!(d instanceof Date) || d < cutoff) continue;
    total++;

    var path = String(rows[i][valueCol - 1] || '/');
    var ref = String(rows[i][valueCol] || '');
    var src = String(rows[i][valueCol + 1] || '');

    pages[path] = (pages[path] || 0) + 1;

    var refKey = ref ? normalizeReferrer(ref) : '(direct)';
    referrers[refKey] = (referrers[refKey] || 0) + 1;

    if (src) sources[src] = (sources[src] || 0) + 1;

    var day = Utilities.formatDate(d, Session.getScriptTimeZone(), 'yyyy-MM-dd');
    var sessId = day + '|' + refKey;
    sessions[sessId] = true;
  }

  function top(obj, limit) {
    return Object.keys(obj)
      .map(function (k) { return { key: k, count: obj[k] }; })
      .sort(function (a, b) { return b.count - a.count; })
      .slice(0, limit)
      .map(function (x) { return x; });
  }

  return {
    total: total,
    sessions: Object.keys(sessions).length,
    referrers: top(referrers, 12).map(function (x) { return { referrer: x.key, count: x.count }; }),
    pages: top(pages, 12).map(function (x) { return { path: x.key, count: x.count }; }),
    sources: top(sources, 12).map(function (x) { return { source: x.key, count: x.count }; })
  };
}

function normalizeReferrer(ref) {
  try {
    var u = ref.replace(/^https?:\/\//, '').split('/')[0];
    return u || '(direct)';
  } catch (e) {
    return ref || '(direct)';
  }
}

function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
