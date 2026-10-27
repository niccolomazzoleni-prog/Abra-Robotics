import os
os.chdir(os.path.join(os.path.dirname(__file__),'..','..','applicazioni'))
T='''<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<title>{TITLE}</title>
<link rel="stylesheet" href="../sistema.css">
<style>
body{margin:0;font-family:var(--f)}
.post{position:relative;width:1200px;height:1500px;background:var(--carta);color:var(--grafite);overflow:hidden;padding:72px}
.testa{display:flex;justify-content:space-between;align-items:center}
.testa img{height:52px}
.testa .lbl{font-size:15px;color:var(--fumo)}
h1{margin:96px 0 0;font-size:76px;max-width:900px}
.sotto{margin:28px 0 0;font-size:26px;line-height:1.45;max-width:880px}
.finestra{position:absolute;left:72px;top:640px;width:500px;height:680px;background:var(--cemento)}
.finestra .pav{position:absolute;left:0;right:0;bottom:0;height:320px;background:#D9D8D2}
.finestra img{position:absolute;left:60px;bottom:96px;width:380px;z-index:2}
.finestra .ombra{position:absolute;left:96px;bottom:82px;width:320px;height:34px;border-radius:50%;background:rgba(32,33,36,.24);filter:blur(7px)}
.dida-r{position:absolute;left:72px;top:1336px;width:500px;font-size:15px;color:var(--fumo);line-height:1.4}
.resta{position:absolute;left:630px;right:72px;top:660px}
.resta .lbl{font-size:15px;color:var(--magenta);margin:0 0 12px}
.resta ol{list-style:none;margin:0;padding:0}
.resta li{display:grid;grid-template-columns:56px 1fr;border-top:1.5px solid var(--grafite);padding:16px 0;font-size:25px;font-weight:600;line-height:1.25}
.resta li b{font-size:18px;color:var(--magenta);padding-top:5px}
.nota{position:absolute;left:630px;right:72px;bottom:72px;font-size:16px;color:var(--fumo);line-height:1.45}
.bozza{position:absolute;right:72px;top:150px;color:var(--magenta)}
</style></head>
<body>
<div class="post">
  <div class="testa"><img src="../logo/orizzontale.svg" alt="abra Robotics"><span class="lbl">{TAG}</span></div>
  {BOZZA}
  <h1 class="titolo">Fai lavorare il tesista sul robot dal primo giorno.</h1>
  <p class="sotto txt">{SOTTO}</p>
  <div class="finestra arco"><div class="pav"></div><div class="ombra"></div><img src="img/segnaposto-unitree-go2.png" alt="Quadrupede (segnaposto)"></div>
  <p class="dida dida-r">(Segnaposto: immagine ufficiale Unitree Go2. Qui andrà la foto della consegna.)</p>
  <div class="resta">
    <p class="lbl">{CHI}</p>
    <ol>{LISTA}</ol>
  </div>
  <p class="nota dida">{NOTA}</p>
</div>
</body></html>
'''
def lista(items): return ''.join(f'<li><b>{i+1:02d}</b><span>{t}</span></li>' for i,t in enumerate(items))
V={
'linkedin-sacmi.html':dict(TITLE='Post LinkedIn, consegna Go2 (versione nominativa, da pubblicare solo con consenso scritto)',TAG='Consegna · 29 ottobre 2026',
 BOZZA='<span class="esempio bozza">Bozza: da pubblicare solo con consenso scritto</span>',
 SOTTO='Il 29 ottobre consegniamo a SACMI un quadrupede Go2 per una tesi in azienda. Lo stabilimento è già mappato e il codice è già nel repository dei tecnici: il tesista parte dal simulatore la prima settimana.',
 CHI='Cosa resta a SACMI',LISTA=lista(['Go2 EDU con LiDAR','Mappatura LiDAR e digital twin dello stabilimento','SLAM e navigazione già configurati','Simulatore MuJoCo della stessa area','Manuale tecnico, revisione 1.1','Repository di codice condiviso con i tecnici','85 ore di assistenza']),
 NOTA='(File da pubblicare solo con il consenso scritto di SACMI. Nessun logo del cliente.)'),
'linkedin-sacmi-anonima.html':dict(TITLE='Post LinkedIn, consegna Go2 (versione anonima)',TAG='Tesi in azienda',BOZZA='',
 SOTTO="Consegniamo un quadrupede Go2 a un'azienda manifatturiera per una tesi. L'area di lavoro è già mappata e il codice è già nel repository dei tecnici: il tesista parte dal simulatore la prima settimana.",
 CHI='Cosa resta al cliente',LISTA=lista(['Robot quadrupede con LiDAR',"Mappa e digital twin dell'area di lavoro",'Navigazione autonoma già configurata','Simulatore della stessa area','Manuale tecnico','Repository di codice condiviso','Assistenza nei primi mesi']),
 NOTA='(Versione anonima, pronta finché manca il consenso: senza data, nome o dettagli che rendano riconoscibile il cliente.)'),
}
for fn,v in V.items():
    s=T
    for k,val in v.items(): s=s.replace('{'+k+'}',val)
    open(fn,'w').write(s)
