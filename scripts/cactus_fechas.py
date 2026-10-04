"""Correcciones y adiciones a partir de las piezas gráficas diseñadas por Cactus Taller Gráfico para el
Museo La Tertulia (carpeta 'Museo La Tertulia/04 Originales'). Cada cambio cita el archivo de origen.
Se ejecuta después de complemento_2016_2026.py y antes de normalizar.py."""
import csv, os
F = os.path.join(os.path.dirname(__file__), 'salida', 'exposiciones_2016_2026.csv')
rows = list(csv.DictReader(open(F, encoding='utf-8')))
cols = list(rows[0].keys()) + [c for c in ('modalidad', 'pieza_cactus') if c not in rows[0]]
by = {r['nombre_expo']: r for r in rows}

# nombre -> cambios (solo campos que dicen las piezas) + archivo de origen
P = {
 "Karen Lamassonne. Desnuda astucia del deseo": dict(fecha_fin="2017-11-19", curadores="Andrés Matute Echeverri", confianza="alta",
    pieza_cactus="EXPOSICIONES 2017/Karen Lamassone/Piezas/Camisetas.ai; EXPOSICIONES 2017/Carlos Amorales/Piezas/Programa de mano"),
 "Carlos Amorales. Herramientas de trabajo": dict(espacio="Sala Subterránea", fecha_ini="2017-12-15",
    pieza_cactus="EXPOSICIONES 2017/Carlos Amorales/Piezas", notas="Las piezas anuncian cierre el 1 de abril y, en otra versión, el 19 de junio de 2018 (posible prórroga)"),
 "¡Oído Pueblo! Ritmo y economía en Cali": dict(fecha_fin="2018-06-10", curadores="Ericka Flórez Hidalgo, Alejandro Martín Maldonado",
    pieza_cactus="EXPOSICIONES 2017/Oido pueblo/Piezas/Programa de mano", notas="Una pieza temprana dice 'hasta el 3 de marzo'; la posterior, 10 de junio de 2018. Alejandro Martín figura como curador del Museo"),
 "En Cauce": dict(pieza_cactus="EXPOSICIONES 2017/En Cauce (invitación, inauguración 14 dic. 2017)", confianza="alta"),
 "Costurero Viajero": dict(fecha_ini="2018-02-14", fecha_fin="2018-04-26", apoyan_auspicia="Universidad Icesi", confianza="alta",
    pieza_cactus="Exposiciones 2018/Costutero viajero", notas=""),
 "Savia Solaris": dict(curadores="Ximena Gama", pieza_cactus="Exposiciones 2018/Programa C/CAROLINA CHARRY/Invitación"),
 "Augusto Rivera, el gran ausente": dict(espacio="Sala Subterránea", apoyan_auspicia="Universidad del Valle",
    pieza_cactus="Exposiciones 2018/Antonio Dorado", notas="Inferencia: la pieza de la carpeta 'Antonio Dorado' (instalación, 10–19 oct. 2018, Sala Subterránea, Univalle) coincide en fechas; Antonio Dorado figura en 'concepción y dirección'"),
 "Abandonen toda esperanza": dict(pieza_cactus="Exposiciones 2018/Abandonen Toda Esperanza"),
 "EOCL": dict(fecha_ini="2018-07-12", espacio="", apoyan_auspicia="Lugar a Dudas", confianza="alta",
    pieza_cactus="Exposiciones 2018/BLOC (invitación, jueves 12 de julio)", notas="BLOC; la fecha de la web (2022) era de publicación"),
 "Allá nos veremos, sin sombra y sin faz": dict(pieza_cactus="Exposiciones 2018/Adriana Ciudad"),
 "El carácter de la tradición en la arquitectura de Barney, Távora, Coderch": dict(fecha_ini="2019-05-09", fecha_fin="2019-07",
    curadores="Andrés Felipe Erazo Barco, Antonio Armesto Aira, Manuel Augusto Mendes Soares", confianza="alta",
    pieza_cactus="Exposiciones 2019/El Carácter de la Tradición; Exposiciones 2018/Sticker programación/MAYO",
    notas="Curadores: autores de la propuesta itinerante; las piezas anuncian 'conferencias con los curadores'"),
 "Srape Pøtø Tul-yu. El último círculo": dict(fecha_ini="2019", fecha_fin="2019-07", pieza_cactus="Exposiciones 2018/Sticker programación/MAYO ('hasta julio 2019')"),
 "La obra arquitectónica de Le Corbusier": dict(fecha_ini="2019", fecha_fin="2019-06", espacio="Jardines del museo", confianza="media",
    pieza_cactus="Exposiciones 2018/Sticker programación/MAYO ('hasta junio 2019')", notas="Fundación Le Corbusier; 17 obras patrimonio Unesco"),
 "Exposición ganadores BLOC 2018": dict(fecha_ini="2019-07-11", espacio="Sala Subterránea, Sala Alterna", curadores="Éricka Flórez, Johan Samboní",
    confianza="alta", pieza_cactus="Exposiciones 2019/Bloc 2019/INVITACION GANADORES BLOC",
    notas="Herlyng Ferla (Sala Subterránea, cur. Éricka Flórez) y Vanessa Ortiz (Sala Alterna, cur. Johan Samboní)"),
 "La unión que separa las cosas. BLOC 2018": dict(fecha_ini="2019-04-25", espacio="Sala Subterránea", artistas="Esteban López, Christian Velásquez",
    confianza="media", pieza_cactus="Exposiciones 2019/Bloc 2019; Banner 2019/Bloc 2019",
    notas="Muestra de finalistas; la lista de nombres en la pieza está cortada. Reabre el 22 de junio de 2019 en el segundo piso"),
 "Manglaria. Raíces, vínculos y sujeciones": dict(fecha_ini="2019-08-15", espacio="Casa Obeso Mejía", artistas="Fabio Melecio Palacios, Henry Salazar",
    apoyan_auspicia="Semillero de Investigación Litoralidades", confianza="alta", pieza_cactus="Exposiciones 2019/Manglaria"),
 "El Testigo": dict(fecha_ini="2019-09", fecha_fin="2020-03-01", espacio="Edificio de la Colección", confianza="alta",
    pieza_cactus="Exposiciones 2019/Luz de memoria/EL TESTIGO", notas="Temporada 'Luz para la memoria'"),
 "Bifurcaciones. Trayectos y cruces de una generación": dict(fecha_ini="2019-09", espacio="Sala Maritza Uribe de Urdinola", confianza="media",
    pieza_cactus="Exposiciones 2019/Luz de memoria/Museo de puertas abiertas", modalidad="colectiva"),
 "Fractales": dict(fecha_ini="2019-09", espacio="Sala Alterna", confianza="alta", pieza_cactus="Exposiciones 2019/Luz de memoria"),
 "Voces para transformar a Colombia": dict(pieza_cactus="Exposiciones 2019/Luz de memoria/VOCES", modalidad="colectiva"),
 "Sala Abierta. Acciones para la memoria y la reconciliación": dict(fecha_ini="2019-11", fecha_fin="2020-03", confianza="media",
    pieza_cactus="Exposiciones 2019/SALA ABIERTA Arte, memoria y reconciliación"),
 "El ruido del silencio": dict(curadores="Adriana Castellanos Olmedo", pieza_cactus="Exposiciones 2019/Programa C"),
 "Casa Ocupada. La colección cruza el puente": dict(fecha_ini="2019-12-17", confianza="alta", modalidad="colectiva",
    pieza_cactus="CUADERNILLO PROGRAMACION/PROGRAMACIÓN DIC 2019"),
 "María Thereza Negreiros y 16 mujeres artistas de su generación": dict(curadores="Miguel González", confianza="alta", modalidad="colectiva",
    pieza_cactus="2020/EXPOSICIONES 2020/Maria Thereza Negreiros",
    notas="Inauguración virtual 24 mar. 2020 (#MuseoEnCasa); otra pieza anuncia cóctel en el Club Campestre de Cali, 18 dic. 2020, curaduría Miguel González"),
 "La escuela del desencanto": dict(curadores="Luz Adriana Hoyos", pieza_cactus="2020/EXPOSICIONES 2020/Programa C/Catalina Jaramillo",
    notas="Inauguración prevista el 24 mar. 2020; se realizó el 10 oct. 2020. Programa C de Celsia"),
 "Manual de instrucciones": dict(espacio="Edificio de la Colección, primer piso", apoyan_auspicia="Secretaría de Cultura de Cali", confianza="media",
    pieza_cactus="2020/EXPOSICIONES 2020/Manual de instrucciones", notas="Estímulos Cali 2020"),
 "Manolo Lago. El entusiasmo de una idea": dict(espacio="Casa Obeso Mejía", pieza_cactus="2020/EXPOSICIONES 2020/Manolo Lago/Marca Manolo Lago.ai",
    notas="La invitación anuncia inauguración el 25 abr. 2020 en la Casa Obeso Mejía; la web la publica en nov. 2021 (inferencia: aplazada por la pandemia)"),
 "Amanecer. BLOC 2020": dict(fecha_ini="2021-01", fecha_fin="2021-03", confianza="alta", pieza_cactus="2021/Exposiciones 2021/Amanecer - Sala Alterna/Folleto"),
 "El ataque del presente contra el resto de los tiempos": dict(fecha_fin="2021-04-18", curadores="Alejandro Martín",
    pieza_cactus="2021/Exposiciones 2021/El ataque de los tiempos"),
 "VI Salón BAT de Arte Popular": dict(fecha_fin="2021-07-04", confianza="alta", modalidad="colectiva", pieza_cactus="2021/Salón BAT - Arte Popular"),
}
# modalidad para exposiciones colectivas cuyos artistas no están nombrados
COLECTIVAS = ["(El otro lado de la) Carretera al mar", "World Press Photo 2018", "Reserva abierta. ¿Por fin Cali sabrá lo que tiene?",
 "21 obras en el cambio de tiempo", "Wildlife Photographer of the Year", "VII Salón BAT de Arte Popular. Colombia y el medio ambiente",
 "Transición. Cuarto Salón de Arte Contemporáneo del Pacífico", "Museo + Escuela. Muestra de proyectos 2022-2023", "Exposición de Museo + Escuela",
 "Hacer ver. Provocar el archivo, agitar el museo", "Ingeniería de la visión", "Ensayos para un mundo perfecto. Salón de Arte BBVA. Nuevos nombres",
 "El mundo entero es una Bauhaus", "Subterránea 2020", "Gráfica Subterránea", "Sigo esperando", "Aula Flexible. Sala Taller"]

