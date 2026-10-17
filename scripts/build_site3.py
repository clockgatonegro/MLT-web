import json,datetime
import subprocess;subprocess.run(['python3','/home/claude/mlt/hacer_plantilla3.py'],check=True)
t=open('/home/claude/mlt/plantilla3.html').read()
import os;os.makedirs('/home/claude/v3build',exist_ok=True)
F={f:open('/home/claude/mlt/salida/'+f,encoding='utf-8').read() for f in ['exposiciones.csv','agentes.csv','nodos.csv','aristas.csv']}
page=t.replace('/*DATA*/null',open('/home/claude/mlt/datos_web.json').read()).replace('/*FILES*/null',json.dumps(F,ensure_ascii=False))
open('/home/claude/mlt/redes-tertulia-v3.html','w').write(page)
URL='https://mlt.cactus.com.co/v3/'
GH='https://github.com/clockgatonegro/MLT-web'
import csv as _c
_na=sum(1 for _ in _c.DictReader(open('/home/claude/mlt/salida/agentes.csv')));_ne=sum(1 for _ in _c.DictReader(open('/home/claude/mlt/salida/exposiciones.csv')))
DESC=(f'Red interactiva de {_ne} exposiciones y {_na:,}'.replace(',','.')+' artistas, curadores y auspiciadores del Museo La Tertulia de Cali, 1956–2026. Datos abiertos.')
ld={"@context":"https://schema.org","@type":"Dataset","name":"Red del Museo La Tertulia, Cali (1956–2026)",
 "description":DESC,"url":URL,"sameAs":GH,"inLanguage":"es","isAccessibleForFree":True,
 "creator":[{"@type":"Person","name":"Juan Fernando Correa"},{"@type":"Person","name":"Carlos Dussán"}],
 "temporalCoverage":"1956/2026","spatialCoverage":{"@type":"Place","name":"Cali, Colombia"},
 "about":{"@type":"Museum","name":"Museo La Tertulia","address":{"@type":"PostalAddress","addressLocality":"Cali","addressCountry":"CO"}},
 "keywords":["Museo La Tertulia","Cali","arte colombiano","exposiciones","curadores","artistas","análisis de redes","humanidades digitales","historia del arte"],
 "distribution":[{"@type":"DataDownload","encodingFormat":"text/csv","name":f,"contentUrl":f"https://raw.githubusercontent.com/clockgatonegro/MLT-web/master/data/{f}"} for f in F],
 "dateModified":datetime.date.today().isoformat()}
head=f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{DESC}">
<meta name="author" content="Juan Fernando Correa, Carlos Dussán">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="Red del Museo La Tertulia">
<meta property="og:title" content="Red del Museo La Tertulia · Cali, 1956–2026">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://mlt.cactus.com.co/og-mlt-2026.jpg">
<meta property="og:image:secure_url" content="https://mlt.cactus.com.co/og-mlt-2026.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Red de exposiciones y agentes del Museo La Tertulia">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Red del Museo La Tertulia · Cali, 1956–2026">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://mlt.cactus.com.co/og-mlt-2026.jpg">
<!-- Verificación de Google Search Console: pegue aquí la etiqueta que le entregue Search Console -->
<!-- <meta name="google-site-verification" content="CÓDIGO"> -->
<!-- Google Analytics 4 con modo de consentimiento: sin cookies hasta que la persona acepte -->
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
var _c=null;try{{_c=localStorage.getItem('mlt_consent')}}catch(e){{}}
gtag('consent','default',{{analytics_storage:_c==='si'?'granted':'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}});
gtag('js',new Date());gtag('config','G-SYWHRKMC3T',{{anonymize_ip:true}});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-SYWHRKMC3T"></script>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#141b19">
<link rel="sitemap" type="application/xml" href="{URL}sitemap.xml">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<style>[hidden]{{display:none!important}}body{{margin:0}}</style>
</head>
<body>
<noscript><main style="padding:16px;max-width:65ch;font-family:sans-serif">
<h1>Red del Museo La Tertulia · Cali, 1956–2026</h1>
<p>{DESC}</p>
<p>Proyecto <em>Cartografiar redes del arte. 60 años del Museo La Tertulia</em>. Juan Fernando Correa y Carlos Dussán.</p>
<p>Esta visualización necesita JavaScript. Las bases de datos están en <a href="{GH}/tree/master/data">{GH}/tree/master/data</a>.</p>
</main></noscript>
'''
BANNER='<div id="ck" hidden style="position:fixed;left:16px;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));max-width:560px;margin:0 auto;z-index:50;background:#1b2422;color:#eef0ec;font:13px/1.45 \'IBM Plex Sans\',Arial,sans-serif;padding:12px 14px;border-radius:6px;display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;box-shadow:0 4px 18px rgba(0,0,0,.25)">\n<span style="flex:1 1 260px">Usamos Google Analytics para saber cómo se usa esta visualización. Las cookies de medición solo se activan si las acepta.</span>\n<span style="display:flex;gap:8px"><button id="ck-no" style="font:inherit;background:transparent;color:inherit;border:1px solid #93a39e;border-radius:4px;padding:4px 10px;cursor:pointer">Rechazar</button><button id="ck-si" style="font:inherit;background:#eef0ec;color:#1b2422;border:0;border-radius:4px;padding:5px 12px;cursor:pointer;font-weight:600">Aceptar</button></span>\n</div>\n<script>\n(function(){var b=document.getElementById(\'ck\'),c=null;try{c=localStorage.getItem(\'mlt_consent\')}catch(e){}\nif(!c)b.hidden=false;\nfunction set(v){try{localStorage.setItem(\'mlt_consent\',v)}catch(e){}if(v===\'si\')gtag(\'consent\',\'update\',{analytics_storage:\'granted\'});b.hidden=true}\ndocument.getElementById(\'ck-si\').onclick=function(){set(\'si\')};document.getElementById(\'ck-no\').onclick=function(){set(\'no\')};})();\n</script>\n'
open('/home/claude/v3build/index.html','w').write(head+page+BANNER+'\n</body>\n</html>\n')
# página aparte: Método y fuentes (mismo documento; una clase en <html> muestra solo esa sección)
def metodo(pg,hd):
    pg=pg.replace('<title>Red del Museo La Tertulia · Cali, 1956–2026</title>','<title>Método y fuentes · Red del Museo La Tertulia</title><script>document.documentElement.classList.add("pg-metodo")</script>',1)
    pg=pg.replace('<a href="metodo.html" class="pgm">','<a href="metodo.html" class="pgm" aria-current="true">',1)
    hd=hd.replace(f'<link rel="canonical" href="{URL}">',f'<link rel="canonical" href="{URL}metodo.html">')
    return hd,pg
_h,_p=metodo(page,head)
open('/home/claude/v3build/metodo.html','w').write(_h+_p+BANNER+'\n</body>\n</html>\n')
def red(pg,hd):
    pg=pg.replace('<title>Red del Museo La Tertulia · Cali, 1956–2026</title>','<title>Explorar la red · Red del Museo La Tertulia</title><script>document.documentElement.classList.add("pg-red")</script>',1)
    pg=pg.replace('<a href="red.html" class="pgr">','<a href="red.html" class="pgr" aria-current="true">',1)
    return hd.replace(f'<link rel="canonical" href="{URL}">',f'<link rel="canonical" href="{URL}red.html">'),pg
_h,_p=red(page,head)
open('/home/claude/v3build/red.html','w').write(_h+_p+BANNER+'\n</body>\n</html>\n')
print('v3 ok')
