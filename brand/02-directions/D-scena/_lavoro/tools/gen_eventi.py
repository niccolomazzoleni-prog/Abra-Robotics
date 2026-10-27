# Genera reel-g1.html con il pubblico disegnato
import os,sys
sys.path.insert(0,os.path.dirname(__file__))
from pubblico import folla
os.chdir(os.path.join(os.path.dirname(__file__),'..','..','applicazioni'))
F=folla(1080,560,[(470,1.25,'#34353B',6),(560,1.65,'#121316',5)],seed=7)
reel=f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<title>Copertina reel Instagram, demo del G1 che risponde al pubblico</title>
<link rel="stylesheet" href="../sistema.css">
<style>
body{{margin:0;font-family:var(--f)}}
.reel{{position:relative;width:1080px;height:1920px;background:var(--grafite);color:var(--carta);overflow:hidden}}
.top{{position:absolute;left:80px;right:80px;top:150px;display:flex;justify-content:space-between;align-items:center}}
.top img{{height:46px}}
.top .lbl{{font-size:18px;color:var(--fumo-chiaro)}}
h1{{position:absolute;left:80px;top:290px;width:960px;margin:0;font-size:128px;color:var(--carta)}}
.boccascena{{position:absolute;left:150px;top:720px;width:780px;height:1080px;background:var(--magenta)}}
.boccascena img{{position:absolute;left:50%;bottom:130px;height:640px;transform:translateX(-50%)}}
.boccascena .pedana{{position:absolute;left:0;right:0;bottom:0;height:150px;background:#B0005B}}
.battuta{{position:absolute;left:220px;top:830px;width:660px;color:var(--carta);z-index:3}}
.battuta .lbl{{font-size:16px;margin:0 0 10px;color:var(--carta)}}
.battuta p.t{{margin:0;font-size:36px;line-height:1.25;font-weight:600}}
.folla{{position:absolute;left:0;right:0;bottom:0;height:560px;z-index:4}}
.folla svg{{width:100%;height:100%;display:block}}
.dida-r{{position:absolute;left:80px;top:650px;width:900px;font-size:17px;color:var(--fumo-chiaro);margin:0}}
.esempio{{position:absolute;right:210px;top:832px;z-index:5;color:var(--carta);font-size:14px}}
</style></head>
<body>
<div class="reel">
  <div class="top"><img src="../logo/orizzontale-negativo.svg" alt="abra Robotics"><span class="lbl">Eventi e fiere</span></div>
  <h1 class="scena">Fai parlare l'umanoide<br>con il tuo pubblico.</h1>
  <p class="dida dida-r">(Segnaposto: immagine ufficiale Unitree G1 nella versione su colonna. Qui andrà un fotogramma della demo.)</p>
  <div class="boccascena arco">
    <div class="pedana"></div>
    <img src="img/segnaposto-unitree-g1d.png" alt="Umanoide che parla al pubblico (segnaposto)">
  </div>
  <div class="battuta"><p class="lbl">G1, dal copione approvato</p><p class="t">«Va in lavastoviglie solo la griglia. Le mostro come si smonta?»</p></div>
  <span class="esempio">Esempio</span>
  <div class="folla">{F}</div>
</div>
</body></html>
'''
open('reel-g1.html','w').write(reel)

# Totem 80 x 200 cm (10 px = 1 cm) in una tavola con quote
F2=folla(800,260,[(200,0.62,'#34353B',6),(260,0.8,'#121316',5)],seed=11)
totem=f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<title>Totem 80 x 200 cm, noleggio dell'umanoide per eventi</title>
<link rel="stylesheet" href="../sistema.css">
<style>
body{{margin:0;font-family:var(--f)}}
.tavola{{position:relative;width:1400px;height:2200px;background:var(--cemento);overflow:hidden}}
.pavimento{{position:absolute;left:0;right:0;bottom:0;height:120px;background:#D6D5CF}}
.totem{{position:absolute;left:100px;top:80px;width:800px;height:2000px;background:var(--grafite);color:var(--carta);overflow:hidden;box-shadow:0 30px 50px rgba(32,33,36,.25)}}
.totem .logo{{position:absolute;left:64px;top:64px;height:50px}}
.totem .lbl-t{{position:absolute;left:64px;top:170px;font-size:17px;color:var(--fumo-chiaro)}}
h1{{position:absolute;left:64px;top:214px;width:680px;margin:0;font-size:104px;z-index:3}}
.arco-t{{position:absolute;left:64px;top:690px;width:672px;height:640px;background:var(--magenta)}}
.arco-t img{{position:absolute;left:50%;bottom:30px;height:520px;transform:translateX(-50%)}}
.arco-t .folla{{position:absolute;left:0;right:0;bottom:0;height:200px}}
.arco-t .folla svg{{width:100%;height:100%;display:block}}
.dida-r{{position:absolute;left:64px;top:1340px;width:672px;font-size:14px;color:var(--fumo-chiaro);margin:0}}
.info{{position:absolute;left:64px;right:64px;top:1390px}}
.info ol{{list-style:none;margin:0;padding:0}}
.info li{{display:grid;grid-template-columns:52px 1fr;border-top:1.5px solid #4A4B51;padding:12px 0;font-size:24px;font-weight:600;line-height:1.2}}
.info li b{{color:var(--carta);font-size:17px;padding-top:5px}}
.info li small{{display:block;font-weight:400;font-size:18px;margin-top:3px;color:var(--fumo-chiaro)}}
.cta{{position:absolute;left:64px;right:64px;bottom:60px;display:grid;grid-template-columns:1fr 170px;gap:28px;align-items:end}}
.cta .scena{{font-size:62px;margin:0}}
.cta p.txt{{margin:10px 0 0;font-size:22px;font-weight:600}}
.cta img{{width:170px;height:170px;display:block}}
.esempio-t{{position:absolute;right:64px;top:1352px;color:var(--fumo-chiaro);font-size:11px}}
.quota{{position:absolute;bottom:120px;width:2px;background:var(--grafite)}}
.quota::before,.quota::after{{content:"";position:absolute;left:-9px;width:20px;height:2px;background:var(--grafite)}}
.quota::before{{top:0}}.quota::after{{bottom:0}}
.quota span{{position:absolute;left:14px;top:50%;font-size:16px;white-space:nowrap;color:var(--grafite)}}
.nota{{position:absolute;left:980px;top:120px;width:360px;font-size:19px;line-height:1.5;color:var(--grafite)}}
.nota .lbl{{font-size:12px;margin:0 0 10px;color:var(--fumo)}}
</style></head>
<body>
<div class="tavola">
  <div class="pavimento"></div>
  <div class="totem">
    <img class="logo" src="../logo/orizzontale-negativo.svg" alt="abra Robotics">
    <p class="lbl lbl-t">Noleggio per eventi e fiere</p>
    <h1 class="scena">Noleggia l'umanoide per il tuo evento, con un tecnico Abra in sala.</h1>
    <div class="arco-t arco"><img src="img/segnaposto-unitree-g1d.png" alt="Umanoide (segnaposto)"><div class="folla">{F2}</div></div>
    <p class="dida dida-r">(Segnaposto: immagine ufficiale Unitree G1 nella versione su colonna.)</p>
    <span class="esempio esempio-t">Esempio</span>
    <div class="info txt"><ol>
      <li><b>01</b><span>A giornata, trasporto compreso<small>Il prezzo si definisce con la data e il luogo</small></span></li>
      <li><b>02</b><span>Un tecnico Abra per tutta la giornata<small>Accende, sorveglia e cambia la batteria</small></span></li>
      <li><b>03</b><span>Copione e risposte approvati da te<small>L'umanoide parla del tuo marchio, in italiano e in inglese</small></span></li>
      <li><b>04</b><span>Prova generale prima della data<small>La vedi dal vivo o in video, poi decidi</small></span></li>
    </ol></div>
    <div class="cta"><div><p class="scena">Chiedi una data</p><p class="txt">abrarobotics.com/eventi</p></div><img src="img/qr-eventi.svg" alt="QR verso abrarobotics.com/eventi"></div>
  </div>
  <div class="quota" style="left:940px;height:2000px"><span>totem 200 cm</span></div>
  <div class="quota" style="left:1120px;height:1750px"><span>persona 175 cm</span></div>
  <div class="quota" style="left:1280px;height:1320px"><span>G1 132 cm</span></div>
  <div class="nota"><p class="lbl">Totem 80 x 200 cm, stampa su forex</p>Accanto al totem sta il G1 vero, sul disco magenta "a". Le quote danno la scala: il titolo si legge a 6 metri, la chiamata all'azione e il QR ad altezza di mano.</div>
</div>
</body></html>
'''
open('totem.html','w').write(totem)
