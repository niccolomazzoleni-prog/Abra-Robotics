# Genera i due post LinkedIn (nominativo e anonimo) dallo stesso modello. Uso: python3 build-linkedin.py
T='''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Abra Robotics, post LinkedIn consegna Go2 ({VERS})</title>
<link rel="icon" href="../logo/favicon-16.svg">
<link rel="stylesheet" href="../assets/sistema.css">
<style>
  body{{width:1200px;height:1500px;overflow:hidden;position:relative;background:var(--gesso)}}
  .testa{{position:absolute;left:72px;right:72px;top:64px;display:flex;justify-content:space-between;align-items:center}}
  .testa img{{height:36px}}
  .testa .t-etichetta{{font-size:16px;color:var(--grafite)}}
  h1{{position:absolute;left:72px;top:150px;width:1000px;font-size:84px}}
  .chi{{position:absolute;left:72px;top:352px;font-size:25px;width:980px}}
  .tavola{{position:absolute;left:0;top:500px;width:1200px;height:640px}}
  .go2{{position:absolute;left:352px;top:560px;width:500px;filter:grayscale(1) contrast(1.06);mix-blend-mode:multiply}}
  .dist{{position:absolute;left:72px;right:72px;top:1176px;display:grid;grid-template-columns:repeat(3,1fr);column-gap:36px}}
  .voce{{display:flex;gap:14px;align-items:baseline;padding:17px 0 15px;border-top:2px solid var(--flanella);font-size:22px;line-height:1.25}}
  .voce .n{{font-weight:600;font-stretch:75%;font-size:15px;letter-spacing:.06em;color:var(--grafite);min-width:28px}}
  .piede{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font-size:16px;color:var(--grafite)}}
  .piede .esempio{{font-size:12px}}
  .segn{{position:absolute;right:112px;top:1096px;font-size:12px;color:var(--flanella)}}
</style>
</head>
<body>
<div class="testa"><img src="../logo/orizzontale.svg" alt="Abra Robotics"><span class="t-etichetta">{DATA}</span></div>
<h1 class="t-display">Misura il reparto con il LiDAR prima di scrivere il codice.</h1>
<p class="chi t-sotto">{CORPO}</p>

<svg class="tavola" viewBox="0 0 1200 640" aria-hidden="true">
  <path d="M72 0 H586 L600 20 L614 0 H1128 V640 H72 Z" fill="#CFCCC3"/>
  <text x="104" y="44" font-family="Abra Bricolage" font-size="26" font-weight="680" font-stretch="80%" fill="#2F3337">1/6</text>
  <g font-family="Abra Bricolage" fill="#2F3337">
    <text x="120" y="110" font-size="15" font-weight="600" font-stretch="75%" letter-spacing="1.4">INGOMBRO IN PIEDI</text>
    <text x="120" y="140" font-size="28" font-weight="680" font-stretch="80%">circa 70 x 31 x 40 cm</text>
    <text x="120" y="230" font-size="15" font-weight="600" font-stretch="75%" letter-spacing="1.4">LIDAR</text>
    <text x="120" y="260" font-size="28" font-weight="680" font-stretch="80%">Mappa del reparto</text>
    <text x="120" y="288" font-size="18">per localizzazione e</text>
    <text x="120" y="312" font-size="18">navigazione autonoma</text>
{DESTRA}
  </g>
  <path d="M330 262 H398" stroke="#2F3337" stroke-width="2"/><circle cx="404" cy="262" r="5" fill="#2F3337"/>
</svg>
<img class="go2" src="../assets/segnaposto/unitree-go2.png" alt="Segnaposto: quadrupede Unitree Go2, immagine ufficiale del produttore">
<span class="segn t-etichetta">Segnaposto: foto ufficiale Unitree</span>

<div class="dist">
{VOCI}
</div>
<div class="piede"><span>abrarobotics.com · Robotica applicata</span><span class="esempio">{NOTA}</span></div>
</body>
</html>
'''
def voci(v): return '\n'.join(f'  <div class="voce"><span class="n">0{i+1}</span>{x}</div>' for i,x in enumerate(v))
D_NOM='''    <text x="896" y="110" font-size="15" font-weight="600" font-stretch="75%" letter-spacing="1.4">PROGETTO</text>
    <text x="896" y="140" font-size="28" font-weight="680" font-stretch="80%">Tesi in azienda</text>
    <text x="896" y="168" font-size="18">seguita da un tecnico</text>
    <text x="896" y="192" font-size="18">del cliente</text>'''
D_ANO='''    <text x="896" y="110" font-size="15" font-weight="600" font-stretch="75%" letter-spacing="1.4">CONSEGNA</text>
    <text x="896" y="140" font-size="28" font-weight="680" font-stretch="80%">Pacchetto completo</text>
    <text x="896" y="168" font-size="18">i tecnici del cliente</text>
    <text x="896" y="192" font-size="18">lavorano da soli</text>'''
nom=dict(DESTRA=D_NOM,VERS='versione nominativa, da pubblicare solo con consenso scritto',DATA='Consegna del 29 ottobre 2026',
 CORPO="Consegniamo a SACMI un Go2 con LiDAR per una tesi in azienda. Prima il robot mappa il reparto, poi il tesista scrive il codice sul simulatore. Nella cassa c'è anche quello che serve per lavorare da soli.",
 VOCI=voci(['Go2 EDU con LiDAR','Simulatore MuJoCo','Modello digitale del reparto','Manuale tecnico rev. 1.1','Codice in un repository condiviso','85 ore di assistenza']),
 NOTA='Da pubblicare solo con consenso scritto di SACMI')
ano=dict(DESTRA=D_ANO,VERS='versione anonima',DATA='Consegna',
 CORPO="Consegniamo a un'azienda manifatturiera italiana un robot quadrupede con LiDAR. Prima il robot mappa il reparto, poi i tecnici del cliente scrivono il codice sul simulatore, con il materiale che trovano nella cassa.",
 VOCI=voci(['Robot quadrupede con LiDAR','Simulatore MuJoCo','Modello digitale del reparto','Manuale tecnico in italiano','Codice nel repository del cliente','Assistenza in italiano']),
 NOTA='Versione anonima')
import os
d=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','applicazioni')
open(os.path.join(d,'linkedin-sacmi.html'),'w').write(T.format(**nom))
open(os.path.join(d,'linkedin-anonimo.html'),'w').write(T.format(**ano))
print('ok')
