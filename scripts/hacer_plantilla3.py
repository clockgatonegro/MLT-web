# Genera plantilla3.html (versión 3.0, de prueba) a partir de plantilla2.html sin modificarla.
import re
s=open('/home/claude/mlt/plantilla2.html',encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]);s=s.replace(a,b)
# colores: curadores en el naranja de los presentadores; presentadores en amarillo pálido
# paleta v3 (a partir de los colores que propuso Carlos): claro / oscuro
for a,b in [('--ind:#1b9a9a;','--ind:#005d71;'),('--col:#e2725b;','--col:#ff6b59;'),('--artista:#4f9a2c;','--artista:#1a983f;'),('--curador:#c8323c;','--curador:#e69500;'),('--presentador:#e08a1e;','--presentador:#c9b04a;'),('--apoyo:#7a5fc0;','--apoyo:#464c89;'),('--curart:#8a4fb8;','--curart:#dd4d88;')]:
    R(a,b)
for a,b in [('--ind:#3cc2c0;','--ind:#3aa6bd;'),('--col:#f08a72;','--col:#ff6b59;'),('--artista:#7cc552;','--artista:#3fbf62;'),('--curador:#ef5a62;','--curador:#ffa600;'),('--presentador:#f2a443;','--presentador:#ece08c;'),('--apoyo:#a08ae0;','--apoyo:#8e94d8;'),('--curart:#b980e6;','--curart:#ef6fa3;')]:
    R(a,b,2)
# CSS de páginas y de la cartografía
R('html:not(.pg-metodo) #metodo{display:none}','''html:not(.pg-metodo) #metodo{display:none}
html:not(.pg-red) #explorar{display:none}html.pg-red #inicio,html.pg-red main,html.pg-red #carto{display:none}html.pg-red #explorar{display:grid}
html.pg-metodo #carto{display:none}#expedientes{display:none}
.hero .lede3{font:400 clamp(18px,2.2vw,23px)/1.45 var(--f-body);max-width:46ch;margin:14px 0 22px}
.carto{display:grid;grid-template-columns:minmax(300px,390px) minmax(0,1fr);gap:0 36px;max-width:1360px;margin:0 auto;padding:0 16px}
.carto-g{grid-column:2;grid-row:1;position:sticky;top:var(--navh,48px);height:calc(100vh - var(--navh,48px));height:calc(100svh - var(--navh,48px))}
.carto-g canvas{width:100%;height:100%;display:block;touch-action:pan-y}
.carto-yr{position:absolute;left:12px;top:10px;font:500 11px var(--f-data);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.carto-leg{position:absolute;left:12px;bottom:10px;display:flex;flex-wrap:wrap;gap:4px 12px;font-size:12px;color:var(--muted);max-width:90%}
.carto-leg i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px}.carto-leg i.sq{border-radius:1px}
.carto-steps{grid-column:1;grid-row:1;padding:34vh 0 50vh}
.cstep{min-height:92vh;display:flex;align-items:center}
.cstep .card{padding:6px 0;opacity:.22;transition:opacity .45s}
.cstep.on .card{opacity:1}
.card .act{font:600 11px var(--f-data);letter-spacing:.1em;text-transform:uppercase;color:var(--fg);margin:0 0 10px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.card .k{font:500 11px var(--f-data);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}
.card h3{font:700 22px/1.15 var(--f-display);margin:2px 0 10px;text-wrap:balance}
.card p{margin:0 0 12px;line-height:1.6;font-size:16px}
.card .src{font-size:12px;color:var(--muted)}
.card .lk{display:inline-block;margin-top:6px;font-size:13px;color:var(--muted)}.card .lk:hover{color:var(--fg)}
.card .nw{white-space:nowrap}.card table.m{width:100%;border-collapse:collapse;font-size:13px}.card table.m td{padding:2px 0;border-bottom:1px dotted var(--line)}.card table.m td:nth-child(2){color:var(--muted);font-size:12px}.card table.m td:last-child{text-align:right;font:12px var(--f-data);color:var(--muted)}
.card .sw{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--c);margin:0 4px 0 2px;vertical-align:-1px}
.card .fig{background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:10px 12px;margin:8px 0 10px}
.card .fig .cap{font-size:12px;color:var(--muted);margin:2px 0 8px}.card .fig .big{font:700 30px/1 var(--f-display)}
.card .fig ol,.card .fig ul{margin:0;padding:0;list-style:none;font-size:13px}
.card .fig li{display:flex;gap:8px;justify-content:space-between;border-bottom:1px dotted var(--line);padding:3px 0}
.card .fig li span:last-child{font:12px var(--f-data);color:var(--muted)}
.card .fig svg{width:100%;height:auto;display:block}.card .fig svg text{fill:var(--muted);font:10px var(--f-data)}
.csrch input{width:100%;box-sizing:border-box;font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--fg)}
.csrch ul{list-style:none;margin:6px 0 10px;padding:0}.csrch button{all:unset;cursor:pointer;display:block;padding:4px 2px;font-size:14px;border-bottom:1px dotted var(--line);width:100%}
.csrch button:hover{color:var(--curador)}
@media (max-width:860px){.carto{display:block;padding:0}.carto-g{position:sticky;top:var(--navh,48px);height:54vh;height:54svh;z-index:0;background:var(--bg)}
 .carto-steps{position:relative;z-index:1;padding:4vh 12px 30vh}.cstep{min-height:80vh;align-items:flex-end}.cstep .card{opacity:0;padding:14px 4px}.cstep.on .card{opacity:1;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(3px)}}
''')
# navegación
R('''  <a href="#expedientes">Expedientes</a>
  <a href="#quien">Quién conecta</a>
  <a href="#explorar">Explorar la red</a>''','''  <a href="./#carto">Cartografía</a>
  <a href="./#quien">Quién conecta</a>
  <a href="red.html" class="pgr">Explorar la red</a>''')
