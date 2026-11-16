/* Manometro della Linea 3, solo per la vista semplice di Fleet Control.
   Un'unica fonte per il disegno del quadrante: serve sia come texture del quadrante nella scena 3D (app.js)
   sia come «Foto dal robot» nella scheda dei comandi (index.html). Scala 0-10 bar, settori verde / giallo / rosso,
   lancetta a 8,7 bar (soglia 6 bar). Nessun emoji, nessuna immagine esterna. */
(function () {
  var VALORE = 8.7, SOGLIA = 6, GIALLO = 4.5, FONDO = 10;
  var CX = 100, CY = 100;
  function ang(v) { return (135 + 27 * v) * Math.PI / 180; }   // 0 bar in basso a sinistra, 10 bar in basso a destra, 270 gradi in senso orario
  function pt(v, r) { return [(CX + r * Math.cos(ang(v))).toFixed(2), (CY + r * Math.sin(ang(v))).toFixed(2)]; }
  function arco(v1, v2, r, col, w) {
    var a = pt(v1, r), b = pt(v2, r), grande = (v2 - v1) * 27 > 180 ? 1 : 0;
    return '<path d="M' + a[0] + ' ' + a[1] + ' A' + r + ' ' + r + ' 0 ' + grande + ' 1 ' + b[0] + ' ' + b[1] + '" fill="none" stroke="' + col + '" stroke-width="' + w + '" stroke-linecap="butt"/>';
  }
  function quadrante() {
    var s = '<circle cx="100" cy="100" r="97" fill="#26282b"/><circle cx="100" cy="100" r="90" fill="#f1f1ec"/>';
    s += arco(0, GIALLO, 74, '#2fbf5a', 15) + arco(GIALLO, SOGLIA, 74, '#f2c200', 15) + arco(SOGLIA, FONDO, 74, '#e23b30', 15);
    for (var v = 0; v <= FONDO; v++) {
      var a = pt(v, 62), b = pt(v, 83);
      s += '<line x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '" stroke="#15171a" stroke-width="' + (v % 2 ? 1.6 : 2.6) + '"/>';
      if (v % 2 === 0) { var t = pt(v, 50); s += '<text x="' + t[0] + '" y="' + (+t[1] + 5) + '" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="15" fill="#15171a">' + v + '</text>'; }
    }
    s += '<text x="100" y="140" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="15" fill="#15171a">bar</text>';
    var p = pt(VALORE, 70), c = pt(VALORE + 5.5, 12), d = pt(VALORE - 5.5, 12);
    s += '<polygon points="' + p[0] + ',' + p[1] + ' ' + c[0] + ',' + c[1] + ' ' + d[0] + ',' + d[1] + '" fill="#15171a"/>';
    s += '<circle cx="100" cy="100" r="9" fill="#15171a"/><circle cx="100" cy="100" r="3" fill="#8a8d90"/>';
    return s;
  }
  window.ABRA_MANOMETRO = {
    valore: VALORE, soglia: SOGLIA,
    // il quadrante da solo (200 x 200), per la texture 3D
    svgQuadrante: function () {
      return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="1024" height="1024">' + quadrante() + '</svg>';
    },
    // la «foto» scattata dal robot (320 x 160): impianto sfocato, quadrante, lettura grande, mirino
    svgFoto: function () {
      var rack = '';
      for (var i = 0; i < 6; i++) rack += '<rect x="' + (i * 58 - 8) + '" y="' + (18 + (i % 2) * 8) + '" width="46" height="' + (70 - (i % 3) * 6) + '" fill="#2a3138" opacity="0.55"/>';
      return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 160" role="img" aria-label="Foto del manometro della Linea 3: lancetta nel settore rosso, 8,7 bar">' +
        '<defs><linearGradient id="mf-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2328"/><stop offset="1" stop-color="#0c0f12"/></linearGradient><filter id="mf-sf"><feGaussianBlur stdDeviation="2.4"/></filter></defs>' +
        '<rect width="320" height="160" fill="url(#mf-bg)"/><g filter="url(#mf-sf)">' + rack + '<rect y="108" width="320" height="52" fill="#15191d"/></g>' +
        '<rect x="45" y="120" width="12" height="40" fill="#d8b000"/>' +
        '<g transform="translate(10,6) scale(.64)">' + quadrante() + '</g>' +
        '<rect x="22" y="132" width="86" height="22" rx="3" fill="#f2c200"/><text x="65" y="148.5" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="16" fill="#111">LINEA 3</text>' +
        '<text x="206" y="82" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="48" fill="#ff5a4d">8,7</text>' +
        '<text x="206" y="106" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="600" font-size="20" fill="#f5f5f5">bar</text>' +
        '<g fill="none" stroke="#fff" stroke-width="2" opacity=".85"><path d="M8 24V8h16M296 8h16v16M312 136v16h-16M24 152H8v-16"/></g>' +
        '</svg>';
    }
  };
})();
