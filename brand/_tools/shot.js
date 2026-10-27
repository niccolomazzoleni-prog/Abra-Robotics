// Uso: node brand/_tools/shot.js <file.html> <out.png> [larghezza] [altezza] [fullPage:0|1]
// Stampa gli errori di console e le richieste fallite. Usa Chrome di sistema.
const {chromium}=require('/Users/niccolomazzoleni/Downloads/prisma-hero/node_modules/playwright');
const path=require('path');
(async()=>{
  const [,,inp,out,w='1440',h='900',full='0']=process.argv;
  const b=await chromium.launch({channel:'chrome'});
  const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
  const errs=[];
  p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text())});
  p.on('pageerror',e=>errs.push('pageerror: '+e.message));
  p.on('requestfailed',r=>errs.push('failed: '+r.url()));
  p.on('response',r=>{if(r.status()>=400)errs.push(r.status()+': '+r.url())});
  await p.goto('file://'+path.resolve(inp),{waitUntil:'networkidle'});
  await p.waitForTimeout(600);
  await p.screenshot({path:out,fullPage:full==='1'});
  await b.close();
  console.log(errs.length?errs.join('\n'):'nessun errore');
})();
