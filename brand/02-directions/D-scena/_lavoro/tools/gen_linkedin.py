import os
os.chdir(os.path.join(os.path.dirname(__file__),'..','..','applicazioni'))
T=open('../_lavoro/tools/linkedin.tpl').read()
V={
 'linkedin-sacmi.html':dict(ver="versione nominativa",
   sotto="Il 29 ottobre consegniamo a SACMI un quadrupede Go2 per una tesi in azienda. Il robot arriva con lo stabilimento già mappato e il codice già nel repository dei tecnici.",
   chi="a SACMI",dove="dello stabilimento",
   nota="(Versione nominativa: si pubblica solo con il consenso scritto di SACMI, senza il suo logo.)"),
 'linkedin-sacmi-anonima.html':dict(ver="versione anonima",
   sotto="Il 29 ottobre consegniamo un quadrupede Go2 a un gruppo industriale italiano, per una tesi in azienda. Il robot arriva con l'area di lavoro già mappata e il codice già nel repository dei tecnici.",
   chi="al cliente",dove="dell'area di lavoro",
   nota="(Versione anonima: pronta da pubblicare finché manca il consenso scritto del cliente.)"),
}
for fn,v in V.items():
    s=T
    for k,val in v.items(): s=s.replace('{'+k+'}',val)
    open(fn,'w').write(s)
