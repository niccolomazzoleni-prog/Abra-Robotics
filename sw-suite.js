/* Suite software Abra: anteprime animate (stesse della home). */
(function(){
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')}
  function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim()}
var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* Run a draw loop only while the element is on screen */
  function whenVisible(el,start,stop){
    new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?start():stop()})},{threshold:.05}).observe(el);
  }
  function fit(cv){
    var r=cv.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);
    cv.width=Math.max(1,r.width*d);cv.height=Math.max(1,r.height*d);
    var c=cv.getContext('2d');c.setTransform(d,0,0,d,0,0);return {c:c,w:r.width,h:r.height};
  }

  /* Lazy videos: play only when visible */
  document.querySelectorAll('video[data-src]').forEach(function(v){
    var src=v.getAttribute('data-src');
    if(!src)return;
    var slot=v.closest('[data-video-slot]');if(slot)slot.classList.add('has-video');
    if(RM)return;
    whenVisible(v,function(){if(!v.src)v.src=src;v.play().catch(function(){})},function(){v.pause()});
  });

  /* Humanoid Studio: two-link arm doing pick and place */
  document.querySelectorAll('canvas.hs-sim').forEach(function(cv){
    var g,raf=0,t0=performance.now(),slot=cv.parentNode,stepEl=slot.querySelector('[data-hs-step]'),cntEl=slot.querySelector('[data-hs-count]'),count=0,lastCyc=-1;
    var STEPS=['Rilevamento pezzo','Avvicinamento','Presa','Trasferimento','Posa in maschera','Rilascio'];
    function ik(sx,sy,tx,ty,l1,l2){
      var dx=tx-sx,dy=ty-sy,d=Math.min(Math.hypot(dx,dy),l1+l2-.01),a=Math.atan2(dy,dx);
      var b=Math.acos((l1*l1+d*d-l2*l2)/(2*l1*d));return [a+b,sx+Math.cos(a+b)*l1,sy+Math.sin(a+b)*l1];
    }
    function lerp(a,b,k){return a+(b-a)*k}
    function ease(k){return k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2}
    function draw(now){
      var c=g.c,W=g.w,H=g.h,acc=css('--acc')||'#8b5cf6',acc2=css('--acc2')||'#2bc4a8';
      c.clearRect(0,0,W,H);
      /* grid floor */
      c.strokeStyle='rgba(255,255,255,.06)';c.lineWidth=1;
      for(var gx=0;gx<W;gx+=22){c.beginPath();c.moveTo(gx,0);c.lineTo(gx,H);c.stroke()}
      for(var gy=0;gy<H;gy+=22){c.beginPath();c.moveTo(0,gy);c.lineTo(W,gy);c.stroke()}
      var base=H*.7,sx=W*.5,sy=H*.36,l1=H*.27,l2=H*.27;
      /* torso of the humanoid */
      c.fillStyle='rgba(255,255,255,.08)';c.strokeStyle='rgba(255,255,255,.35)';
      c.beginPath();c.roundRect(sx-24,sy-22,48,H*.3,10);c.fill();c.stroke();
      c.beginPath();c.arc(sx,sy-36,11,0,7);c.stroke();
      /* tray (left) and fixture (right) */
      var trayX=W*.2,fixX=W*.8;
      c.fillStyle='rgba(255,255,255,.1)';c.fillRect(trayX-46,base,92,8);c.fillRect(fixX-40,base,80,8);
      c.strokeStyle=acc2;c.setLineDash([4,4]);c.strokeRect(fixX-15,base-22,30,22);c.setLineDash([]);
      c.fillStyle='rgba(255,255,255,.55)';c.font='10px ui-monospace,monospace';c.fillText('VASSOIO',trayX-24,base+20);c.fillText('MASCHERA',fixX-26,base+20);
      var T=4.2,t=((now-t0)/1000)/T,cyc=Math.floor(t),p=t-cyc;
      if(cyc!==lastCyc){if(lastCyc>=0)count++;lastCyc=cyc;if(cntEl)cntEl.textContent=count+' pezzi'}
      var up=base-H*.2,pick=base-12,place=base-12,tx,ty,hold=false,st;
      if(p<.15){st=0;tx=lerp(fixX,trayX,ease(p/.15));ty=up}
      else if(p<.28){st=1;tx=trayX;ty=lerp(up,pick,ease((p-.15)/.13))}
      else if(p<.36){st=2;tx=trayX;ty=pick;hold=p>.32}
      else if(p<.7){st=3;hold=true;var k=ease((p-.36)/.34);tx=lerp(trayX,fixX,k);ty=lerp(pick,place,k)-Math.sin(k*Math.PI)*H*.22}
      else if(p<.85){st=4;hold=true;tx=fixX;ty=place}
      else{st=5;tx=fixX;ty=lerp(place,up,ease((p-.85)/.15))}
      if(stepEl)stepEl.textContent=STEPS[st];
      /* remaining parts in the tray */
      for(var n=0;n<3;n++){if(n===0&&(hold||st>=4))continue;c.fillStyle=n?'rgba(255,255,255,.35)':'#fff';c.fillRect(trayX-30+n*24,base-12,16,12)}
      /* placed part */
      if(st===5||(st===0&&cyc>0)){c.fillStyle=acc2;c.fillRect(fixX-8,base-12,16,12)}
      /* planned trajectory */
      c.strokeStyle='rgba(255,255,255,.18)';c.setLineDash([3,5]);c.beginPath();
      for(var s=0;s<=1.001;s+=.05){var xx=lerp(trayX,fixX,s),yy=pick-Math.sin(s*Math.PI)*H*.22;s?c.lineTo(xx,yy):c.moveTo(xx,yy)}
      c.stroke();c.setLineDash([]);
      /* arm */
      var j=ik(sx+20,sy,tx,ty-14,l1,l2);
      c.strokeStyle='#fff';c.lineWidth=7;c.lineCap='round';c.beginPath();c.moveTo(sx+20,sy);c.lineTo(j[1],j[2]);c.lineTo(tx,ty-14);c.stroke();
      c.fillStyle=acc;[[sx+20,sy],[j[1],j[2]]].forEach(function(q){c.beginPath();c.arc(q[0],q[1],5,0,7);c.fill()});
      /* gripper */
      var o=hold?5:10;c.strokeStyle=acc;c.lineWidth=3;c.beginPath();c.moveTo(tx-o,ty-14);c.lineTo(tx-o,ty-2);c.moveTo(tx+o,ty-14);c.lineTo(tx+o,ty-2);c.stroke();
      if(hold&&st<5){c.fillStyle='#fff';c.fillRect(tx-8,ty-12,16,12)}
      /* vision box on the target part */
      if(st<=1){c.strokeStyle=acc2;c.lineWidth=1;c.strokeRect(trayX-34,base-16,24,20);c.fillStyle=acc2;c.fillText('pezzo 0.97',trayX-34,base-20)}
      raf=requestAnimationFrame(draw);
    }
    function start(){if(slot.classList.contains('has-video'))return;g=fit(cv);if(RM){draw(t0+1500);cancelAnimationFrame(raf);return}if(!raf)raf=requestAnimationFrame(draw)}
    function stop(){cancelAnimationFrame(raf);raf=0}
    whenVisible(cv,start,stop);addEventListener('resize',function(){if(raf)g=fit(cv)});
  });

  /* Fleet Control: top-down map, Go2 on patrol, LiDAR rays build the map, click to send */
  document.querySelectorAll('canvas.fleet').forEach(function(cv){
    var g,raf=0,last=0,slot=cv.parentNode,stEl=slot.querySelector('[data-fl-state]'),batEl=slot.querySelector('[data-fl-bat]');
    var walls=[],hits=[],route=[[.15,.8],[.15,.2],[.5,.2],[.5,.55],[.85,.55],[.85,.85]],wi=0,pos=[.15,.8],head=0,bat=92,goto=null;
    function build(){
      walls=[[.05,.08,.95,.08],[.95,.08,.95,.95],[.95,.95,.05,.95],[.05,.95,.05,.08],[.32,.08,.32,.42],[.32,.62,.32,.95],[.32,.42,.42,.42],[.66,.3,.66,.72],[.66,.3,.78,.3],[.7,.08,.7,.16]];
      [[.43,.68,.12,.12],[.76,.68,.1,.08],[.12,.45,.1,.12]].forEach(function(r){walls.push([r[0],r[1],r[0]+r[2],r[1]],[r[0]+r[2],r[1],r[0]+r[2],r[1]+r[3]],[r[0]+r[2],r[1]+r[3],r[0],r[1]+r[3]],[r[0],r[1]+r[3],r[0],r[1]])});
    }
    build();
    function ray(ox,oy,a,max){
      var dx=Math.cos(a),dy=Math.sin(a),best=max;
      for(var k=0;k<walls.length;k++){var w=walls[k],ex=w[2]-w[0],ey=w[3]-w[1],den=dx*ey-dy*ex;if(Math.abs(den)<1e-9)continue;
        var t=((w[0]-ox)*ey-(w[1]-oy)*ex)/den,u=((w[0]-ox)*dy-(w[1]-oy)*dx)/den;if(t>0&&t<best&&u>=0&&u<=1)best=t}
      return best;
    }
    cv.addEventListener('click',function(e){var r=cv.getBoundingClientRect();goto=[Math.min(.93,Math.max(.07,(e.clientX-r.left-10)/(r.width-20))),Math.min(.93,Math.max(.1,(e.clientY-r.top-46)/(r.height-104)))];if(stEl)stEl.textContent='Verso il punto inviato'});
    function step(dt){
      var tgt=goto||route[wi],dx=tgt[0]-pos[0],dy=tgt[1]-pos[1],d=Math.hypot(dx,dy),v=.11*dt;
      if(d<.01){if(goto){goto=null;if(stEl)stEl.textContent='In ispezione'}else wi=(wi+1)%route.length}
      else{var a=Math.atan2(dy,dx),da=Math.atan2(Math.sin(a-head),Math.cos(a-head));head+=da*Math.min(1,dt*6);pos[0]+=Math.cos(head)*Math.min(v,d);pos[1]+=Math.sin(head)*Math.min(v,d)}
      bat=Math.max(18,bat-dt*.05);
    }
    function draw(now){
      var dt=last?Math.min(.05,(now-last)/1000):0;last=now;step(dt);
      var c=g.c,W=g.w,H=g.h,acc=css('--acc4')||'#4f7cff',acc3=css('--acc3')||'#ff7a59';
      c.clearRect(0,0,W,H);
      c.save();c.translate(10,46);c.scale((W-20)/W,(H-104)/H);
      c.fillStyle='rgba(255,255,255,.035)';c.fillRect(0,0,W,H);
      /* walls, faint: the map the robot is building */
      c.strokeStyle='rgba(255,255,255,.1)';c.lineWidth=1;walls.forEach(function(w){c.beginPath();c.moveTo(w[0]*W,w[1]*H);c.lineTo(w[2]*W,w[3]*H);c.stroke()});
      /* rays */
      var ox=pos[0],oy=pos[1];
      for(var k=0;k<48;k++){var a=head+(k/48)*Math.PI*2,r=ray(ox,oy,a,.28),hx=ox+Math.cos(a)*r,hy=oy+Math.sin(a)*r;
        c.strokeStyle='rgba(79,124,255,.12)';c.beginPath();c.moveTo(ox*W,oy*H);c.lineTo(hx*W,hy*H);c.stroke();
        if(r<.28&&Math.random()<.35){hits.push([hx,hy]);if(hits.length>2600)hits.shift()}}
      c.fillStyle=acc;hits.forEach(function(h){c.fillRect(h[0]*W-1,h[1]*H-1,1.6,1.6)});
      /* route */
      c.strokeStyle='rgba(255,255,255,.22)';c.setLineDash([3,5]);c.beginPath();route.forEach(function(p,i){i?c.lineTo(p[0]*W,p[1]*H):c.moveTo(p[0]*W,p[1]*H)});c.closePath();c.stroke();c.setLineDash([]);
      route.forEach(function(p,i){c.fillStyle=i===wi&&!goto?'#fff':'rgba(255,255,255,.4)';c.beginPath();c.arc(p[0]*W,p[1]*H,2.6,0,7);c.fill()});
      if(goto){c.strokeStyle=acc3;c.lineWidth=1.5;c.beginPath();c.arc(goto[0]*W,goto[1]*H,7+Math.sin(now/150)*2,0,7);c.stroke();c.beginPath();c.moveTo(ox*W,oy*H);c.lineTo(goto[0]*W,goto[1]*H);c.stroke()}
      /* robot */
      c.save();c.translate(ox*W,oy*H);c.rotate(head);c.fillStyle='#fff';c.beginPath();c.roundRect(-9,-5,18,10,3);c.fill();c.fillStyle=acc3;c.fillRect(6,-2,4,4);c.restore();
      c.restore();
      if(batEl)batEl.textContent=Math.round(bat)+'%';
      raf=requestAnimationFrame(draw);
    }
    function start(){if(slot.classList.contains('has-video'))return;g=fit(cv);if(RM){for(var i=0;i<200;i++)step(.05);draw(performance.now());cancelAnimationFrame(raf);raf=0;return}if(!raf){last=0;raf=requestAnimationFrame(draw)}}
    function stop(){cancelAnimationFrame(raf);raf=0}
    whenVisible(cv,start,stop);addEventListener('resize',function(){if(raf)g=fit(cv)});
  });

  /* One-prompt coding: typed terminal */
  document.querySelectorAll('[data-term]').forEach(function(pre){
    var L=[['p','> Prendi il pezzo dal vassoio e posalo nella maschera'],['d','  robot: Unitree G1-D · mano Dex3'],['d','  strumenti: visione, presa, traiettorie'],['o','✓ pezzo rilevato (0.97)'],['o','✓ traiettoria calcolata e verificata in simulazione'],['o','✓ codice pronto: pick_place_tray.py'],['p','> Ripeti per 20 pezzi e avvisami a fine ciclo']];
    var li=0,ci=0,html='',timer;
    function tick(){
      if(li>=L.length){timer=setTimeout(function(){li=0;ci=0;html='';pre.innerHTML='';tick()},2600);return}
      var l=L[li];ci++;
      var cur=html+'<span class="t-'+l[0]+'">'+esc(l[1].slice(0,ci))+'</span><i class="caret"></i>';
      pre.innerHTML=cur;
      if(ci>=l[1].length){html+='<span class="t-'+l[0]+'">'+esc(l[1])+'</span>\n';li++;ci=0;timer=setTimeout(tick,l[0]==='p'?700:260)}
      else timer=setTimeout(tick,l[0]==='p'?34:12);
    }
    if(RM){pre.innerHTML=L.map(function(l){return '<span class="t-'+l[0]+'">'+esc(l[1])+'</span>'}).join('\n');return}
    whenVisible(pre,function(){if(!timer)tick()},function(){clearTimeout(timer);timer=0});
  });

})();
