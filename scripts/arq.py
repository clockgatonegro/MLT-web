# Inserta en Método y fuentes la arquitectura de datos (después de «Cuatro medidas para leer la red»)
p='/home/claude/mlt/plantilla2.html';s=open(p,encoding='utf-8').read()
if 'id="arq"' in s: raise SystemExit('ya está')
T={ # clave: (título, usada en la red, csv, campos [(texto, clave de campo o None, sangría)])
 'inst':('Instituciones',1,'agentes.csv · organización',[('id de la institución','id'),('nombre de la institución',),('año de constitución',),('año de cierre',),('financiación',),('sectores',),('id de imagen del logo',),('país',)]),
 'obras':('Obras',0,'fuera de esta red',[('id de la obra','id'),('código del registro',),('nombre del artista',),('id de persona','per'),('título de la obra',),('descripción textual',),('clase espacial',),('diámetro',),('ancho',),('largo',),('alto',),('área',),('volumen',),('año de creación',),('año de adquisición',),('tiraje',),('número de copia',),('técnica registrada',),('técnica GCAI',),('materiales',),('movimiento artístico',),('id de imagen',)]),
 'expo':('Exposiciones',1,'exposiciones.csv · aristas.csv',[('id de la exposición','id'),('nombre de la exposición',),('descripción de la exposición',),('autor del texto',),('id del documento','doc'),('id de otros documentos','doc2'),('mes de inicio',),('día de inicio',),('año de finalización',),('mes de finalización',),('día de finalización',),('fecha de inicio',),('fecha de finalización',),('duración en días',),('artistas',),('id de persona','art',1),('curadores',),('id de persona','cur',1),('presentadores',),('id de persona','pre',1),('nombre del espacio',),('id de espacio','esp',1),('obras',),('id de la obra','obra',1),('instituciones involucradas',),('id de las instituciones','inst',1),('id de imagen',)]),
 'esp':('Espacios',1,'columnas espacio y sede',[('id de espacio','id'),('sede',),('sala',),('nombre corto',),('latitud',),('longitud',),('id de imagen',)]),
 'docs':('Documentos',0,'fuera de esta red',[('id del documento','id'),('nombre del documento',),('año de creación',),('mes de creación',),('diseño de la edición',),('impresor',),('tipología Cedoc',),('formato de publicación',),('archivo .txt',),('ruta .txt',),('signatura física',),('id de imagen',)]),
 'pers':('Personas',1,'agentes.csv · persona',[('id de persona','id'),('nombre de registro',),('nombre',),('apellido',),('seudónimo',),('año de nacimiento',),('año de muerte',),('sexo',),('nacionalidad',),('país de nacimiento',),('ciudad de nacimiento',),('ocupaciones',),('id de imagen',)]),
}
# vínculos: (tabla.campo origen, tabla.campo destino)
LK=[('inst.id','expo.inst'),('obras.id','expo.obra'),('obras.per','pers.id'),('expo.doc','docs.id'),('expo.doc2','docs.id'),('expo.art','pers.id'),('expo.cur','pers.id'),('expo.pre','pers.id'),('esp.id','expo.esp')]
dest={}
for a,b in LK:
    for x,y in ((a,b),(b,a)):
        if not x.endswith('.id'): dest[x]=T[y.split('.')[0]][0]
def tabla(k):
    t,uso,csv,F=T[k]
    li=[]
    for f in F:
        txt=f[0];key=f[1] if len(f)>1 else None;ind=len(f)>2
        fk=f'{k}.{key}' if key else ''
        cls=' '.join(c for c in ['pk' if key=='id' else '','fk' if key and key!='id' else '','in' if ind else ''] if c)
        tag=f'<i>→ {dest[fk]}</i>' if fk in dest else ''
        li.append(f'<li{f" data-k=\"{fk}\"" if fk else ""}{f" class=\"{cls}\"" if cls else ""}>{txt}{tag}</li>')
    return f'<div class="tb tb-{k}{"" if uso else " off"}" data-t="{k}"><b>{t}</b><span class="csv">{csv}</span><ul>{"".join(li)}</ul></div>'
