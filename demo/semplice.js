/* Vista semplice delle demo (?vista=semplice), usata dalle card del sito.
   La scena 3D riempie la pagina e sopra restano solo un titolo, una frase, due o tre pulsanti
   e una riga di stato in italiano semplice. Testi e azioni stanno in window.DEMO_SEMPLICE (in ogni
   pagina); il CSS html.semplice di ogni pagina nasconde i pannelli da esperti.
   "Vista completa" toglie il filtro.
   Prima che parta l'app misura i byte scaricati (fetch e XMLHttpRequest): da lì la barra di
   caricamento a tutta pagina e il messaggio {type:'abra-demo', progress, ready} per demo-modal.js.
   Con &rec=1 (registrazioni per le card) spariscono anche titolo, pulsanti e caricamento.
   Va caricato nel <head> dopo window.DEMO_SEMPLICE e prima degli script dell'app. */
(function () {
  var q = new URLSearchParams(location.search);
  if (q.get('vista') !== 'semplice') return;
  var rec = q.get('rec') === '1';
  var incorniciata = window.parent !== window;   // dentro il riquadro di demo-modal.js, che mostra il suo caricamento
  var root = document.documentElement;
  var qui = (document.currentScript && document.currentScript.src) || location.href;
  var cfg = window.DEMO_SEMPLICE || {};
  var $ = function (s) { return document.querySelector(s); };
  root.classList.add('semplice');
  if (rec) root.classList.add('rec');

  // stile del sito
  var font = document.createElement('link');
  font.rel = 'stylesheet';
  font.href = new URL('../fonts/geist.css', qui).href;   // gli stessi font della home
  document.head.appendChild(font);

  var CALL = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF';
  var SANS = "'Geist',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif";
  var css = document.createElement('style');
  css.textContent = [
    // caricamento a tutta pagina
    '.vs-load{position:fixed;inset:0;z-index:2000;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:24px;background:#000;color:#f5f5f5;text-align:center;font:300 15px/1.5 ' + SANS + ';-webkit-font-smoothing:antialiased;transition:opacity .5s ease,visibility .5s}',
    '.vs-load.vs-via{opacity:0;visibility:hidden;pointer-events:none}',
    '.vs-load img{display:block;height:22px;width:auto;margin-bottom:10px;opacity:.92}',
    '.vs-lt{font-size:24px;font-weight:400;letter-spacing:-.025em;line-height:1.15;color:#fff}',
    '.vs-bar{position:relative;width:min(320px,72vw);height:6px;overflow:hidden;border-radius:999px;background:#1c1c1c}',
    '.vs-bar i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:inherit;background:linear-gradient(90deg,#2bc4a8,#2f5bff);transition:width .3s ease}',
    '.vs-bar.vs-ind i{width:36%;transition:none;animation:vsind 1.25s ease-in-out infinite}',
    '.vs-bar.vs-prep i{animation:vsprep 1s ease-in-out infinite alternate}',
    '.vs-pct{min-height:24px;font-size:16px;line-height:1.5;color:#c4c4c4}',
    '@keyframes vsind{0%{transform:translateX(-100%)}100%{transform:translateX(280%)}}',
    '@keyframes vsprep{from{opacity:.55}to{opacity:1}}',
    // scheda comandi: sta accanto alla scena (colonna a sinistra) o sotto (telefono e tablet in piedi),
    // mai sopra la scena. Le due fasce nere (::before e ::after) coprono lo spazio che la scena lascia libero.
    '.vs-ui{position:fixed;inset:0;z-index:100;pointer-events:none;color:#f5f5f5;font:300 16px/1.5 ' + SANS + ';-webkit-font-smoothing:antialiased}',
    '.vs-ui *{box-sizing:border-box}',
    '.vs-ui::before{content:"";position:absolute;left:0;top:0;bottom:0;width:var(--vs-l,0px);background:#000;pointer-events:auto}',
    '.vs-ui::after{content:"";position:absolute;left:0;right:0;bottom:0;height:var(--vs-b,0px);background:#000;pointer-events:auto}',
    '.vs-card{position:absolute;left:12px;top:12px;z-index:1;display:flex;flex-direction:column;width:clamp(290px,25vw,360px);max-height:calc(100% - 24px);overflow:hidden;pointer-events:auto;border-radius:20px;border:1px solid #2a2a2a;background:#0a0a0a}',
    '.vs-corpo{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:22px 20px 8px}',
    '.vs-fondo{flex:none;padding:12px 20px 16px;border-top:1px solid #242424;background:#0a0a0a}',
    '.vs-cta{display:grid;grid-template-columns:1fr;gap:8px}',
    '.vs-nota{margin:10px 0 0;font-size:15px;line-height:1.4;color:#b4b4b4}',
    '.vs-titolo{display:block;width:100%;margin:0 0 12px;padding:0;border:0;background:none;color:inherit;font:inherit;text-align:left;cursor:default}',
    '.vs-t{display:block;font-size:26px;font-weight:400;letter-spacing:-.025em;line-height:1.15;color:#fff}',
    '.vs-frase{margin:0 0 14px;font-size:16px;line-height:1.5;color:#e6e6e6}',
    '.vs-cit{margin:0 0 14px;padding-left:12px;border-left:2px solid #2bc4a8;font-size:15px;line-height:1.45;color:#c4c4c4}',
    '.vs-azioni{display:grid;grid-template-columns:1fr;gap:8px}',
    '.vs-btn{display:flex;align-items:center;justify-content:center;gap:8px;min-height:52px;padding:10px 18px;border-radius:999px;border:1px solid rgba(255,255,255,.28);background:transparent;color:#fff;font:500 16px/1.25 ' + SANS + ';letter-spacing:0;text-transform:none;text-align:center;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:background .2s,color .2s,border-color .2s,transform .1s}',
    '.vs-btn:hover{border-color:#fff}',
    '.vs-btn:active{transform:scale(.985)}',
    '.vs-btn.vs-on{border-color:#2bc4a8;background:rgba(43,196,168,.14)}',
    '.vs-btn.vs-on::before{content:"";flex:none;width:8px;height:8px;border-radius:50%;background:#2bc4a8}',
    '.vs-btn.vs-next{background:#fff;color:#000;border-color:#fff}',
    '.vs-btn.vs-next:hover{background:#d9d9d9}',
    '.vs-btn[aria-disabled=true]{opacity:.6;cursor:default}',
    'a.vs-btn{text-decoration:none}',
    '.vs-btn.vs-prim{background:#2bc4a8;color:#00110d;border-color:#2bc4a8}',
    '.vs-btn.vs-prim:hover{background:#5fd9c2;border-color:#5fd9c2}',
    '.vs-btn svg{flex:none;width:20px;height:20px}',
    '.vs-btn:focus-visible,.vs-full:focus-visible,.vs-titolo:focus-visible{outline:2px solid #2f5bff;outline-offset:2px}',
    '.vs-stato{display:flex;align-items:flex-start;gap:10px;margin-top:14px;padding-top:14px;border-top:1px solid #242424;font-size:16px;line-height:1.45;color:#f5f5f5}',
    '.vs-stato i{flex:none;width:8px;height:8px;margin-top:.55em;border-radius:50%;background:#2bc4a8;box-shadow:0 0 10px rgba(43,196,168,.7);animation:vsp 1.6s ease-in-out infinite}',
    '.vs-stato span{display:block;min-height:2.9em}',   // due righe sempre: la scheda non cambia altezza a ogni frase
    '.vs-stato.vs-invito i{background:#ff7a59;box-shadow:0 0 10px rgba(255,122,89,.7)}',
    '@keyframes vsp{50%{opacity:.35}}',
    '.vs-pie{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;column-gap:12px;margin-top:6px;font-size:15px;color:#b4b4b4}',
    '.vs-full{display:inline-flex;align-items:center;min-height:44px;color:#fff;text-decoration:underline;text-decoration-color:#6b6b6b;text-underline-offset:3px}',
    '.vs-full:hover{text-decoration-color:#fff}',
    // risultato della missione: foto + messaggio, al posto dei comandi (si chiude con «Torna ai comandi»)
    '.vs-extra{display:none}',
    '.vs-ris .vs-extra{display:block}',
    '.vs-ris .vs-frase,.vs-ris .vs-cit,.vs-ris .vs-azioni,.vs-ris .vs-pie{display:none}',
    '.vs-ris .vs-titolo{display:none}',
    '.vs-ris .vs-corpo{padding-top:14px}',
    '.vs-ris .vs-stato{margin-top:4px;padding-top:10px}',
    '.vs-foto{display:flex;align-items:center;margin:0 0 10px;overflow:hidden;border:1px solid #2a2a2a;border-radius:14px;background:#000}',
    '.vs-foto>div{flex:0 0 52%}',
    '.vs-foto svg{display:block;width:100%;height:auto}',
    '.vs-foto figcaption{flex:1;padding:8px 10px;font-size:15px;line-height:1.4;color:#f5f5f5}',
    '.vs-foto figcaption b{display:block;font-weight:500;color:#fff}',
    '.vs-chat{margin:0 0 12px;overflow:hidden;border:1px solid #1d3a30;border-radius:16px;background:#0b141a}',
    '.vs-ch-h{display:flex;align-items:center;gap:10px;padding:10px 12px;background:#10201c;border-bottom:1px solid #1d3a30}',
    '.vs-av{display:grid;place-items:center;flex:none;width:36px;height:36px;border-radius:50%;background:#25d366;color:#04210f;font-weight:600;font-size:16px}',
    '.vs-ch-n{display:block;line-height:1.25;font-size:15px}',
    '.vs-ch-n b{display:block;font-weight:500;color:#fff}',
    '.vs-ch-n i{font-style:normal;color:#25d366}',
    '.vs-ch-b{display:flex;flex-direction:column;gap:8px;padding:12px}',
    '.vs-msg{align-self:flex-start;max-width:100%;padding:10px 12px 8px;border-radius:4px 14px 14px 14px;background:#202c33;color:#e9edef;font-size:15px;line-height:1.45;animation:vsin .3s ease}',
    '.vs-msg svg{display:inline-block;width:18px;height:18px;margin:0 6px -3px 0}',
    '.vs-ora{display:block;margin-top:4px;text-align:right;font-size:15px;line-height:1.2;color:#8696a0}',
    '.vs-scrive{display:flex;align-self:flex-start;gap:5px;padding:13px 14px;border-radius:4px 14px 14px 14px;background:#202c33}',
    '.vs-scrive i{width:8px;height:8px;border-radius:50%;background:#8696a0;animation:vsd 1s ease-in-out infinite}',
    '.vs-scrive i:nth-child(2){animation-delay:.15s}.vs-scrive i:nth-child(3){animation-delay:.3s}',
    '.vs-chat .vs-btn{margin:0 12px 12px;width:calc(100% - 24px)}',
    '.vs-btn.vs-wa{background:#25d366;color:#04210f;border-color:#25d366}',
    '.vs-btn.vs-wa:hover{background:#4ee184;border-color:#4ee184}',
    '.vs-flash{position:fixed;top:0;right:0;bottom:var(--vs-b,0px);left:var(--vs-l,0px);z-index:90;background:#fff;opacity:0;pointer-events:none}',
    '.vs-flash.vs-sc{animation:vsf .55s ease-out}',
    '@keyframes vsin{from{opacity:0;transform:translateY(6px)}}',
    '@keyframes vsd{50%{opacity:.3;transform:translateY(-3px)}}',
    '@keyframes vsf{0%{opacity:.9}100%{opacity:0}}',
    // computer con poca altezza (es. 1280x720): comandi e risultato devono stare nella scheda senza scorrere
    '@media (min-width:901px) and (max-height:760px){.vs-cta{grid-template-columns:1fr 1fr}.vs-fondo .vs-btn{padding:8px 8px;font-size:15px}.vs-fondo{padding:8px 14px 10px}.vs-nota{margin-top:6px;line-height:1.3}.vs-ris .vs-corpo{padding-top:10px}.vs-ch-h{padding:6px 10px}.vs-ch-b{padding:8px}.vs-msg{padding:8px 10px 6px}.vs-foto,.vs-chat{margin-bottom:8px}.vs-chat .vs-btn{margin:0 10px 10px;width:calc(100% - 20px)}.vs-ris .vs-stato{padding-top:8px}.vs-ris .vs-stato span{min-height:0}}',
    // schermi bassi (telefono girato): colonna compatta, senza spiegazione
    '@media (max-height:520px){.vs-corpo{padding:14px 16px 6px}.vs-fondo{padding:8px 16px 10px}.vs-t{font-size:20px}.vs-frase,.vs-cit,.vs-nota{display:none}.vs-btn{min-height:48px;padding:8px 14px}.vs-stato{margin-top:10px;padding-top:10px}}',
    // telefono e tablet in piedi: barra in basso a tutta larghezza, la scena sta sopra; il titolo apre e chiude la spiegazione
    '@media (max-width:900px) and (min-height:521px){.vs-card{left:0;right:0;top:auto;bottom:0;width:auto;max-height:62vh;border-width:1px 0 0;border-radius:20px 20px 0 0}.vs-corpo{padding:12px 16px 2px}.vs-fondo{padding:8px 16px calc(8px + env(safe-area-inset-bottom,0px))}.vs-cta{grid-template-columns:1fr 1fr}.vs-btn{padding:8px 10px}.vs-titolo{margin-bottom:6px;cursor:pointer}.vs-t{display:flex;align-items:center;justify-content:space-between;font-size:20px;min-height:36px}.vs-t::after{content:"";width:9px;height:9px;margin:0 6px 4px 12px;border:solid #b4b4b4;border-width:0 2px 2px 0;transform:rotate(45deg)}.vs-chiusa .vs-t::after{transform:rotate(-135deg);margin-bottom:-4px}.vs-frase{margin-bottom:10px}.vs-cit{margin-bottom:10px}.vs-chiusa .vs-frase,.vs-chiusa .vs-cit,.vs-chiusa .vs-nota{display:none}.vs-azioni{grid-template-columns:repeat(auto-fit,minmax(160px,1fr))}.vs-stato{margin-top:10px;padding-top:10px}.vs-ris{max-height:74vh}.vs-ris .vs-nota{display:none}.vs-chat{margin-bottom:10px}}',
    '@media (prefers-reduced-motion:reduce){.vs-bar i,.vs-stato i,.vs-btn,.vs-load,.vs-flash,.vs-msg,.vs-scrive i{animation:none!important;transition:none!important}}'
  ].join('\n');
  document.head.appendChild(css);

  // niente video nascosti che scaricano o partono per niente
  var play0 = window.HTMLMediaElement && HTMLMediaElement.prototype.play;
  if (play0) HTMLMediaElement.prototype.play = function () {
    return this.getClientRects().length ? play0.apply(this, arguments) : Promise.resolve();
  };
  if (cfg.rimuovi && window.MutationObserver) {   // elementi che nella vista semplice non servono (es. un video)
    var selRim = cfg.rimuovi.join(',');
    var pulisci = function () {
      [].forEach.call(document.querySelectorAll(selRim), function (e) { e.removeAttribute('src'); e.remove(); });
    };
    var osserva = new MutationObserver(pulisci);
    osserva.observe(root, { childList: true, subtree: true });
    document.addEventListener('DOMContentLoaded', function () { pulisci(); osserva.disconnect(); });
  }

  // byte scaricati
  var richieste = [];   // una per file: {tot: byte attesi (0 se non noti), got: byte arrivati, fine}
  var DA_SEGUIRE = /\.(bin|glb|gltf|json|mp4|webm|png|jpe?g|webp|ktx2|hdr|wasm)(\?|#|$)/i;
  function nuova() { var r = { tot: 0, got: 0, fine: false }; richieste.push(r); return r; }

  var fetch0 = window.fetch;
  if (fetch0) window.fetch = function (input) {
    var url = typeof input === 'string' ? input : (input && input.url) || String(input);
    var p = fetch0.apply(this, arguments);
    if (!DA_SEGUIRE.test(url)) return p;
    var r = nuova();
    return p.then(function (res) {
      var len = +res.headers.get('content-length'), enc = res.headers.get('content-encoding');
      if (len > 0 && (!enc || enc === 'identity')) r.tot = len;   // con la compressione i byte non coincidono: dimensione non nota
      if (!res.body || !res.clone) { r.fine = true; return res; }
      var rd = res.clone().body.getReader();   // si leggono i byte su una copia, l'app riceve la risposta intatta
      (function giro() {
        rd.read().then(function (x) {
          if (x.done) r.fine = true; else { r.got += x.value.length; giro(); }
        }, function () { r.fine = true; });
      })();
      return res;
    }, function (e) { r.fine = true; throw e; });
  };

  var XHR = window.XMLHttpRequest;
  if (XHR) {
    var open0 = XHR.prototype.open;
    XHR.prototype.open = function (metodo, url) {
      if (DA_SEGUIRE.test(String(url))) {
        var r = nuova();
        this.addEventListener('progress', function (e) { r.got = e.loaded; if (e.lengthComputable) r.tot = e.total; });
        this.addEventListener('loadend', function () { r.fine = true; });
      }
      return open0.apply(this, arguments);
    };
  }

  // quanto è stato scaricato: frac 0..1, oppure -1 se qualche file in corso non dichiara la dimensione
  function scaricato() {
    var tot = 0, got = 0, aperte = 0, ignote = false;
    richieste.forEach(function (r) {
      if (!r.fine) { aperte++; if (!r.tot) ignote = true; }
      if (r.tot) { tot += r.tot; got += r.fine ? r.tot : Math.min(r.got, r.tot); }
    });
    return { aperte: aperte, frac: tot && !ignote ? got / tot : -1 };
  }

  // caricamento
  var dopoPronto = [];     // cose da fare quando la scena è pronta (es. chiudere la spiegazione sul telefono)
  var mostrato = 0;        // 0..1, non torna mai indietro
  var pronta = false;
  var inviato = -1;
  var elLoad = null;

  function invia(ready) {
    if (!incorniciata) return;
    var p = Math.round(mostrato * 100) / 100;
    if (!ready && p === inviato) return;
    inviato = p;
    try { parent.postMessage({ type: 'abra-demo', progress: p, ready: !!ready }, '*'); } catch (e) { /* senza finestra madre */ }
  }

  function disegnaCaricamento(d) {
    if (!elLoad) return;
    var bar = elLoad.querySelector('.vs-bar'), txt = elLoad.querySelector('.vs-pct');
    var scarica = d.frac >= 0 && d.aperte > 0;
    bar.classList.toggle('vs-ind', mostrato <= 0);
    bar.classList.toggle('vs-prep', mostrato > 0 && d.aperte === 0 && !pronta);
    bar.firstChild.style.width = mostrato > 0 ? Math.round(mostrato * 100) + '%' : '';
    bar.setAttribute('aria-valuenow', Math.round(mostrato * 100));
    txt.textContent = scarica && mostrato > 0 ? 'Scarico i modelli 3D · ' + Math.round(mostrato * 100) + '%' : 'Preparo la scena';
  }

  function finito() {
    if (pronta) return;
    pronta = true;
    clearInterval(timer);
    mostrato = 1;
    disegnaCaricamento({ aperte: 0, frac: 1 });
    invia(true);
    if (elLoad) {
      var el = elLoad;
      setTimeout(function () { el.classList.add('vs-via'); }, 200);
      setTimeout(function () { el.remove(); }, 900);
    }
    if (cfg.avvio) setTimeout(function () { try { cfg.avvio(rec); } catch (e) { /* la demo funziona anche senza */ } }, cfg.ritardo || 600);
    dopoPronto.forEach(function (f) { f(); });
    window.dispatchEvent(new Event('resize'));
  }

  function dopoDueFrame(fn) {   // la scena ha disegnato almeno un fotogramma
    var fatto = false;
    function vai() { if (!fatto) { fatto = true; fn(); } }
    requestAnimationFrame(function () { requestAnimationFrame(vai); });
    setTimeout(vai, 500);
  }

  var inizio = Date.now(), attesa = false;
  function giro() {
    if (pronta) return;
    var d = scaricato();
    if (d.frac >= 0) mostrato = Math.max(mostrato, 0.92 * d.frac);   // l'ultimo 8% è la scena che si prepara
    disegnaCaricamento(d);
    invia(false);
    var scena = cfg.pronto ? cfg.pronto() : window.__pronto === true;
    if (richieste.length && d.aperte === 0 && scena && !attesa) { attesa = true; dopoDueFrame(finito); }
    if (Date.now() - inizio > 40000) finito();   // sicurezza: la pagina si mostra comunque
  }

  if (!rec && !incorniciata) {   // nel riquadro del sito il caricamento lo mostra demo-modal.js
    elLoad = document.createElement('div');
    elLoad.className = 'vs-load';
    elLoad.innerHTML = '<img alt="Abra Robotics" src="' + new URL('img/abra-logo-horizontal-white.svg', qui).href + '">' +
      '<div class="vs-lt"></div><div class="vs-bar vs-ind" role="progressbar" aria-valuemin="0" aria-valuemax="100"><i></i></div><div class="vs-pct">Preparo la scena</div>';
    elLoad.querySelector('.vs-lt').textContent = cfg.titolo || '';
    root.appendChild(elLoad);   // il body non esiste ancora: il caricamento compare subito
  }
  invia(false);
  var timer = setInterval(giro, 100);

  // titolo, comandi, stato
  function pronto(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  pronto(function () {
    if (rec) return;
    var telefono = window.matchMedia('(max-width:900px) and (min-height:521px)');   // scheda sotto la scena
    var ui = document.createElement('div');
    ui.className = 'vs-ui';
    ui.innerHTML =
      '<section class="vs-card" aria-label="Comandi della demo"><div class="vs-corpo">' +
      '<button type="button" class="vs-titolo"><span class="vs-t" role="heading" aria-level="1"></span></button>' +
      '<p class="vs-frase"></p><p class="vs-cit" hidden></p><div class="vs-azioni"></div>' +
      '<div class="vs-extra"><div class="vs-ex-foto"></div><div class="vs-ex-chat"></div><button type="button" class="vs-btn vs-nuova">Torna ai comandi</button></div>' +
      '<div class="vs-stato" role="status" aria-live="polite"><i></i><span></span></div>' +
      '<div class="vs-pie"><span>Trascina per girare la scena</span><a class="vs-full">Vista completa</a></div></div>' +
      '<div class="vs-fondo"><div class="vs-cta">' +
      '<a class="vs-btn" href="../../index.html" target="_top" data-cta="home">Torna alla home</a>' +
      '<a class="vs-btn vs-prim" href="' + CALL + '" target="_blank" rel="noopener" data-cta="call">Prenota una call</a></div>' +
      '<p class="vs-nota">Simulatore semplificato per girare leggero nel tuo browser. I robot veri li configuriamo sul tuo processo.</p></div></section>' +
      '<div class="vs-flash" aria-hidden="true"></div>';
    ui.querySelector('.vs-t').textContent = cfg.titolo || '';
    ui.querySelector('.vs-frase').textContent = cfg.frase || '';
    var completa = new URL(location.href);
    completa.searchParams.delete('vista');
    completa.searchParams.delete('rec');
    ui.querySelector('.vs-full').href = completa.pathname + completa.search + completa.hash;

    var card = ui.querySelector('.vs-card'), titolo = ui.querySelector('.vs-titolo');
    var azioni = ui.querySelector('.vs-azioni'), bottoni = [];
    (cfg.bottoni || []).forEach(function (def) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'vs-btn';
      b.textContent = def.testo;
      b.addEventListener('click', function () {
        if (b.getAttribute('aria-disabled') === 'true') return;
        try { def.clic(); } catch (e) { /* l'app non è ancora pronta */ }
        setTimeout(sicuro, 60);
      });
      azioni.appendChild(b);
      bottoni.push(b);
    });
    document.body.appendChild(ui);

    // tracciamento: i pulsanti di invito avvisano la pagina del sito (demo-modal.js), che decide se registrarli
    ui.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('[data-cta]');
      if (!a || !incorniciata) return;
      try { parent.postMessage({ type: 'abra-demo-cta', demo: cfg.demo || '', action: a.getAttribute('data-cta') }, '*'); } catch (err) { /* senza finestra madre */ }
    });

    // risultato della missione (foto e messaggio): cfg.extra() dà {id, foto:{svg,titolo,didascalia}, chat:{nome,testo,bottone,url,avviso}} o null
    var corpo = ui.querySelector('.vs-corpo'), elFoto = ui.querySelector('.vs-ex-foto'), elChat = ui.querySelector('.vs-ex-chat');
    var extraId = null, fotoOk = false, chatOk = false, tChat = 0;
    var AVVISO = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2 20.5h20z" fill="#ffb020"/><path d="M12 9.5v5.2" stroke="#1a1200" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="17.6" r="1.3" fill="#1a1200"/></svg>';
    var WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a8.5 8.5 0 0 0-7.3 12.8L3.5 20.5l4.8-1.2A8.5 8.5 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 8.6c.3 3.3 2.700 5.700 6.100 6.300l1-1.300-2-1-.9.800c-1-.4-1.800-1.200-2.200-2.200l.8-.9-1-2z" fill="currentColor"/></svg>';
    function nascondiExtra() {
      extraId = null; fotoOk = chatOk = false; clearTimeout(tChat);
      card.classList.remove('vs-ris'); elFoto.textContent = ''; elChat.textContent = '';
      setTimeout(misura, 30);
    }
    ui.querySelector('.vs-nuova').addEventListener('click', function () {
      if (cfg.extraChiuso) try { cfg.extraChiuso(); } catch (e) { /* niente */ }
      nascondiExtra();
    });
    function mostraFoto(f) {
      var fig = document.createElement('figure');
      fig.className = 'vs-foto';
      fig.innerHTML = '<div>' + f.svg + '</div><figcaption><b></b><span></span></figcaption>';
      fig.querySelector('b').textContent = f.titolo || 'Foto dal robot';
      fig.querySelector('span').textContent = f.didascalia || '';
      elFoto.appendChild(fig);
    }
    function mostraChat(c) {
      var ch = document.createElement('div');
      ch.className = 'vs-chat';
      ch.innerHTML = '<div class="vs-ch-h"><span class="vs-av">A</span><span class="vs-ch-n"><b></b><i>online</i></span></div>' +
        '<div class="vs-ch-b"><div class="vs-scrive" aria-label="Sta scrivendo"><i></i><i></i><i></i></div></div>';
      ch.querySelector('b').textContent = c.nome;
      elChat.appendChild(ch);
      corpo.scrollTop = corpo.scrollHeight;
      tChat = setTimeout(function () {
        var m = document.createElement('div'), d = new Date();
        m.className = 'vs-msg';
        m.innerHTML = (c.avviso ? AVVISO : '') + '<span></span><span class="vs-ora"></span>';
        m.children[c.avviso ? 1 : 0].textContent = c.testo;
        m.lastChild.textContent = ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);
        var b = ch.querySelector('.vs-ch-b'); b.textContent = ''; b.appendChild(m);
        var a = document.createElement('a');
        a.className = 'vs-btn vs-wa'; a.href = c.url; a.target = '_blank'; a.rel = 'noopener'; a.setAttribute('data-cta', 'whatsapp');
        a.innerHTML = WA + '<span></span>'; a.lastChild.textContent = c.bottone || 'Rispondi su WhatsApp';
        ch.appendChild(a);
        corpo.scrollTop = corpo.scrollHeight;
        if (c.inviato) try { c.inviato(); } catch (e) { /* niente */ }
      }, c.attesa || 1400);
    }
    function aggiornaExtra() {
      var ex = cfg.extra ? cfg.extra() : null;
      if (!ex) { if (extraId) nascondiExtra(); return; }
      if (ex.id !== extraId) { nascondiExtra(); extraId = ex.id; card.classList.add('vs-ris'); setTimeout(misura, 30); }
      if (ex.foto && !fotoOk) { fotoOk = true; mostraFoto(ex.foto); }
      if (ex.chat && !chatOk) { chatOk = true; mostraChat(ex.chat); }
    }
    window.__semplice = {
      flash: function () { var f = ui.querySelector('.vs-flash'); f.classList.remove('vs-sc'); void f.offsetWidth; f.classList.add('vs-sc'); },
      risultato: function () { return !!extraId; }
    };

    // la scena usa solo lo spazio che la scheda non occupa: --vs-l a sinistra (computer), --vs-b in basso (telefono)
    var ultima = '';
    function misura() {
      var r = card.getBoundingClientRect();
      var tel = telefono.matches;
      var l = tel ? 0 : Math.round(r.right + 12), b = tel ? Math.round(innerHeight - r.top) : 0;
      if (l + ',' + b === ultima) return;
      ultima = l + ',' + b;
      root.style.setProperty('--vs-l', l + 'px');
      root.style.setProperty('--vs-b', b + 'px');
      requestAnimationFrame(function () { window.dispatchEvent(new Event('resize')); });
    }
    if (window.ResizeObserver) new ResizeObserver(misura).observe(card);
    window.addEventListener('resize', misura);

    // sul telefono la spiegazione si chiude da sola dopo qualche secondo e si riapre toccando il titolo
    var toccato = false;
    function adatta() {
      if (telefono.matches) { titolo.setAttribute('aria-expanded', String(!card.classList.contains('vs-chiusa'))); titolo.tabIndex = 0; }
      else { card.classList.remove('vs-chiusa'); titolo.removeAttribute('aria-expanded'); titolo.tabIndex = -1; }
      misura();
    }
    titolo.addEventListener('click', function () {
      if (!telefono.matches) return;
      toccato = true;
      card.classList.toggle('vs-chiusa');
      adatta();
    });
    if (telefono.addEventListener) telefono.addEventListener('change', adatta);
    dopoPronto.push(function () {
      setTimeout(function () { if (telefono.matches && !toccato) { card.classList.add('vs-chiusa'); adatta(); } }, 7000);
    });

    var elStato = ui.querySelector('.vs-stato'), elCit = ui.querySelector('.vs-cit');
    var ultimoStato = '', ultimaCit = '';
    function aggiorna() {
      var occupato = !!(cfg.occupato && cfg.occupato());
      var prossimo = cfg.prossimo ? cfg.prossimo() : -1;   // indice del pulsante da premere adesso
      (cfg.bottoni || []).forEach(function (def, i) {
        bottoni[i].classList.toggle('vs-on', !!(def.on && def.on()));
        bottoni[i].classList.toggle('vs-next', i === prossimo && !occupato);
        bottoni[i].setAttribute('aria-disabled', occupato && def.blocca !== false ? 'true' : 'false');
      });
      var s = cfg.stato ? cfg.stato() : '';
      if (s !== ultimoStato) { ultimoStato = s; elStato.lastChild.textContent = s; }
      elStato.classList.toggle('vs-invito', !!(cfg.invito && cfg.invito()));
      var c = cfg.citazione ? cfg.citazione() : '';
      if (c !== ultimaCit) { ultimaCit = c; elCit.hidden = !c; elCit.textContent = c ? '\u201c' + c + '\u201d' : ''; }
      aggiornaExtra();
      if (cfg.ogni) cfg.ogni();   // es. la telecamera deve seguire sempre il robot
    }
    function sicuro() { try { aggiorna(); } catch (e) { /* la pagina dell'app sta ancora nascendo */ } }
    adatta();
    sicuro();
    setInterval(sicuro, 250);
  });
})();
