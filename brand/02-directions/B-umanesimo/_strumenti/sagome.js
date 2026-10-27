// Sagome di persone per le scene degli eventi: figure piatte, senza volto, come nei rendering architettonici.
// sagoma(x, base, h, {v, col}) -> SVG. x = asse, base = linea dei piedi, h = altezza totale.
const f=v=>+v.toFixed(1);
function sagoma(x,base,h,o={}){
  const {v=0,col='#5E6264'}=o;
  const u=h/172;
  const hr=10.5*u;                                  // raggio della testa
  const top=base-h, cyH=top+hr*1.12;
  const yN=top+2.2*hr+1*u, ySh=yN+4*u;              // collo, spalle
  const sh=(v===2?44:41)*u, wa=(v===2?36:31)*u;     // larghezza spalle, vita
  const yHip=base-84*u;
  const coat=v===2?14*u:0;
  let d='';
  d+=`M${f(x-hr*0.88)} ${f(cyH)}A${f(hr*0.88)} ${f(hr*1.12)} 0 1 1 ${f(x+hr*0.88)} ${f(cyH)}A${f(hr*0.88)} ${f(hr*1.12)} 0 1 1 ${f(x-hr*0.88)} ${f(cyH)}Z`;
  d+=`M${f(x-4.5*u)} ${f(cyH+hr*0.8)}H${f(x+4.5*u)}V${f(ySh+3*u)}H${f(x-4.5*u)}Z`;
  // busto con braccia unite: spalle tonde, braccia lungo i fianchi fino a metà coscia
  const yHand=yHip+14*u, arm=7.5*u;
  d+=`M${f(x-sh/2)} ${f(ySh+8*u)}Q${f(x-sh/2)} ${f(ySh)} ${f(x-sh/2+9*u)} ${f(ySh)}H${f(x+sh/2-9*u)}Q${f(x+sh/2)} ${f(ySh)} ${f(x+sh/2)} ${f(ySh+8*u)}`
    +`L${f(x+sh/2+1.5*u)} ${f(yHand)}H${f(x+sh/2-arm)}L${f(x+wa/2+coat/2)} ${f(yHip+coat)}H${f(x-wa/2-coat/2)}L${f(x-sh/2+arm)} ${f(yHand)}H${f(x-sh/2-1.5*u)}Z`;
  // gambe leggermente rastremate
  const lw=12.5*u, g=2.5*u;
  d+=`M${f(x-g/2-lw)} ${f(yHip-1)}H${f(x-g/2)}L${f(x-g/2-1*u)} ${f(base)}H${f(x-g/2-lw+1.5*u)}Z`;
  d+=`M${f(x+g/2)} ${f(yHip-1)}H${f(x+g/2+lw)}L${f(x+g/2+lw-1.5*u)} ${f(base)}H${f(x+g/2+1*u)}Z`;
  if(v===3) d+=`M${f(x+sh/2-2*u)} ${f(yHip-18*u)}h${f(13*u)}v${f(19*u)}h${f(-13*u)}Z`;
  return `<path fill="${col}" d="${d}"/>`;
}
module.exports={sagoma};