NEW = [
 dict(nombre_expo="La Escena. Sala didáctica", fecha_ini="2017-01-28", espacio="Sala Subterránea", tipo="sala didáctica", confianza="media",
      pieza_cactus="EXPOSICIONES 2017/LA ESCENA sala sub", notas="Fecha = apertura"),
 dict(nombre_expo="Breyner Huertas. XVI Salón Regional de Artistas, Zona Pacífico", fecha_ini="2017-07-19", fecha_fin="2017-09-03", espacio="Sala Alterna",
      artistas="Breyner Huertas", curadores="Miguel González", apoyan_auspicia="Ministerio de Cultura", tipo="presencial", confianza="alta",
      pieza_cactus="EXPOSICIONES 2017/Breyner - Salón Regional", notas="Beca para exposición individual del XVI Salón Regional; el título exacto no aparece en las piezas", modalidad="individual"),
 dict(nombre_expo="Radiar memorias. Diálogos con el Carare", fecha_ini="2017-08-21", fecha_fin="2017-09-14", espacio="Casa Obeso Mejía",
      artistas="Fundación Sub/Liminal", apoyan_auspicia="Centro Nacional de Memoria Histórica", tipo="laboratorio", confianza="alta",
      pieza_cactus="EXPOSICIONES 2017/Radiar Memorias - Casa Obeso", notas="Beca de proyectos museográficos en memoria histórica 2016"),
 dict(nombre_expo="Revelar la mirada. Sala didáctica Karen Lamassonne", fecha_ini="2017-08", fecha_fin="2017-11-18", espacio="Sala Subterránea",
      artistas="Karen Lamassonne", tipo="sala didáctica", confianza="media", pieza_cactus="Banners 2017/Boletín profesore"),
 dict(nombre_expo="El Río suena. Temporada de laboratorios", fecha_ini="2017-12-14", fecha_fin="2018-01-14", espacio="Jardines del museo",
      tipo="laboratorio", confianza="media", pieza_cactus="EXPOSICIONES 2017/El Río suena", notas="Laboratorios a cargo de Juan López y Alejandro Villegas Pabón"),
 dict(nombre_expo="Joint Venture. Museo Popular de Siloé en el Museo La Tertulia", fecha_ini="2018-07-28", fecha_fin="2018-09-30",
      espacio="Sala Jugar al Museo, primer piso de la colección", artistas="Museo Popular de Siloé", tipo="comunitaria", confianza="alta",
      pieza_cactus="Exposiciones 2018/Museo Popular de Siloé"),
]

for n, ch in P.items():
    r = by.get(n)
    if not r: print('NO ENCONTRADA:', n); continue
    for k, v in ch.items():
        if k == 'notas' and r.get('notas') and v: r[k] = (r[k] + '. ' + v) if v not in r[k] else r[k]
        else: r[k] = v
    if r['fecha_ini']: r['ano'] = r['fecha_ini'][:4]
for n in COLECTIVAS:
    if n in by: by[n]['modalidad'] = 'colectiva'
    else: print('NO ENCONTRADA (col):', n)
last = max(int(r['id_expo'][3:]) for r in rows)
for i, d in enumerate(NEW, 1):
    r = {c: '' for c in cols}; r.update(d); r['id_expo'] = f'ex.{last+i}'; r['ano'] = r['fecha_ini'][:4]
    r['fuente_url'] = ''; rows.append(r)
with open(F, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, '') for c in cols})
print(len(rows), 'filas;', sum(1 for r in rows if r.get('pieza_cactus')), 'con pieza de Cactus')
