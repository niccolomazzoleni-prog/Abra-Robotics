// testo in tracciati da TTF locali, opentype.js in Chrome. node txt.js out.json
const {chromium}=require('/Users/niccolomazzoleni/Downloads/prisma-hero/node_modules/playwright');
const fs=require('fs');const F='/Users/niccolomazzoleni/Abra-Robotics-brand/brand/02-directions/B-umanesimo/fonts/';
const jobs=[{id:'rob_caps_r',font:'InstrumentSans-Regular.ttf',text:'ROBOTICS',ls:0.14},{id:'rob_caps_b',font:'InstrumentSans-Bold.ttf',text:'ROBOTICS',ls:0.12},{id:'rob_r',font:'InstrumentSans-Regular.ttf',text:'Robotics',ls:0},{id:'rob_b',font:'InstrumentSans-Bold.ttf',text:'Robotics',ls:0}];
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage();await p.goto('about:blank');
await p.addScriptTag({url:'https://cdnjs.cloudflare.com/ajax/libs/opentype.js/1.3.4/opentype.min.js'});
const out={};
for(const j of jobs){const b64=fs.readFileSync(F+j.font).toString('base64');
 out[j.id]=await p.evaluate(({b64,j})=>{const bin=atob(b64);const u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
  const font=opentype.parse(u.buffer);const size=1000;let x=0;let d='';const glyphs=font.stringToGlyphs(j.text);
  glyphs.forEach((g,i)=>{const path=g.getPath(x,0,size);d+=path.toPathData(2);x+=g.advanceWidth*size/font.unitsPerEm+j.ls*size; if(i<glyphs.length-1){x+=font.getKerningValue(g,glyphs[i+1])*size/font.unitsPerEm;}});
  const full=new opentype.Path();full.commands=[];
  return {d,adv:x-j.ls*size,upm:font.unitsPerEm,cap:font.tables.os2.sCapHeight*size/font.unitsPerEm,xh:font.tables.os2.sxHeight*size/font.unitsPerEm};
 },{b64,j});}
fs.writeFileSync(process.argv[2],JSON.stringify(out));await b.close();console.log(Object.keys(out).map(k=>k+' '+out[k].adv.toFixed(0)+' cap '+out[k].cap).join('\n'));})();
