/* Metro da sarta (v3: nastro in gesso blu, Pantone 278 C): disegna un nastro millimetrato in SVG dentro gli elementi [data-metro].
   Attributi: data-from (cm iniziale), data-to (cm finale), data-step (px per cm),
   data-dir ("h" orizzontale, "v" verticale con lo zero in basso), data-w (spessore nastro px),
   data-label (cifre ogni N cm, default 10), data-sw (moltiplicatore spessore tacche).
   Regola: il metro si usa solo dove misura qualcosa di vero, con la scala allineata all'oggetto. */
(function(){
  const NS='http://www.w3.org/2000/svg';
  function draw(el){
    const from=+el.dataset.from||0, to=+el.dataset.to||100, step=+el.dataset.step||8;
    const dir=el.dataset.dir||'h', tw=+el.dataset.w||36, every=+el.dataset.label||10;
    const len=(to-from)*step+4;
    const ink=el.dataset.ink||'#2F3337', tape=el.dataset.tape||'#8BB8E8', k=+el.dataset.sw||1;
    const W=dir==='h'?len:tw, H=dir==='h'?tw:len;
    const s=document.createElementNS(NS,'svg');
    s.setAttribute('viewBox',`0 0 ${W} ${H}`);s.setAttribute('width',W);s.setAttribute('height',H);
    s.style.display='block';
    let h=`<rect width="${W}" height="${H}" fill="${tape}"/>`;
    const fs=Math.max(9,Math.round(tw*0.34));
    for(let c=from;c<=to;c++){
      const p=(c-from)*step+2;
      const l=c%every===0?tw*0.46:(c%5===0?tw*0.3:tw*0.18);
      const sw=(c%every===0?1.6:1.1)*k;
      if(dir==='h'){
        h+=`<line x1="${p}" y1="0" x2="${p}" y2="${l}" stroke="${ink}" stroke-width="${sw}"/>`;
        if(c%every===0&&c!==from) h+=`<text x="${p+2}" y="${tw-5}" font-size="${fs}" fill="${ink}" font-family="Abra Bricolage" font-weight="680" font-stretch="80%">${c}</text>`;
      }else{
        const y=H-p;
        h+=`<line x1="0" y1="${y}" x2="${l}" y2="${y}" stroke="${ink}" stroke-width="${sw}"/>`;
        if(c%every===0&&c!==from) h+=`<text x="${tw-4}" y="${y+fs+1}" text-anchor="end" font-size="${fs}" fill="${ink}" font-family="Abra Bricolage" font-weight="680" font-stretch="80%">${c}</text>`;
      }
    }
    s.innerHTML=h; el.innerHTML=''; el.appendChild(s);
  }
  function all(){document.querySelectorAll('[data-metro]').forEach(draw)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',all);else all();
  window.abraMetro=all;
})();
