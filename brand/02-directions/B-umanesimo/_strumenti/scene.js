// Scala la "a montata" a scena: node scene.js k X Y [colori json]
const {circle,rect,band,lens}=require('./geo.js');
function scene(k,X,Y,c={hook:'#E2A93B',bowl:'#BB3B26',stem:'#24211E',win:'#F3EEE3'},stemBottom){
  const T=(x,y)=>[x*k+X,y*k+Y];
  const [hx,hy]=T(84,256),[bx,by]=T(77,327),[s0]=T(128,0),[s1]=T(180,0);
  const sb=stemBottom??(400*k+Y);
  return `<path fill="${c.hook}" d="${band(hx,hy,96*k,44*k,150,0)}"/>`+
  `<path fill="${c.bowl}" d="${circle(bx,by,77*k)}"/>`+
  `<path fill="${c.stem}" d="${rect(s0,hy,s1-s0,sb-hy)}"/>`+
  `<path fill="${c.win}" d="${lens(bx,by,77*k,s0,s1)}"/>`;
}
module.exports=scene;
if(require.main===module){const a=process.argv.slice(2);console.log(scene(+a[0],+a[1],+a[2],a[3]?JSON.parse(a[3]):undefined,a[4]?+a[4]:undefined));}
