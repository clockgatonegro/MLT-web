import json,datetime
t=open('/home/claude/mlt/plantilla2.html').read()
F={f:open('/home/claude/mlt/salida/'+f,encoding='utf-8').read() for f in ['exposiciones.csv','agentes.csv','nodos.csv','aristas.csv']}
page=t.replace('/*DATA*/null',open('/home/claude/mlt/datos_web.json').read()).replace('/*FILES*/null',json.dumps(F,ensure_ascii=False))
open('/home/claude/mlt/redes-tertulia.html','w').write(page)
URL='https://mlt.cactus.com.co/'
GH='https://github.com/clockgatonegro/MLT-web'
DESC=('Red interactiva de 932 exposiciones y 3.574 artistas, curadores, presentadores y auspiciadores del Museo La Tertulia de Cali, '
      'de 1956 a 2026. Exposiciones individuales y colectivas, red de curadores y artistas por periodos, y bases de datos abiertas en CSV.')
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
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="Red del Museo La Tertulia">
<meta property="og:title" content="Red del Museo La Tertulia · Cali, 1956–2026">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Red de exposiciones y agentes del Museo La Tertulia">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Red del Museo La Tertulia · Cali, 1956–2026">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{URL}og-image.png">
<!-- Verificación de Google Search Console: pegue aquí la etiqueta que le entregue Search Console -->
<!-- <meta name="google-site-verification" content="CÓDIGO"> -->
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
open('/home/claude/mlt-web/index.html','w').write(head+page+'\n</body>\n</html>\n')
open('/home/claude/mlt-web/sitemap.xml','w').write(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{URL}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod><changefreq>yearly</changefreq><priority>1.0</priority></url>
</urlset>
''')
open('/home/claude/mlt-web/robots.txt','w').write(f'''User-agent: *
Allow: /

Sitemap: {URL}sitemap.xml
''')