# portada: título, entradilla y un solo llamado
i=s.index('    <p class="lede">Setenta años');j=s.index('  </div>\n</header>',i)
s=s[:i]+'''    <p class="lede3">Un viaje interactivo por las redes que se formaron durante 70 años de exposiciones: quién expuso, quién curó, quién presentó y con quién coincidió. Cada exposición une a las personas que la hicieron posible. Juntas dibujan la historia de un museo y de la circulación del arte de la ciudad.</p>
    <div class="nums" id="nums"></div>
    <div class="cta"><a class="btn" href="#carto">Empezar el recorrido ↓</a><a class="btn ghost" href="red.html">Explorar la red</a></div>
'''+s[j:]
R('<p class="eyebrow">Cali · <span class="yrs">1956–2026</span></p>','<p class="eyebrow">Cartografía · Cali · <span class="yrs">1956–2026</span></p>')
# sección de cartografía antes de los expedientes
R('<main>\n<section class="s wrap" id="expedientes">','''<section id="carto" class="carto" aria-label="Cartografía de la red">
  <div class="carto-g"><canvas id="ccv" role="img" aria-label="Red de exposiciones y agentes del Museo La Tertulia que cambia con el relato"></canvas><div class="carto-yr" id="cyr"></div><div class="carto-leg" id="cleg"></div></div>
  <div class="carto-steps" id="csteps"></div>
</section>
<main>
<section class="s wrap" id="expedientes">''')
# perbar ya no existe en la portada
R("{const box=document.getElementById('perbar');","{const box=document.getElementById('perbar')||document.createElement('div');")
# título del expediente 07
R("t:'Quién vuelve y quién paga'","t:'Quién vuelve y quién apoya'")
# fuera de red.html, los botones y el índice abren red.html con el estado
R("function explore(o,scroll=true){\n","function explore(o,scroll=true){\n  if(!document.documentElement.classList.contains('pg-red')){location.href='red.html'+hashOf(o);return}\n")
# aviso de pantalla grande: solo en red.html; en la cartografía el relato funciona en el celular
R("{const mv=document.getElementById('movil');let seen=null;","{const mv=document.documentElement.classList.contains('pg-red')?document.getElementById('movil'):document.createElement('div');let seen=null;")
R("La red completa se explora mejor en un computador. En el celular puede leer los expedientes y el índice.","La red completa se explora mejor en un computador. En el celular puede seguir el recorrido de la cartografía y el índice.")
# la portada de la v3 dibuja su propia red de fondo (carto.js)
R("heroN=VN.slice();heroE=VE.slice();drawHero();setTimeout(()=>{heroLive=false;drawHero()},9000);","")
# Método con el ritmo pausado del recorrido: bloques con aire, una sola columna de lectura y aparición al hacer scroll
R('html.pg-metodo #metodo{padding-top:24px}','''html.pg-metodo #metodo{padding-top:24px}
html.pg-metodo #metodo>.lede{margin-bottom:6vh}
html.pg-metodo #metodo .estr2{margin:4vh 0 14vh}
html.pg-metodo #metodo .mh{margin-top:0;padding-top:16px}
html.pg-metodo #metodo .dgs,html.pg-metodo #metodo .arq-n{margin-bottom:14vh}
html.pg-metodo #metodo .cols2{display:block;max-width:72ch}
html.pg-metodo #metodo .cols2 h3{margin-top:9vh;padding-top:14px;border-top:1px solid var(--line)}
html.pg-metodo #metodo .cols2>div:first-child>h3:first-child{margin-top:0}
html.pg-metodo #metodo .ask{margin-top:12vh}
html.pg-metodo .rv{opacity:0;transform:translateY(28px);transition:opacity .7s ease,transform .7s ease}
html.pg-metodo .rv.vis{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html.pg-metodo .rv{opacity:1;transform:none;transition:none}}''')
REVEAL='''<script>(function(){if(!document.documentElement.classList.contains('pg-metodo')||!('IntersectionObserver' in window))return;
 const M=document.getElementById('metodo');if(!M)return;
 const T=[...M.querySelectorAll(':scope>.lede,:scope>.estr2>figure,:scope>.mh,:scope>.dgs>figure,:scope>.arq-l,:scope>.arq,:scope>.arq-n,.cols2>div>*,:scope>.ask')];
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}}),{rootMargin:'0px 0px -12% 0px'});
 T.forEach(el=>{el.classList.add('rv');const p=el.parentElement;if(p.classList.contains('dgs')||p.classList.contains('estr2'))el.style.transitionDelay=(0.12*[...p.children].indexOf(el))+'s';io.observe(el)});
})();</script>
'''
# altura de la barra de navegación para el gráfico fijo
s=s.replace('</body>','</body>')
s+='\n'+REVEAL+'<script>(function(){const n=document.querySelector(".nav");const f=()=>document.documentElement.style.setProperty("--navh",n.offsetHeight+"px");f();addEventListener("resize",f)})();</script>\n<script>\n'+open('/home/claude/mlt/carto.js',encoding='utf-8').read()+'\n</script>\n'
open('/home/claude/mlt/plantilla3.html','w',encoding='utf-8').write(s)
print('plantilla3 ok')
