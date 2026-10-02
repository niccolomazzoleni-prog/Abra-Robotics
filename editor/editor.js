// Editor blog di abrarobotics.com: legge e salva gli articoli direttamente
// nel repository GitHub del sito (commit su main, poi GitHub Pages pubblica).
// Del file HTML si sostituiscono SOLO: <title>, meta description, h1,
// contenuto di .article-content e i JSON-LD (headline, description,
// dateModified, FAQPage). Il resto del file resta byte per byte com'era.
(function () {
  'use strict';
  const REPO = 'niccolomazzoleni-prog/Abra-Robotics';
  const BRANCH = 'main';
  const API = 'https://api.github.com';
  const KEY = 'abra-editor-token';
  const $ = (id) => document.getElementById(id);

  let token = '';
  let current = null; // { path, sha, text }
  let dirty = false;

  // ---------- utilità ----------
  function msg(text, isError) {
    const el = $('ed-msg');
    el.hidden = !text;
    el.textContent = text || '';
    el.classList.toggle('is-error', !!isError);
    if (text) el.scrollIntoView({ block: 'nearest' });
  }
  function show(id) {
    ['ed-login', 'ed-list', 'ed-edit'].forEach((s) => { $(s).hidden = s !== id; });
  }
  function b64decode(b64) {
    const bin = atob(b64.replace(/\n/g, ''));
    const bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
    return new TextDecoder('utf-8').decode(bytes);
  }
  function b64encode(text) {
    const bytes = new TextEncoder().encode(text);
    let bin = '';
    for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  }
  function escAttr(s) {
    return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function escText(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function today() {
    const d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }

  async function gh(path, options = {}) {
    const r = await fetch(API + path, {
      ...options,
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: 'Bearer ' + token,
        'X-GitHub-Api-Version': '2022-11-28',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      },
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) {
      const e = new Error(data.message || 'Errore GitHub ' + r.status);
      e.status = r.status;
      throw e;
    }
    return data;
  }

  // ---------- accesso ----------
  function loadToken() {
    try { return sessionStorage.getItem(KEY) || localStorage.getItem(KEY) || ''; } catch (e) { return ''; }
  }
  function saveToken(t, remember) {
    try {
      sessionStorage.setItem(KEY, t);
      if (remember) localStorage.setItem(KEY, t); else localStorage.removeItem(KEY);
      localStorage.setItem('abra-editor', '1'); // mostra "Modifica articolo" sugli articoli
    } catch (e) {}
  }
  function logout() {
    try { sessionStorage.removeItem(KEY); localStorage.removeItem(KEY); localStorage.removeItem('abra-editor'); } catch (e) {}
    token = '';
    $('ed-user').textContent = '';
    $('ed-logout').hidden = true;
    show('ed-login');
  }
  async function login(t, remember) {
    token = t.trim();
    const [user, repo] = await Promise.all([gh('/user'), gh('/repos/' + REPO)]);
    if (!repo.permissions || !repo.permissions.push)
      throw new Error('Questo account GitHub non ha i permessi di scrittura sul sito.');
    saveToken(token, remember);
    $('ed-user').textContent = user.login;
    $('ed-logout').hidden = false;
  }

  // ---------- elenco ----------
  async function openList() {
    show('ed-list');
    msg('');
    const [files, blog] = await Promise.all([
      gh('/repos/' + REPO + '/contents/blog?ref=' + BRANCH),
      gh('/repos/' + REPO + '/contents/blog.html?ref=' + BRANCH).then((f) => b64decode(f.content)).catch(() => ''),
    ]);
    const titles = {};
    blog.replace(/<a class="blog-card" href="blog\/([^"]+)"[\s\S]*?<h2 class="blog-card-title">([\s\S]*?)<\/h2>/g, (m, f, t) => { titles[f] = t.replace(/<[^>]+>/g, '').trim(); });
    const items = files
      .filter((f) => f.type === 'file' && f.name.endsWith('.html'))
      .map((f) => ({ path: f.path, name: f.name, title: titles[f.name] || f.name.replace(/\.html$/, '').replace(/-/g, ' ') }));
    const ul = $('ed-articles');
    ul.replaceChildren(...items.map((it) => {
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button';
      b.dataset.search = (it.title + ' ' + it.name).toLowerCase();
      b.innerHTML = '<span class="ed-a-title"></span><span class="ed-a-file"></span>';
      b.firstChild.textContent = it.title;
      b.lastChild.textContent = it.name;
      b.onclick = () => openFile(it.path).catch((e) => msg(e.message, true));
      li.appendChild(b);
      return li;
    }));
  }

  // ---------- apertura ----------
  function contentBounds(text) {
    // Trova il <div class="article-content"> e il suo </div> di chiusura.
    const open = text.search(/<div class="article-content"[^>]*>/i);
    if (open < 0) return null;
    const start = text.indexOf('>', open) + 1;
    const re = /<div\b[^>]*>|<\/div>/gi;
    re.lastIndex = start;
    let depth = 1, m;
    while ((m = re.exec(text))) {
      depth += m[0][1] === '/' ? -1 : 1;
      if (depth === 0) return { start, end: m.index };
    }
    return null;
  }
  function grab(text, re) { const m = text.match(re); return m ? m[1] : ''; }
  function decodeEntities(s) { const t = document.createElement('textarea'); t.innerHTML = s; return t.value; }

  async function openFile(path) {
    msg('');
    const f = await gh('/repos/' + REPO + '/contents/' + encodeURI(path) + '?ref=' + BRANCH);
    const text = b64decode(f.content);
    const b = contentBounds(text);
    if (!b) throw new Error('Questo file non ha la struttura di un articolo (manca .article-content).');
    current = { path, sha: f.sha, text };
    $('ed-file').textContent = path;
    $('ed-view').href = '../' + path;
    $('ed-title').value = decodeEntities(grab(text, /<title>([\s\S]*?)<\/title>/i));
    $('ed-desc').value = decodeEntities(grab(text, /<meta name="description" content="([^"]*)"/i));
    $('ed-h1').innerHTML = grab(text, /<h1[^>]*>([\s\S]*?)<\/h1>/i);
    // Base per link e immagini relativi come nella pagina vera (/blog/).
    $('ed-content').innerHTML = text.slice(b.start, b.end).replace(/(src|poster)="(?!https?:|\/|data:)([^"]+)"/g, '$1="../blog/$2"');
    $('ed-content').querySelectorAll('script').forEach((s) => s.remove());
    setDirty(false);
    updateCounts();
    show('ed-edit');
    history.replaceState(null, '', '?file=' + encodeURIComponent(path));
    window.scrollTo(0, 0);
  }

  // ---------- pulizia del contenuto modificato ----------
  function cleanContent(root) {
    const node = root.cloneNode(true);
    node.querySelectorAll('[style]').forEach((el) => el.removeAttribute('style'));
    node.querySelectorAll('[contenteditable],[spellcheck]').forEach((el) => { el.removeAttribute('contenteditable'); el.removeAttribute('spellcheck'); });
    node.querySelectorAll('font, span:not([class])').forEach((el) => el.replaceWith(...el.childNodes));
    node.querySelectorAll('b').forEach((el) => { const s = document.createElement('strong'); s.append(...el.childNodes); el.replaceWith(s); });
    node.querySelectorAll('i').forEach((el) => { const s = document.createElement('em'); s.append(...el.childNodes); el.replaceWith(s); });
    // I browser creano <div> senza classe andando a capo: sono paragrafi.
    node.querySelectorAll('div:not([class])').forEach((el) => { const p = document.createElement('p'); p.append(...el.childNodes); el.replaceWith(p); });
    node.querySelectorAll('p, h2, h3, li').forEach((el) => { if (!el.textContent.trim() && !el.querySelector('img,video,iframe')) el.remove(); });
    node.querySelectorAll('a[href^="http"]').forEach((a) => {
      if (!/^https?:\/\/(www\.)?abrarobotics\.com/.test(a.href)) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
    });
    let html = node.innerHTML.replace(/(src|poster)="\.\.\/blog\/([^"]+)"/g, '$1="$2"');
    html = html.replace(/&nbsp;/g, ' ').replace(/[ \t]+\n/g, '\n');
    return '\n' + html.trim() + '\n';
  }
  function cleanInline(el) {
    const n = el.cloneNode(true);
    n.querySelectorAll('[style]').forEach((x) => x.removeAttribute('style'));
    n.querySelectorAll('font, span:not([class]), div, br').forEach((x) => x.replaceWith(...x.childNodes));
    return n.innerHTML.replace(/&nbsp;/g, ' ').trim();
  }

  // FAQ: h2 "Domande frequenti"/"FAQ" seguito da h3 (domanda) + risposta.
  function extractFaq(root) {
    const h2 = [...root.querySelectorAll('h2')].find((h) => /domande frequenti|faq/i.test(h.textContent));
    if (!h2) return null;
    const out = [];
    let el = h2.nextElementSibling, q = null, a = [];
    const flush = () => { if (q && a.length) out.push({ q, a: a.join(' ').replace(/\s+/g, ' ').trim() }); };
    const visit = (x) => {
      if (x.tagName === 'H3') { flush(); q = x.textContent.trim(); a = []; }
      else if (q) a.push(x.textContent.trim());
    };
    while (el && el.tagName !== 'H2') {
      if (el.querySelector && el.querySelector('h3') && el.tagName !== 'H3') [...el.children].forEach(visit);
      else visit(el);
      el = el.nextElementSibling;
    }
    flush();
    return out.length ? out : null;
  }

  function updateJsonLd(text, { title, desc, h1Text, faq }) {
    return text.replace(/(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/gi, (all, a, body, c) => {
      let data;
      try { data = JSON.parse(body); } catch (e) { return all; }
      const fix = (d) => {
        if (d['@type'] === 'Article' || d['@type'] === 'BlogPosting') {
          d.headline = h1Text || title;
          d.description = desc;
          d.dateModified = today();
        }
        if (d['@type'] === 'FAQPage' && faq) {
          d.mainEntity = faq.map((x) => ({ '@type': 'Question', name: x.q, acceptedAnswer: { '@type': 'Answer', text: x.a } }));
        }
        return d;
      };
      data = Array.isArray(data) ? data.map(fix) : fix(data);
      const indent = (body.match(/\n(\s*)"@context"/) || [, '  '])[1];
      return a + '\n' + JSON.stringify(data, null, 2).replace(/^/gm, indent.replace(/ {2}$/, '')) + '\n  ' + c;
    });
  }

  // ---------- salvataggio ----------
  async function save() {
    if (!current) return;
    const title = $('ed-title').value.trim();
    const desc = $('ed-desc').value.trim();
    if (!title || !desc) return msg('Titolo e descrizione non possono essere vuoti.', true);
    const content = $('ed-content');
    const h1Html = cleanInline($('ed-h1'));
    const h1Text = $('ed-h1').textContent.trim();
    if (!h1Text) return msg('Il titolo dell\'articolo (h1) non può essere vuoto.', true);
    let text = current.text;
    const b = contentBounds(text);
    text = text.slice(0, b.start) + cleanContent(content) + text.slice(b.end);
    text = text.replace(/<title>[\s\S]*?<\/title>/i, '<title>' + escText(title) + '</title>');
    text = text.replace(/(<meta name="description" content=")[^"]*(")/i, '$1' + escAttr(desc) + '$2');
    text = text.replace(/(<meta property="og:title" content=")[^"]*(")/i, '$1' + escAttr(title) + '$2');
    text = text.replace(/(<meta property="og:description" content=")[^"]*(")/i, '$1' + escAttr(desc) + '$2');
    text = text.replace(/(<h1[^>]*>)[\s\S]*?(<\/h1>)/i, '$1' + h1Html + '$2');
    text = updateJsonLd(text, { title, desc, h1Text, faq: extractFaq(content) });
    if (text === current.text) { setDirty(false); return msg('Nessuna modifica da salvare.'); }

    $('ed-save').disabled = true;
    $('ed-save').textContent = 'Salvataggio...';
    try {
      const r = await gh('/repos/' + REPO + '/contents/' + encodeURI(current.path), {
        method: 'PUT',
        body: JSON.stringify({
          message: 'blog: modifica ' + current.path.replace(/^blog\//, '') + ' (editor)',
          content: b64encode(text),
          sha: current.sha,
          branch: BRANCH,
        }),
      });
      current = { ...current, sha: r.content.sha, text };
      setDirty(false);
      msg('Salvato. La pagina online si aggiorna entro 1-2 minuti.');
    } catch (e) {
      msg(e.status === 409
        ? 'Qualcun altro ha modificato questo articolo nel frattempo. Copia le tue modifiche, riapri l\'articolo e riapplicale.'
        : 'Salvataggio non riuscito: ' + e.message, true);
      $('ed-save').disabled = false;
    } finally {
      $('ed-save').textContent = 'Salva e pubblica';
    }
  }

  // ---------- interfaccia ----------
  function setDirty(v) { dirty = v; $('ed-save').disabled = !v; }
  function updateCounts() {
    const t = $('ed-title').value.length, d = $('ed-desc').value.length;
    $('ed-title-count').textContent = t + '/60';
    $('ed-title-count').classList.toggle('is-over', t > 60);
    $('ed-desc-count').textContent = d + '/155';
    $('ed-desc-count').classList.toggle('is-over', d > 155);
  }

  document.querySelectorAll('.ed-toolbar button').forEach((btn) => {
    btn.addEventListener('mousedown', (e) => e.preventDefault()); // non perdere la selezione
    btn.addEventListener('click', () => {
      const cmd = btn.dataset.cmd;
      if (cmd === 'link') {
        const url = prompt('Indirizzo del link (es. https://... oppure ../umanoidi.html):');
        if (url) document.execCommand('createLink', false, url.trim());
      } else {
        document.execCommand(cmd, false, btn.dataset.val || null);
      }
      setDirty(true);
    });
  });
  ['ed-content', 'ed-h1'].forEach((id) => $(id).addEventListener('input', () => setDirty(true)));
  ['ed-title', 'ed-desc'].forEach((id) => $(id).addEventListener('input', () => { setDirty(true); updateCounts(); }));
  // Incolla solo testo: niente stili copiati da Word o da altri siti.
  ['ed-content', 'ed-h1'].forEach((id) => $(id).addEventListener('paste', (e) => {
    e.preventDefault();
    document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain'));
  }));
  $('ed-h1').addEventListener('keydown', (e) => { if (e.key === 'Enter') e.preventDefault(); });
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's' && !$('ed-edit').hidden) { e.preventDefault(); if (dirty) save(); }
  });
  window.addEventListener('beforeunload', (e) => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
  $('ed-save').onclick = save;
  $('ed-back').onclick = () => {
    if (dirty && !confirm('Ci sono modifiche non salvate. Tornare comunque all\'elenco?')) return;
    setDirty(false);
    history.replaceState(null, '', location.pathname);
    openList().catch((e) => msg(e.message, true));
  };
  $('ed-filter').addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    document.querySelectorAll('#ed-articles button').forEach((b) => { b.parentNode.hidden = !b.dataset.search.includes(q); });
  });
  $('ed-logout').onclick = logout;
  $('ed-login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
      await login($('ed-token').value, $('ed-remember').checked);
      $('ed-token').value = '';
      await start();
    } catch (err) {
      token = '';
      msg(err.status === 401 ? 'Token non valido o scaduto.' : err.message, true);
    }
  });

  async function start() {
    const file = new URLSearchParams(location.search).get('file');
    if (file && /^blog\/[a-z0-9-]+\.html$/.test(file)) await openFile(file);
    else await openList();
  }

  (async function init() {
    token = loadToken();
    if (!token) return show('ed-login');
    try {
      await login(token, !!localStorage.getItem(KEY));
      await start();
    } catch (e) {
      logout();
      msg(e.status === 401 ? 'Accesso scaduto: inserisci di nuovo il token.' : e.message, true);
    }
  })();
})();