html=f'''
  <h3 class="mh" id="arq-h">Arquitectura de datos</h3>
  <p class="arq-l">La base de datos MLT de 2016 se organizó en seis tablas relacionadas por sus identificadores, con las exposiciones en el centro. Esta red usa cuatro: exposiciones, personas, instituciones y espacios. Obras y documentos, en gris, siguen en la base de datos pero no hacen parte de esta visualización. Los datos abiertos aplanan esa estructura en archivos CSV: cada exposición en <code>exposiciones.csv</code>, cada persona o institución en <code>agentes.csv</code> y cada vínculo, con su rol, en <code>aristas.csv</code>.</p>
  <div class="arq" id="arq"><svg class="arq-ln" aria-hidden="true"></svg>{"".join(tabla(k) for k in ['inst','obras','expo','esp','docs','pers'])}</div>
  <p class="hint arq-n">Las líneas unen cada identificador con la tabla de la que viene. Pase el cursor por un campo para ver sus vínculos.</p>
'''
a='  </div>\n  <div class="cols2">'
assert s.count(a)==1
s=s.replace(a,'  </div>'+html+'  <div class="cols2">')
css='''.arq{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-areas:"inst expo docs" "obras expo pers" "obras esp pers";gap:28px 64px;margin:14px 0 8px;align-items:start}
.arq-ln{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.arq-ln path{fill:none;stroke:var(--muted);stroke-width:1;opacity:.55;transition:opacity .2s,stroke .2s}.arq-ln path.off{stroke-dasharray:3 3;opacity:.35}.arq-ln path.hi{stroke:var(--fg);opacity:1;stroke-width:1.6}
.tb{position:relative;z-index:1;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:0 0 8px;font-size:13px}
.tb>b{display:inline-block;background:var(--fg);color:var(--bg);font:700 15px var(--f-display);padding:3px 8px;margin:-1px 0 0 -1px;border-radius:4px 0 4px 0}
.tb .csv{display:block;font:500 10.5px var(--f-data);letter-spacing:.04em;color:var(--muted);padding:6px 10px 4px}
.tb ul{list-style:none;margin:0;padding:0 10px}.tb li{padding:1.5px 0;line-height:1.35;color:var(--fg)}.tb li.in{padding-left:12px}
.tb li.pk,.tb li.fk{font-family:var(--f-data);font-size:12px;font-weight:600}.tb li.fk{cursor:default}.tb li.hi{color:var(--curador)}
.tb li i{display:none;font-style:normal;font-weight:400;color:var(--muted);margin-left:6px}
.tb.off{opacity:.62}.tb.off>b{background:var(--muted)}
.tb-inst{grid-area:inst}.tb-obras{grid-area:obras}.tb-expo{grid-area:expo}.tb-esp{grid-area:esp}.tb-docs{grid-area:docs}.tb-pers{grid-area:pers}
.arq-l{max-width:70ch}
@media (max-width:860px){.arq{grid-template-columns:1fr;grid-template-areas:"expo" "pers" "inst" "esp" "obras" "docs";gap:14px}.arq-ln{display:none}.tb li i{display:inline}.arq-n{display:none}}
'''
a2='.estr{margin:18px 0 6px}'
assert s.count(a2)==1
s=s.replace(a2,css+a2)
js=r'''<script>
(function(){const A=document.getElementById('arq');if(!A)return;const sv=A.querySelector('.arq-ln');
const LK=__LK__;
function draw(){if(getComputedStyle(sv).display==='none')return;const R=A.getBoundingClientRect();let g='';
  LK.forEach(([a,b],n)=>{const ea=A.querySelector(`[data-k="${a}"]`),eb=A.querySelector(`[data-k="${b}"]`);if(!ea||!eb)return;
    const ra=ea.getBoundingClientRect(),rb=eb.getBoundingClientRect(),ta=ea.closest('.tb').getBoundingClientRect(),tb=eb.closest('.tb').getBoundingClientRect();
    const right=tb.left>ta.left+5,ya=ra.top+ra.height/2-R.top,yb=rb.top+rb.height/2-R.top;
    let xa,xb;if(Math.abs(tb.left-ta.left)<5){xa=ta.right-R.left;xb=tb.right-R.left;const d=40;g+=`<path data-n="${n}" d="M${xa},${ya}C${xa+d},${ya} ${xb+d},${yb} ${xb},${yb}"/>`;return}
    xa=(right?ta.right:ta.left)-R.left;xb=(right?tb.left:tb.right)-R.left;const m=(xa+xb)/2;
    const off=ea.closest('.tb').classList.contains('off')||eb.closest('.tb').classList.contains('off');
    g+=`<path data-n="${n}"${off?' class="off"':''} d="M${xa},${ya}C${m},${ya} ${m},${yb} ${xb},${yb}"/>`});
  sv.innerHTML=g}
new ResizeObserver(draw).observe(A);if(document.fonts)document.fonts.ready.then(draw);addEventListener('load',draw);
A.addEventListener('mouseover',ev=>{const li=ev.target.closest('li[data-k]');A.querySelectorAll('.hi').forEach(e=>e.classList.remove('hi'));if(!li)return;const k=li.dataset.k;
  LK.forEach(([a,b],n)=>{if(a===k||b===k){const p=sv.querySelector(`[data-n="${n}"]`);if(p)p.classList.add('hi');[a,b].forEach(x=>{const e=A.querySelector(`[data-k="${x}"]`);if(e)e.classList.add('hi')})}})});
A.addEventListener('mouseleave',()=>A.querySelectorAll('.hi').forEach(e=>e.classList.remove('hi')));
})();
</script>
'''.replace('__LK__',str([list(x) for x in LK]).replace("'",'"'))
s=s+js
open(p,'w',encoding='utf-8').write(s);print('ok')
