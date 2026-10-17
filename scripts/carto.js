// ---------- Cartografía: scrollytelling sobre la red (versión 3) ----------
(function(){
const host=document.getElementById('carto');if(!host)return;
const cv=document.getElementById('ccv'),ctx=cv.getContext('2d'),box=cv.parentElement;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const KEY=`${Y0}-${Y1}`,CM=COMM[KEY];
// conteos fijos
const nEx=new Uint16Array(N.length),nArt=new Uint16Array(N.length),mainRole=new Int8Array(N.length).fill(0);
AGENTS.forEach(a=>{nEx[a.i]=new Set(a.adj.map(k=>E[k].s)).size;const c=[0,0,0,0];a.adj.forEach(k=>c[E[k].r]++);mainRole[a.i]=c[1]?1:c[2]?2:c[0]?0:3});
EXPOS.forEach(x=>{nArt[x.i]=x.adj.filter(k=>E[k].r===0).length});
const byId=new Map(N.map(n=>[n.id,n])),byLab=l=>AGENTS.find(n=>n.label===l);
const ids=f=>new Set(N.filter(f).map(n=>n.i));
const nm=i=>esc(N[i].label);
const lista=a=>a.length>1?a.slice(0,-1).join(', ')+' y '+a[a.length-1]:a[0]||'';
// párrafos de los expedientes, tal como están escritos
function P(id,...k){const x=EXPS.find(e=>e.id===id);if(!x)return'';const d=document.createElement('div');d.innerHTML=x.body();const ps=[...d.querySelectorAll('p')];return k.map(j=>ps[j]?ps[j].outerHTML:'').join('').replace('como muestra el expediente anterior','como muestra el paso siguiente').replace('que describen los expedientes 03 y 05','que se vio en los actos anteriores').replace(' (tabla a la derecha)','').replace(/«Curadores → artistas»/g,'<span class="nw">«Curadores → artistas»</span>')}
function FIG(id){const x=EXPS.find(e=>e.id===id);return x?`<div class="fig">${x.fig()}</div>`:''}

// ---------- conjuntos para el relato ----------
const X15=byId.get('ex.77');
const x15A=X15?X15.adj.filter(k=>E[k].r===0).map(k=>E[k].t):[];
const BIEN=EXPOS.filter(n=>/Bienal Americana de Artes Gr/i.test(n.label)&&n.year).sort((a,b)=>a.year-b.year);
const B1=BIEN[0];
const bienSet=new Set(BIEN.map(n=>n.i));
const bienA=new Set();BIEN.forEach(x=>x.adj.forEach(k=>{if(E[k].r===0)bienA.add(E[k].t)}));
const bienOnce=new Set([...bienA].filter(t=>N[t].adj.every(k=>bienSet.has(E[k].s))));
const bienBack=new Set([...bienA].filter(t=>!bienOnce.has(t)));
const bienMulti=[...bienA].filter(t=>N[t].adj.filter(k=>bienSet.has(E[k].s)).length>=2);
const EV4=['Miguel González','Eduardo Serrano','Alberto Sierra','Álvaro Barrios'].map(byLab).filter(Boolean);
const curOf=(c,a,b)=>{const s=new Set();c.adj.forEach(k=>{if(E[k].r!==1&&E[k].r!==2)return;const x=N[E[k].s];if(a!=null&&(!x.year||x.year<a||x.year>b))return;x.adj.forEach(q=>{if(E[q].r===0&&E[q].t!==c.i)s.add(E[q].t)})});return s};
const curEx=c=>c.adj.filter(k=>E[k].r===1).map(k=>N[E[k].s]).filter(x=>x.year).sort((a,b)=>a.year-b.year);
const topBy=(set,f,k)=>[...set].sort((a,b)=>f(b)-f(a)).slice(0,k);
const inYears=(i,a,b)=>N[i].adj.some(k=>{const y=N[E[k].s].year;return y>=a&&y<=b});
const curPres=ids(n=>n.t>0&&n.adj.some(k=>E[k].r===1||E[k].r===2));
const mgA=MG?new Set(MG.adj.filter(k=>E[k].r===1).flatMap(k=>N[E[k].s].adj.filter(q=>E[q].r===0).map(q=>E[q].t))):new Set();
// artistas de 1982–2006 que ya habían expuesto en los quince años anteriores a alguna de sus exposiciones
const repe=new Set();AGENTS.forEach(a=>{const ys=a.adj.filter(k=>E[k].r===0).map(k=>N[E[k].s].year).filter(Boolean);if(ys.some(y=>y>=1982&&y<=2006&&ys.some(z=>z<y&&z>=y-15)))repe.add(a.i)});
const sponsorsIn=(a,b)=>{const c=new Map();EXPOS.forEach(x=>{if(!x.year||x.year<a||x.year>b)return;x.adj.forEach(k=>{if(E[k].r===3)c.set(E[k].t,(c.get(E[k].t)||0)+1)})});return [...c].sort((p,q)=>q[1]-p[1])};
const spEarly=sponsorsIn(1956,1979),spLate=sponsorsIn(1990,2009);
const spAll=ids(n=>n.t>0&&n.adj.some(k=>E[k].r===3));
const CAset=ids(n=>n.t>0&&isCA(n.i)&&inYears(n.i,2007,Y1));
const BT=((RAW.met[KEY]||{}).bt||[]).slice(0,10).map(r=>r[0]);
const K8=COMS();
const durSet=ids(n=>n.t===0&&n.dur!=null);
const commOf=k=>new Set([...CM].filter(([,c])=>c===k).map(([i])=>i));

// ---------- pasos ----------
const L=(o)=>`<a class="lk" href="red.html${hashOf(o)}">Abrir esta vista en la red →</a>`;
const S=[];
const step=o=>S.push(o);
step({act:'Antes de empezar',t:'Una exposición',mode:'expo',range:[1963,1963],only:['ex.77'],minEx:1,roles:[1,1,1,1],dist:95,charge:4,
  labels:()=>[X15.i,...x15A.slice(),...X15.adj.filter(k=>E[k].r>0).map(k=>E[k].t)],ring:X15?[X15.i]:[],
  html:()=>`<p>Empecemos por una sola exposición. En 1963 la casona de San Antonio recibió el ${esc(X15.label)}: ${x15A.length} artistas, una presentadora —Mireya Zawadzki— y un auspiciador, Taxader de Aviación.</p>
   <p>En esta red cada exposición es un cuadrado y cada persona o entidad que participó en ella es un círculo unido a él. El color dice qué hizo cada quien: <span class="nw"><span class="sw" style="--c:var(--artista)"></span>expuso,</span> <span class="nw"><span class="sw" style="--c:var(--curador)"></span>curó,</span> <span class="nw"><span class="sw" style="--c:var(--presentador)"></span>presentó,</span> <span class="nw"><span class="sw" style="--c:var(--apoyo)"></span>apoyó.</span></p>`,
  src:'Catálogo del XV Salón de Artistas Colombianos (1963); base de datos MLT 2016.',link:{view:'red',a:1963,b:1963,sel:'ex.77',mindeg:1,roles:[1,1,1,1]}});
step({act:'Acto 1 · El origen y la explosión',t:'Un club que expone',mode:'expo',range:[1956,1968],minEx:1,roles:[1,1,1,0],
  ring:X15?[X15.i]:[],hl:()=>new Set([X15.i,...x15A]),soft:true,
  labels:()=>[X15.i,...topBy(new Set(AGENTS.filter(a=>inYears(a.i,1956,1968)).map(a=>a.i)),i=>N[i].adj.filter(k=>{const y=N[E[k].s].year;return y<=1968}).length,7)],
  html:()=>{const back=x15A.filter(t=>N[t].adj.some(k=>E[k].s!==X15.i&&N[E[k].s].year<=1968)).length;
    return P('san-antonio',0,1)+`<p>De los ${x15A.length} artistas del XV Salón, ${back} exponen también en otras exposiciones de la casona. Por eso la exposición queda en el centro de esta primera red.</p>`+P('san-antonio',2)},
  link:{view:'red',a:1956,b:1968,mindeg:1}});
step({t:'La I Bienal',mode:'expo',range:[1956,1971],minEx:1,roles:[1,1,1,0],ring:B1?[B1.i]:[],hl:()=>new Set([B1.i,...B1.adj.map(k=>E[k].t)]),
  labels:()=>[B1.i,X15.i],html:()=>P('bienales',0),link:{view:'red',a:1969,b:1986,mindeg:1,sel:B1&&B1.id}});
step({t:'El estallido',mode:'expo',range:[1956,1986],minEx:1,roles:[1,1,1,0],ring:BIEN.filter(b=>b.year<=1986).map(b=>b.i),
  auto:false,labels:()=>BIEN.filter(b=>b.year<=1986).map(b=>b.i),softLab:()=>topBy(new Set(bienMulti),i=>N[i].adj.filter(k=>bienSet.has(E[k].s)).length,60),html:()=>P('bienales',1),link:{view:'red',a:1969,b:1986,mindeg:1}});
step({t:'Los que pasan una vez',mode:'expo',range:[1956,1986],minEx:1,roles:[1,1,1,0],hl:()=>new Set([...bienOnce,...bienSet]),
  labels:()=>BIEN.filter(b=>b.year<=1986).map(b=>b.i),html:()=>P('bienales',2),link:{view:'red',a:1969,b:1986,mindeg:1}});
step({t:'Los que vuelven',mode:'expo',range:[1956,Y1],minEx:2,roles:[1,1,1,0],hl:()=>bienBack,
  labels:()=>topBy(bienBack,i=>nEx[i],10),
  html:()=>{const v=[...bienBack],m=d3.mean(v,i=>nEx[i]),top=new Set(topBy(new Set(AGENTS.map(a=>a.i)),i=>nEx[i],100)),k=v.filter(i=>top.has(i)).length;
    return `<p>Los otros ${fmt(v.length)} artistas de las bienales sí vuelven. En promedio participan en ${dn(m,1)} exposiciones del Museo, y ${k} de ellos están entre los cien agentes con más exposiciones en setenta años.</p><p>Desde aquí la red muestra solo a quienes participaron en dos exposiciones o más.</p>`},
  link:{view:'red',a:Y0,b:Y1,mindeg:2}});
step({act:'Acto 2 · El cambio de poder',t:'Del presentador al curador',mode:'expo',range:[Y0,Y1],minEx:2,roles:[1,1,1,0],hl:()=>new Set([...curPres]),
  labels:()=>topBy(curPres,i=>N[i].adj.filter(k=>E[k].r===1||E[k].r===2).length,8),
  html:()=>P('presentador-curador',1,2)+FIG('presentador-curador'),link:{view:'pro',a:Y0,b:Y1,layout:'t'}});
step({t:'La exposición desaparece',mode:'pro',range:[Y0,Y1],minEx:2,
  labels:()=>topBy(new Set(curPres),i=>N[i].adj.filter(k=>E[k].r===1||E[k].r===2).length,6),
  html:()=>`<p>Ahora retiramos las exposiciones. Cada línea va directo de quien curó o presentó una exposición a cada artista que expuso en ella. Es la vista <span class="nw">«Curadores → artistas»</span>, la que permite ver la relación dinámica y simbiótica, que puede ser de colaboración profesional, diálogo intelectual o el impulso estratégico a la carrera de un artista. El curador se convierte en un intermediario clave en el sistema del arte.</p>`,link:{view:'pro',a:Y0,b:Y1}});
step({t:'El nodo mayor',mode:'pro',range:[1982,2006],minEx:2,hl:()=>new Set([MG.i,...mgA]),labels:()=>[MG.i],big:[MG.i],
  html:()=>P('miguel-gonzalez',0,2),link:{view:'pro',a:1993,b:2006,sel:MG&&MG.id}});
step({t:'Cuatro evangelistas',mode:'pro',range:[1977,2007],minEx:2,keep:new Set(EV4.map(n=>n.i)),auto:false,
  hl:()=>{const s=new Set(EV4.map(n=>n.i));EV4.slice(1).forEach(c=>{curOf(c).forEach(t=>s.add(t))});return s},
  labels:()=>{const mgS=curOf(EV4[0]),L=EV4.map(n=>n.i);EV4.slice(1).forEach(c=>curOf(c).forEach(t=>{if(mgS.has(t))L.push(t)}));return L.filter(i=>!/jes[uú]s mar[ií]a zamora|luis fernando pel[aá]ez/i.test(N[i].label))},right:/d[eé]bora arango/i,big:EV4.map(n=>n.i),fit:'focus',
  html:()=>{const [mg,...o]=EV4,mgS=curOf(mg),d=o.map(c=>{const ex=curEx(c),sh=[...curOf(c)].filter(t=>mgS.has(t));return {c,ex,sh}});
    const fr=d.map(({c,ex})=>`${esc(c.label)} curó ${ex.length===1?'una exposición':ex.length+' exposiciones'} (${ex.length?(ex[0].year===ex[ex.length-1].year?ex[0].year:ex[0].year+'–'+ex[ex.length-1].year):''})`);
    const sh=d.map(({c,sh})=>`${esc(c.label.split(' ').pop())}, ${sh.length}${sh.length?` (${sh.slice(0,4).map(nm).join(', ')}${sh.length>4?'…':''})`:''}`);
    const all3=d.length===3?[...curOf(d[0].c)].filter(t=>curOf(d[1].c).has(t)&&curOf(d[2].c).has(t)).length:0;
    const barr=byLab('Álvaro Barrios'),barrArt=barr?barr.adj.filter(k=>E[k].r===0).length:0;
    return P('miguel-gonzalez',1)+`<p>Los otros tres también pasan por el Museo: ${lista(fr)}.${barrArt?` Álvaro Barrios, además, expuso como artista en ${barrArt} ${barrArt===1?'exposición':'exposiciones'}.`:''} Los cruces con González se ven en los artistas que comparten: ${lista(sh)}.${all3?'':' Entre los tres no hay ningún artista en común.'}</p>`+P('miguel-gonzalez',3)},link:{view:'pro',a:1993,b:2006,sel:MG&&MG.id}});
step({t:'El círculo se cierra',mode:'pro',range:[1982,2006],minEx:2,hl:()=>repe,labels:()=>topBy(repe,i=>nEx[i],8),
  html:()=>{const D=CIRC(),Lr=D.dec.filter(x=>x.d>=1960);return P('circulacion',1)+`<div class="fig"><div class="cap">Artistas de cada década que ya habían expuesto en el Museo en los quince años anteriores (%)</div>${decBars([Lr.map(x=>x.rec)],Lr.map(x=>String(x.d).slice(2)),['var(--artista)'],' %')}</div>`},
  link:{view:'pro',a:1982,b:2006}});
step({act:'Acto 3 · La metamorfosis institucional',t:'Quién apoya',mode:'expo',range:[Y0,Y1],minEx:2,roles:[1,1,1,1],hl:()=>new Set(spAll),
  labels:()=>[...spEarly.slice(0,4).map(r=>r[0]),...spLate.slice(0,4).map(r=>r[0])],
  html:()=>{const per=[...spAll].filter(i=>N[i].t===1).length;return P('circulacion',2)+`<p>Colcultura, creada en 1968, se transformó en el Ministerio de Cultura en 1997, con la Ley General de Cultura (Ley 397); en la red son dos nodos distintos. En esta vista también aparecen ${per} personas que apoyaron o financiaron exposiciones: por eso hay nodos de artistas y de presentadores entre los auspiciadores.</p>`+`<div class="fig"><div class="cap">Auspiciadores por exposición, por década</div>${list(CIRC().dec.filter(x=>x.d>=1960&&x.d<=2000).map(x=>[`${x.d}–${String(x.d+9).slice(2)}`,dn(x.ap,2)]))}</div>`},
  link:{view:'red',a:Y0,b:Y1,roles:[0,0,0,1],layout:'t'}});
step({t:'Más tiempo, más inversión',mode:'expo',range:[Y0,Y1],minEx:2,roles:[1,1,1,0],size:'dur',hl:()=>durSet,
  labels:()=>topBy(durSet,i=>N[i].dur||0,4),html:()=>P('duracion',0,1)+FIG('duracion'),link:{view:'dur'}});
step({t:'Curadores que también exponen',mode:'pro',range:[2007,Y1],minEx:1,ca:true,hl:()=>CAset,auto:false,labels:()=>topBy(CAset,i=>N[i].adj.length,200),
  html:()=>P('expansion',0,1),link:{view:'pro',a:2007,b:2016,color:'rol'}});
step({t:'Los puentes',mode:'pro',range:[Y0,Y1],minEx:1,ca:true,hl:()=>new Set(BT),auto:false,labels:()=>BT,big:BT,
  html:()=>P('expansion',3),link:{view:'pro',a:Y0,b:Y1}});
step({act:'Acto 4 · Las comunidades',t:'Las islas',mode:'pro',range:[Y0,Y1],minEx:1,color:'com',
  labels:()=>K8.main.map(c=>c.cur[0][0]),html:()=>P('comunidades',0),link:{view:'pro',a:Y0,b:Y1,color:'com'}});
const PRO=build({mode:'pro',range:[Y0,Y1],minEx:1}),PDEG=new Map();PRO.links.forEach(l=>{PDEG.set(l.s,(PDEG.get(l.s)||0)+1);PDEG.set(l.t,(PDEG.get(l.t)||0)+1)});
const EXTRA=[/fresneda/i,/fajardo/i,/manuel lago/i,/powerpaola/i];
const rolTxt=i=>isCA(i)?'curador-artista':mainRole[i]===1?'curador':mainRole[i]===2?'presentador':mainRole[i]===3?'auspiciador':'artista';
K8.main.forEach((c,j)=>{const mem=commOf(c.k),ex=[...new Set([...mem].flatMap(i=>N[i].adj.map(k=>E[k].s)))];
  step({t:c.name,k:`Comunidad ${j+1} de ${K8.main.length} · ${c.a===c.b?c.a:c.a+'–'+c.b}`,mode:'pro',range:[Y0,Y1],minEx:1,color:'com',hl:()=>mem,fit:'focus',
    labels:()=>[...[...mem].filter(i=>EXTRA.some(r=>r.test(N[i].label))),...topBy(mem,i=>PDEG.get(i)||0,12)],big:c.cur.map(r=>r[0]),
    html:()=>(j===0?P('comunidades',1):'')+`<p>${fmt(c.n)} agentes. La sostienen ${lista(c.cur.map(([i])=>nm(i)))}, que curaron dentro de ella ${c.a===c.b?"en "+c.a:"entre "+c.a+" y "+c.b}. La exposición que más vínculos le aporta es «${esc(c.ex)}» (${c.y}).</p><div class="fig"><div class="cap">Los diez agentes con más vínculos en la comunidad (centralidad de grado)</div><table class="m"><tbody>${topBy(mem,i=>PDEG.get(i)||0,10).map(i=>`<tr><td>${nm(i)}</td><td>${rolTxt(i)}</td><td>${PDEG.get(i)||0}</td></tr>`).join('')}</tbody></table></div>`,
    link:{view:'pro',a:Y0,b:Y1,color:'com',com:c.k}})});
step({t:'Lo que el método no ve',mode:'pro',range:[Y0,Y1],minEx:1,color:'com',
  hl:()=>new Set(K8.single.flatMap(c=>[...commOf(c.k)])),labels:()=>K8.single.map(c=>topBy(commOf(c.k),i=>N[i].adj.length,1)[0]),
  html:()=>P('comunidades',2,3),link:{view:'pro',a:Y0,b:Y1,color:'com'}});
step({act:'Ahora usted',t:'Explore la red',mode:'pro',range:[Y0,Y1],minEx:1,final:true,
  labels:()=>topBy(new Set(AGENTS.map(a=>a.i)),i=>nEx[i],8),
  html:()=>`<p>Busque a una persona, una entidad o una exposición para verla en esta red, o abra la herramienta completa con todos los filtros.</p>
   <div class="csrch"><input id="cq" type="search" placeholder="Artista, curador, entidad…" autocomplete="off" aria-label="Buscar en la red"><ul id="cql"></ul></div>
   <p><a class="btn" href="red.html${hashOf({view:'red',a:Y0,b:Y1,roles:[1,1,1,1],mindeg:1})}">Explorar la red completa →</a></p>`});

// ---------- dibujo de las tarjetas ----------
const wrap=document.getElementById('csteps');
wrap.innerHTML=S.map((s,i)=>`<div class="cstep" data-i="${i}"><div class="card">${s.act?`<p class="act">${s.act}</p>`:''}<p class="k">${s.k||`${s.range[0]===s.range[1]?s.range[0]:s.range[0]+'–'+s.range[1]}`}</p><h3>${esc(s.t)}</h3>${s.html()}${s.src?`<p class="src">${s.src}</p>`:''}${s.link?L(s.link):''}</div></div>`).join('');

// ---------- simulación ----------
const SN=new Map();let cur=null,curG=null,F=null,LAB=[],RING=new Set(),BIG=new Set(),gdeg=new Map();
const rng=d3.randomLcg(0.4217);
const sim=d3.forceSimulation().randomSource(rng).force('link',d3.forceLink().distance(l=>cur&&cur.dist?cur.dist:cur&&cur.mode==='pro'?26:20).strength(l=>.5/Math.sqrt(Math.min(l.source.k||1,l.target.k||1))))
  .force('charge',d3.forceManyBody().strength(o=>(N[o.i].t===0?-28:-16)*(cur&&cur.charge||1)).distanceMax(320).theta(.95))
  .force('x',d3.forceX(0).strength(.05)).force('y',d3.forceY(0).strength(.05))
  .force('col',d3.forceCollide(o=>rad(o)+1).iterations(1)).alphaDecay(.028).velocityDecay(.38).stop();
function rad(o){const n=N[o.i];
  if(cur&&cur.size==='dur'&&n.t===0)return n.dur!=null?1.6+Math.sqrt(n.dur)*.5:1.3;
  if(n.t===0)return 2.2+Math.sqrt(nArt[o.i])*.75;
  if(BIG.has(o.i))return Math.max(9,cur&&cur.mode==='pro'?2+Math.sqrt(gdeg.get(o.i)||1)*1.1:2+Math.sqrt(nEx[o.i])*1.1);
  return cur&&cur.mode==='pro'?1.8+Math.sqrt(gdeg.get(o.i)||1)*1.05:1.7+Math.sqrt(Math.min(nEx[o.i],80))*1.05}
function build(st){
  const [a,b]=st.range,roles=st.roles||[1,1,1,0],minEx=st.minEx||1,ok=j=>nEx[j]>=minEx||(st.keep&&st.keep.has(j)),nodes=new Set(),links=[];
  if(st.mode==='expo'){
    const ex=st.only?st.only.map(id=>byId.get(id)).filter(Boolean):EXPOS.filter(x=>x.year&&x.year>=a&&x.year<=b);
    ex.forEach(x=>{let any=false;x.adj.forEach(k=>{const e=E[k];if(!roles[e.r]||!ok(e.t))return;any=true;nodes.add(e.t);links.push({s:x.i,t:e.t,r:e.r})});if(any||st.only)nodes.add(x.i)});
  }else{
    const w=new Map();EXPOS.forEach(x=>{if(!x.year||x.year<a||x.year>b)return;const R=rolesOf(x);R[1].concat(R[2]).forEach(c=>R[0].forEach(t=>{if(c===t||!ok(c)||!ok(t))return;const k=c*1e5+t;w.set(k,(w.get(k)||0)+1)}))});
    w.forEach((v,k)=>{const s=Math.floor(k/1e5),t=k%1e5;nodes.add(s);nodes.add(t);links.push({s,t,w:v,r:1})});
  }
  return {ids:[...nodes],links}}
function setStep(i){
  const st=S[i];if(!st||st===cur)return;cur=st;
  const g=build(st);curG=g;gdeg=new Map();g.links.forEach(l=>{gdeg.set(l.s,(gdeg.get(l.s)||0)+1);gdeg.set(l.t,(gdeg.get(l.t)||0)+1)});
  const keep=new Set(g.ids),adj=new Map();g.links.forEach(l=>{(adj.get(l.s)||adj.set(l.s,[]).get(l.s)).push(l.t);(adj.get(l.t)||adj.set(l.t,[]).get(l.t)).push(l.s)});
  SN.forEach(o=>{if(!keep.has(o.i))o.ta=0});
  const fresh=[];g.ids.forEach(i=>{let o=SN.get(i);if(!o||o.a<=0.01&&o.ta===0&&!o.live){o=o||{i,a:0};fresh.push(o);SN.set(i,o)}o.ta=1;o.live=true});
  const R0=Math.sqrt(g.ids.length)*9;
  for(let pass=0;pass<3;pass++)fresh.forEach(o=>{if(o.x!=null&&pass===0)return;const nb=(adj.get(o.i)||[]).map(j=>SN.get(j)).find(p=>p&&p.x!=null&&!fresh.includes(p)||p&&p.x!=null&&pass>0);
    if(nb){o.x=nb.x+(rng()-.5)*14;o.y=nb.y+(rng()-.5)*14}else if(pass===2||o.x==null&&pass===2){const a=rng()*6.283,r=R0*(.6+rng()*.6);o.x=Math.cos(a)*r;o.y=Math.sin(a)*r}});
  fresh.forEach(o=>{if(o.x==null){const a=rng()*6.283,r=R0*(.6+rng()*.6);o.x=Math.cos(a)*r;o.y=Math.sin(a)*r}});
  SN.forEach(o=>{if(!keep.has(o.i))o.live=false});
  g.ids.forEach(i=>{SN.get(i).k=gdeg.get(i)||1});
  sim.nodes(g.ids.map(i=>SN.get(i)));sim.force('link').links(g.links.map(l=>({source:SN.get(l.s),target:SN.get(l.t)})));
  F=st.hl?st.hl():null;LAB=st.labels?st.labels().filter(i=>i!=null):[];if(st.auto===false)AUTO=[];else autoLab(g.ids);if(st.softLab)AUTO=st.softLab();RING=new Set(st.ring||[]);BIG=new Set(st.big||[]);
  sim.force('col').radius(o=>rad(o)+1);
  sim.alpha(fresh.length>g.ids.length*.5?1:.55);
  if(RM){for(let k=0;k<260;k++)sim.tick();SN.forEach(o=>o.a=o.ta);camSnap=true}
  legend(st);document.getElementById('cyr').textContent=st.mode==='pro'?'Curadores → artistas':'Red de exposiciones';
  kick()}
// ---------- cámara y dibujo ----------
let AUTO=[],HOV=null;
function autoLab(idsv){const pool=idsv.filter(i=>!F||F.has(i)),mx=d3.max(pool,i=>gdeg.get(i)||0)||1;AUTO=pool.filter(i=>(gdeg.get(i)||0)>=.3*mx).sort((a,b)=>gdeg.get(b)-gdeg.get(a)).slice(0,40)}
let W=0,H=0,DPR=1,cam={x:0,y:0,k:1},camSnap=true,raf=0,vis=false,lastMove=0;
function size(){const r=box.getBoundingClientRect();DPR=devicePixelRatio||1;W=r.width;H=r.height;cv.width=Math.round(W*DPR);cv.height=Math.round(H*DPR);kick()}
new ResizeObserver(size).observe(box);
function target(){let pts=[];const useF=cur&&F&&(cur.fit==='focus'||!cur.soft&&F.size<sim.nodes().length*.5);
  sim.nodes().forEach(o=>{if(!useF||F.has(o.i))pts.push(o)});if(!pts.length)pts=sim.nodes();if(!pts.length)return cam;
  const xs=d3.extent(pts,o=>o.x),ys=d3.extent(pts,o=>o.y),pad=cur&&cur.only?120:40;
  const k=Math.max(.15,Math.min(cur&&cur.only?2.2:3.2,Math.min((W-pad)/((xs[1]-xs[0])||1),(H-pad-30)/((ys[1]-ys[0])||1))*.92));
  return {x:(xs[0]+xs[1])/2,y:(ys[0]+ys[1])/2,k}}
function kick(){if(!raf&&vis)raf=requestAnimationFrame(frame)}
function frame(now){raf=0;let busy=false;
  if(sim.alpha()>sim.alphaMin()){sim.tick();busy=true}
  SN.forEach((o,i)=>{const d=o.ta-o.a;if(Math.abs(d)>.01){o.a+=d*(RM?1:.12);busy=true}else{o.a=o.ta;if(o.ta===0&&!o.live)SN.delete(i)}});
  const t=target();if(camSnap){cam={...t};camSnap=false}else{const f=RM?1:.11;const dx=t.x-cam.x,dy=t.y-cam.y,dk=t.k-cam.k;
    if(Math.abs(dx)*cam.k>.5||Math.abs(dy)*cam.k>.5||Math.abs(dk)>.002){cam.x+=dx*f;cam.y+=dy*f;cam.k+=dk*f;busy=true}}
  draw();if(busy&&vis)raf=requestAnimationFrame(frame)}
const sx=x=>(x-cam.x)*cam.k+W/2,sy=y=>(y-cam.y)*cam.k+H/2+12;
function colorOf(o){const n=N[o.i];
  if(cur.color==='com'){const c=CM.get(o.i);return c!=null&&c<CAT.length?CAT[c]:C.mod[2]}
  if(n.t===0)return C.mod[n.mod];
  if(cur.ca&&isCA(o.i))return C.curart;
  if(cur.mode==='pro')return mainRole[o.i]===0?C.role[0]:C.role[mainRole[o.i]];
  return C.role[mainRole[o.i]]}
function rgba(hex,a){const m=/^#?([\da-f]{2})([\da-f]{2})([\da-f]{2})/i.exec(hex);return m?`rgba(${parseInt(m[1],16)},${parseInt(m[2],16)},${parseInt(m[3],16)},${a})`:hex}
function draw(){if(!cur)return;ctx.setTransform(DPR,0,0,DPR,0,0);ctx.clearRect(0,0,W,H);
  const k=cam.k,foc=o=>!F||F.has(o.i),dimA=cur.soft?.38:.07;
  // aristas
  const Ls=sim.force('link').links();ctx.lineWidth=Math.max(.35,.6*Math.min(1.6,k));
  ctx.strokeStyle=`rgba(${C.edge},${F?.05:cur.mode==='pro'?.16:.13})`;ctx.beginPath();
  for(const l of Ls){const a=l.source,b=l.target;if(F&&foc(a)&&foc(b))continue;const al=Math.min(a.a,b.a);if(al<.3)continue;ctx.moveTo(sx(a.x),sy(a.y));ctx.lineTo(sx(b.x),sy(b.y))}ctx.stroke();
  if(F){ctx.lineWidth=Math.max(.5,.8*Math.min(1.6,k));for(const l of Ls){const a=l.source,b=l.target;if(!(foc(a)&&foc(b)))continue;ctx.strokeStyle=rgba(colorOf(N[a.i].t===0?b:a),.45*Math.min(a.a,b.a));ctx.beginPath();ctx.moveTo(sx(a.x),sy(a.y));ctx.lineTo(sx(b.x),sy(b.y));ctx.stroke()}}
  // nodos (los que salen se desvanecen en su lugar)
  const all=[...SN.values()].sort((p,q)=>(foc(p)?1:0)-(foc(q)?1:0));
  for(const o of all){if(o.x==null)continue;const al=o.a*(foc(o)?1:dimA);if(al<.01)continue;const r=Math.max(1.1,rad(o)*Math.min(1.8,Math.max(.55,k)));
    ctx.globalAlpha=al;ctx.fillStyle=colorOf(o);ctx.beginPath();const X=sx(o.x),Y=sy(o.y);if(N[o.i].t===0)ctx.rect(X-r,Y-r,2*r,2*r);else ctx.arc(X,Y,r,0,7);ctx.fill();
    if(RING.has(o.i)){ctx.globalAlpha=o.a;ctx.strokeStyle=C.fg;ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(X,Y,r+5,0,7);ctx.stroke()}}
  ctx.globalAlpha=1;
  // rótulos sin superposición
  ctx.font='12px "IBM Plex Sans",sans-serif';ctx.textBaseline='middle';const boxes=[];
  const LL=[...new Set([...LAB,...AUTO])];
  const labSet=new Set(LAB);
  for(const i of LL){if(i===HOV)continue;const o=SN.get(i);if(!o||o.a<.4||o.x==null)continue;const r=rad(o)*Math.min(1.8,Math.max(.55,k)),cx=sx(o.x),cy=sy(o.y);
    if(cx<-20||cx>W+20||cy<0||cy>H)continue;const bold=BIG.has(i)||RING.has(i);ctx.font=(bold?'600 ':'')+'12px "IBM Plex Sans",sans-serif';
    const s=N[i].label.length>44?N[i].label.slice(0,42)+'…':N[i].label,w=ctx.measureText(s).width;
    const cand=cur.right&&cur.right.test(N[i].label)?[[cx+r+4,cy,'left']]:[[cx+r+4,cy,'left'],[cx-r-4,cy,'right'],[cx,cy-r-9,'center'],[cx,cy+r+10,'center']];let pick=null,first=null;
    for(const [x,y,al] of cand){const x0=al==='left'?x:al==='right'?x-w:x-w/2,bx=[x0-2,y-8,x0+w+2,y+8];if(x0<4||x0+w>W-4||y<14||y>H-6)continue;if(!first)first=[x,y,al,bx];
      if(!boxes.some(q=>!(bx[2]<q[0]||bx[0]>q[2]||bx[3]<q[1]||bx[1]>q[3]))){pick=[x,y,al,bx];break}}
    if(!pick){if(!labSet.has(i)||!first)continue;pick=first}
    boxes.push(pick[3]);ctx.textAlign=pick[2];ctx.globalAlpha=o.a;ctx.lineWidth=3.5;ctx.strokeStyle=C.bg;ctx.strokeText(s,pick[0],pick[1]);ctx.fillStyle=C.fg;ctx.fillText(s,pick[0],pick[1])}
  ctx.textAlign='left';ctx.font='12px "IBM Plex Sans",sans-serif';
  if(HOV!=null&&SN.has(HOV)){const o=SN.get(HOV),n=N[HOV],r=rad(o)*Math.min(1.8,Math.max(.55,k)),X=sx(o.x),Y=sy(o.y);
    ctx.globalAlpha=.8;ctx.lineWidth=1.2;ctx.strokeStyle=C.fg;for(const l of Ls){if(l.source.i!==HOV&&l.target.i!==HOV)continue;const q=l.source.i===HOV?l.target:l.source;ctx.beginPath();ctx.moveTo(X,Y);ctx.lineTo(sx(q.x),sy(q.y));ctx.stroke()}
    ctx.globalAlpha=1;ctx.beginPath();ctx.arc(X,Y,r+4,0,7);ctx.stroke();
    const s=n.label,sub=n.t===0?`${n.year||''} · ${nArt[HOV]} artistas`:`${nEx[HOV]} ${nEx[HOV]===1?'exposición':'exposiciones'} · ${gdeg.get(HOV)||0} vínculos aquí`;
    ctx.font='600 13px "IBM Plex Sans",sans-serif';const w1=ctx.measureText(s).width;ctx.font='11px "IBM Plex Mono",monospace';const w2=ctx.measureText(sub).width;
    const bw=Math.max(w1,w2)+16,bh=40;let bx=X+r+8,by=Y-bh/2;if(bx+bw>W-4)bx=X-r-8-bw;bx=Math.max(4,Math.min(W-bw-4,bx));by=Math.max(4,Math.min(H-bh-4,by));
    ctx.fillStyle=C.bg;ctx.globalAlpha=.94;ctx.fillRect(bx,by,bw,bh);ctx.globalAlpha=1;ctx.strokeStyle=C.line;ctx.lineWidth=1;ctx.strokeRect(bx+.5,by+.5,bw-1,bh-1);
    ctx.fillStyle=C.fg;ctx.font='600 13px "IBM Plex Sans",sans-serif';ctx.fillText(s,bx+8,by+13);ctx.fillStyle=C.muted;ctx.font='11px "IBM Plex Mono",monospace';ctx.fillText(sub,bx+8,by+29)}
  ctx.globalAlpha=1}
function legend(st){const it=[];
  if(st.color==='com')it.push(['var(--muted)','Color: comunidad (Louvain)']);
  else{if(st.mode==='expo')it.push(['var(--ind)','Individual','sq'],['var(--col)','Colectiva','sq']);
    it.push(['var(--artista)','Artista']);if(st.ca)it.push(['var(--curart)','Curador-artista']);it.push(['var(--curador)','Curador'],['var(--presentador)','Presentador']);
    if((st.roles||[])[3])it.push(['var(--apoyo)','Auspiciador'])}
  document.getElementById('cleg').innerHTML=it.map(([c,l,s])=>`<span><i class="${s||''}" style="background:${c}"></i>${l}</span>`).join('')}
// ---------- buscador del cierre ----------
host.addEventListener('input',ev=>{if(ev.target.id!=='cq')return;const r=qFind(ev.target.value).filter(n=>SN.has(n.i)||n.t===0).slice(0,8);
  document.getElementById('cql').innerHTML=r.map(n=>`<li><button data-i="${n.i}">${esc(n.label)}</button></li>`).join('')});
host.addEventListener('click',ev=>{const b=ev.target.closest('#cql button');if(!b)return;const i=+b.dataset.i,n=N[i];
  let set;if(n.t===0)set=new Set([i,...n.adj.map(k=>E[k].t)]);else{set=new Set([i]);sim.force('link').links().forEach(l=>{if(l.source.i===i)set.add(l.target.i);if(l.target.i===i)set.add(l.source.i)})}
  F=set;LAB=[i,...topBy(set,j=>N[j].adj.length,8)];autoLab(sim.nodes().map(o=>o.i));BIG=new Set([i]);if(!SN.has(i)&&n.t===0){location.href='red.html'+hashOf({view:'red',a:n.year||Y0,b:n.year||Y1,sel:n.id,mindeg:1});return}
  cur={...cur,fit:'focus'};kick()});
// ---------- red de fondo de la portada ----------
(function(){const hc=document.getElementById('herocv');if(!hc)return;const hx=hc.getContext('2d');
  const ids=new Set(),hl=[];EXPOS.forEach(x=>x.adj.forEach(k=>{const e=E[k];if(e.r===3||nEx[e.t]<2)return;ids.add(x.i);ids.add(e.t);hl.push([x.i,e.t])}));
  const r2=d3.randomLcg(0.77),hn=[...ids].map(i=>{const a=r2()*6.283,r=200*Math.sqrt(r2());return {i,x:Math.cos(a)*r,y:Math.sin(a)*r}}),hm=new Map(hn.map(o=>[o.i,o])),hk=hl.map(([a,b])=>({source:hm.get(a),target:hm.get(b)}));
  const hs=d3.forceSimulation(hn).randomSource(r2).force('link',d3.forceLink(hk).distance(16).strength(.35)).force('charge',d3.forceManyBody().strength(-9).distanceMax(220).theta(.95))
    .force('x',d3.forceX(0).strength(.06)).force('y',d3.forceY(0).strength(.06)).alphaDecay(.012).alphaTarget(.015).velocityDecay(.5).stop();
  let on=true,t0=0;
  function fr(now){if(!on)return;hs.tick();const R=hc.getBoundingClientRect(),d=devicePixelRatio||1;if(!R.width){requestAnimationFrame(fr);return}
    if(hc.width!==Math.round(R.width*d)){hc.width=Math.round(R.width*d);hc.height=Math.round(R.height*d)}
    const xs=d3.extent(hn,o=>o.x),ys=d3.extent(hn,o=>o.y),k=Math.min(R.width*(R.width>900?.55:.95)/(xs[1]-xs[0]||1),R.height*.9/(ys[1]-ys[0]||1));
    hx.setTransform(d,0,0,d,0,0);hx.clearRect(0,0,R.width,R.height);hx.save();hx.translate(R.width*(R.width>900?.66:.5),R.height*.46);hx.scale(k,k);hx.translate(-(xs[0]+xs[1])/2,-(ys[0]+ys[1])/2);
    hx.lineWidth=.5/k;hx.strokeStyle=`rgba(${C.edge},.08)`;hx.beginPath();for(const l of hk){hx.moveTo(l.source.x,l.source.y);hx.lineTo(l.target.x,l.target.y)}hx.stroke();
    hx.globalAlpha=.6;for(const o of hn){const n=N[o.i],r=(n.t===0?1.6+Math.sqrt(nArt[o.i])*.5:1.2+Math.sqrt(Math.min(nEx[o.i],60))*.55);hx.fillStyle=n.t===0?C.mod[n.mod]:C.role[mainRole[o.i]];hx.beginPath();if(n.t===0)hx.rect(o.x-r,o.y-r,2*r,2*r);else hx.arc(o.x,o.y,r,0,7);hx.fill()}
    hx.restore();hx.globalAlpha=1;if(!RM)requestAnimationFrame(fr)}
  if(RM){for(let i=0;i<300;i++)hs.tick()}
  new IntersectionObserver(es=>{const v=es[0].isIntersecting;if(v&&!on){on=true;requestAnimationFrame(fr)}else if(!v)on=false}).observe(hc);requestAnimationFrame(fr)})();
// ---------- scroll ----------
const STEPS=[...document.querySelectorAll('.cstep')];let sraf=0,act=-1;
function pickStep(){sraf=0;const t=innerHeight*.62;let k=0;STEPS.forEach((el,i)=>{if(el.firstElementChild.getBoundingClientRect().top<t)k=i});
  if(k!==act){act=k;STEPS.forEach((el,i)=>el.classList.toggle('on',i===k));setStep(k)}}
addEventListener('scroll',()=>{if(!sraf)sraf=requestAnimationFrame(pickStep)},{passive:true});addEventListener('resize',pickStep);
// cursor: revela nombres; clic abre la ficha en la red completa
cv.addEventListener('pointermove',ev=>{const r=cv.getBoundingClientRect(),mx=ev.clientX-r.left,my=ev.clientY-r.top;let best=null,bd=144;
  sim.nodes().forEach(o=>{if(o.a<.5||F&&!F.has(o.i)&&!cur.soft)return;const dx=sx(o.x)-mx,dy=sy(o.y)-my,d=dx*dx+dy*dy;if(d<bd){bd=d;best=o.i}});
  if(best!==HOV){HOV=best;cv.style.cursor=best!=null?'pointer':'';if(!raf)draw()}});
cv.addEventListener('pointerleave',()=>{HOV=null;if(!raf)draw()});
cv.addEventListener('click',()=>{if(HOV==null)return;const n=N[HOV];location.href='red.html'+hashOf({view:cur.mode==='pro'&&n.t>0?'pro':'red',a:cur.range[0],b:cur.range[1],sel:n.id,mindeg:1})});
new IntersectionObserver(es=>{vis=es[0].isIntersecting;if(vis)kick()}).observe(box);
addEventListener('mlt-theme',kick);
act=0;STEPS[0].classList.add('on');setStep(0);size();pickStep();
})();
