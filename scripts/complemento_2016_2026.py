"""Exposiciones del Museo La Tertulia posteriores a la base 07/2016, transcritas desde capturas
del Archivo de Internet (web.archive.org) y la web actual. Solo se registran datos que aparecen
explícitamente en la página citada. confianza: alta = fechas y agentes explícitos; media = fecha o
agentes parciales; baja = solo título en un listado (año = año de la captura, inferido)."""
import csv, os
W = 'https://web.archive.org/web/{}/https://museolatertulia.com{}'
V = 'https://www.museolatertulia.co/#exposiciones'
COM, ORG = W, 'https://web.archive.org/web/{}/http://museolatertulia.org{}'
L1 = W.format('20220119', '/category/exposiciones/')
L2 = W.format('20230120', '/category/exposiciones/page/2/')

R = [
# (nombre, ini, fin, espacio, artistas, curadores, apoyo, tipo, confianza, fuente, notas)
("Artist Talking Back to the Media", "2016-11-11", "2016-11-14", "Casa Obeso Mejía", "", "", "LIMA; De Appel", "presencial", "media", ORG.format('20161115', '/exposicion/artist-talking-back-to-the-media'), "Ausente en la base 07/2016"),
("Universo Holograma", "2017-03-30", "2017-07-16", "Sala Maritza Uribe de Urdinola, Sala Subterránea", "Benoit Pype, Bernardo Oritz, Carlos Motta, François Bucher, Fabien Giraud, Raphael Siboni, John Mario Ortiz, Julien Prévieux, Kader Attia, Laurent Grasso", "", "", "presencial", "media", W.format('20171229', '/museo/exposiciones/universo-holograma'), "Lista de artistas truncada en la captura; 'Oritz' tal como aparece"),
("Casa Liminal", "2017-06-22", "2017-08-05", "Casa Obeso Mejía", "Erick Beltrán", "Lina López", "", "presencial", "alta", W.format('20180510', '/museo/exposiciones/casa-liminal'), ""),
("Karen Lamassonne. Desnuda astucia del deseo", "2017-08-10", "", "Sala Maritza Uribe de Urdinola", "Karen Lamassonne", "", "", "presencial", "media", W.format('20170917', '/museo/exposiciones/desnuda-astucia'), "Fecha = inauguración"),
("La guerra que no hemos visto. Un proyecto de memoria histórica", "", "", "", "", "", "", "presencial", "baja", W.format('20170911', '/museo/exposiciones/la-guerra-que-no-hemos-visto-un-proyecto-de-memoria-historica'), "Sin fechas en la captura (sept. 2017)"),
("El mundo según Mafalda", "2017-10-05", "2017-11-05", "Casa Obeso Mejía", "", "", "Barrilete", "presencial", "media", W.format('20171006', '/museo/exposiciones/el-mundo-segun-mafalda'), ""),
("Es arriba es abajo", "2017-10-19", "2018-01-14", "", "Mariángela Aponte", "", "", "presencial", "alta", W.format('20171102', '/museo/exposiciones/es-arriba-es-abajo'), ""),
("Jugar al museo. Un museo dentro del museo", "2017-11-25", "2018-09", "", "", "", "", "sala didáctica", "media", W.format('20171221', '/museo/exposiciones/jugar-al-museo-museo-dentro-del-museo'), ""),
("Carlos Amorales. Herramientas de trabajo", "2017-12-14", "2018-04-01", "", "Carlos Amorales", "", "", "presencial", "alta", W.format('20171220', '/museo/exposiciones/carlos-amorales-herramientas-trabajo'), ""),
("¡Oído Pueblo! Ritmo y economía en Cali", "2017-12-14", "2018-04-01", "Edificio de la Colección, segundo piso", "Julio Giraldo, Luis Ospina, Carlos Mayolo, Camila Rodríguez, Lina Hincapié, Breyner Huertas, Mónica Restrepo, Felipe Leal, Carolina Charry, Vanessa Ortiz, Carolina Torres, Carolina Navas, Nois Radio", "Ericka Flórez Hidalgo", "", "presencial", "alta", W.format('20180210', '/museo/exposiciones/oido-pueblo'), ""),
("En Cauce", "2017-12-14", "2018-01-14", "Jardines del museo", "", "Alberto Campuzano, Lorena Díez", "Celsia", "espacio público", "media", W.format('20171209', '/museo/exposiciones/en-cauce-programa-c-de-celsia'), "Programa C de Celsia"),
("Costurero Viajero", "2018-02-13", "2018-03-20", "Casa Obeso Mejía", "Artesanal Tecnológica", "", "", "presencial", "media", W.format('20180218', '/museo/exposiciones/costurero-viajero'), "Encabezado dice 2017; el texto dice 2018"),
("No todos los amores de Platón fueron imposibles", "2018-03-08", "2018-05", "", "Sonnia Yepez", "", "", "presencial", "alta", W.format('20180320', '/museo/exposiciones/no-todos-los-amores-platon-fueron-imposibles-sonnia-yepez'), ""),
("De frente me escondo. Powerpaola", "2018-05-05", "2018-07-15", "Sala Maritza Uribe de Urdinola", "Powerpaola", "Andrés Fresneda, Juan Pablo Fajardo, Alejandro Martín", "", "presencial", "alta", W.format('20180511', '/museo/exposiciones/frente-me-escondo-power-paola'), ""),
("(El otro lado de la) Carretera al mar", "2018-08-09", "2018-11-12", "Sala Maritza Uribe de Urdinola", "", "Equipo Museo La Tertulia", "", "presencial", "alta", W.format('20181009', '/museo/exposiciones/lado-la-carretera-al-mar'), "Artistas: 'varios'"),
("Allá nos veremos, sin sombra y sin faz", "2018-08-14", "2018-09-30", "Sala Subterránea", "Adriana Ciudad, Nidia Góngora, C. S. Prince", "", "", "presencial", "alta", W.format('20181010', '/museo/exposiciones/alla-nos-veremos-sin-sombra-sin-faz'), "Proyecto Alabaos"),
("Las populares Gráficas Molinari", "2018-09-01", "2019-02", "", "Gráficas Molinari", "", "", "presencial", "media", W.format('20181023', '/museo/exposiciones/las-populares-graficas-molinari'), ""),
("Savia Solaris", "2018-09-01", "2018-11-12", "Sala Alterna", "Carolina Charry", "", "Celsia", "presencial", "alta", W.format('20181004', '/museo/exposiciones/savia-solaris-carolina-charry'), "Otra captura da cierre 2018-10-28. Programa C de Celsia"),
("Augusto Rivera, el gran ausente", "2018-10-10", "2018-10-19", "", "Augusto Rivera", "", "", "presencial", "media", W.format('20181010', '/museo/exposiciones/augusto-rivera-gran-ausente'), ""),
("World Press Photo 2018", "2018-10-18", "2018-11-08", "", "", "", "World Press Photo", "itinerante", "media", W.format('20181010', '/museo/exposiciones/world-press-photo-2018'), ""),
("Abandonen toda esperanza", "2018-11-07", "2019-02-10", "Sala Subterránea", "José Alejandro Restrepo", "Iván Tovar", "", "presencial", "alta", W.format('20181113', '/museo/exposiciones/abandonen-toda-esperanza'), ""),
("Reserva abierta. ¿Por fin Cali sabrá lo que tiene?", "2018-12-13", "2019-03-13", "", "", "", "", "colección", "media", W.format('20190213', '/museo/exposiciones/reserva-abierta'), ""),
("Trazar el umbral", "2018-12-13", "2019-03-24", "", "Juan Guillermo Tamayo", "Olga C. Eusse González", "Celsia", "presencial", "alta", W.format('20190213', '/museo/exposiciones/trazar-umbral-juan-guillermo-tamayo'), "Otra captura da cierre 2019-03-03. Programa C de Celsia"),
("Aula Flexible. Sala Taller", "2018-12-15", "2019-03-13", "Edificio de la Colección, primer piso", "", "Equipo Museo La Tertulia", "Secretaría de Cultura de Cali", "sala didáctica", "alta", W.format('20190204', '/museo/exposiciones/aula-flexible-sala-taller'), ""),
("El carácter de la tradición en la arquitectura de Barney, Távora, Coderch", "", "", "Sala Maritza Uribe de Urdinola", "Benjamín Barney, Fernando Távora, José Antonio Coderch", "", "", "presencial", "media", W.format('20190525', '/museo/exposiciones/caracter-la-tradicion-la-arquitectura-barney-tavora-coderch'), "Sin fechas; captura mayo 2019"),
("Srape Pøtø Tul-yu. El último círculo", "", "", "", "Julieth Morales", "", "Celsia", "presencial", "media", W.format('20190525', '/museo/exposiciones/srape-poto-tul-yu-ultimo-circulo-julieth-morales'), "Sin fechas; captura mayo 2019. Programa C de Celsia"),
("Exposición ganadores BLOC 2018", "", "", "", "Vanessa Ortiz, Herlyng Ferla", "", "Lugar a Dudas", "presencial", "media", W.format('20190714', '/museo/exposiciones/exposicion-ganadores-bloc-2018'), "Sin fechas; captura julio 2019"),
("La unión que separa las cosas. BLOC 2018", "", "", "", "", "", "Lugar a Dudas", "presencial", "baja", W.format('20190715', '/museo/exposiciones/la-union-separa-las-cosas'), "Finalistas BLOC 2018, sin nombres en la captura"),
("El Testigo", "", "", "", "Jesús Abad Colorado", "María Belén Sáez de Ibarra", "", "itinerante", "media", W.format('20190817', '/museo/exposiciones/el-testigo'), "Sin fechas; captura agosto 2019"),
("Manglaria. Raíces, vínculos y sujeciones", "", "", "", "", "", "", "presencial", "baja", W.format('20190817', '/museo/exposiciones/manglaria'), "Sin fechas; captura agosto 2019"),
("Bifurcaciones. Trayectos y cruces de una generación", "", "", "", "", "", "Embajada de Suiza en Colombia; Ministerio de Cultura", "presencial", "baja", W.format('20190915', '/museo/exposiciones/bifurcaciones'), "Premio Nacional Colombo Suizo de Fotografía; captura sept. 2019"),
("Voces para transformar a Colombia", "2019-09-26", "2019-10-27", "", "", "", "Museo de Memoria de Colombia", "itinerante", "media", W.format('20191018', '/museo/exposiciones/voces-transformar-colombia'), ""),
("Fractales", "", "", "", "Mónica Vilá", "", "Celsia", "presencial", "media", W.format('20191019', '/museo/exposiciones/fractales'), "Sin fechas; captura oct. 2019. Programa C de Celsia"),
("Sala Abierta. Acciones para la memoria y la reconciliación", "", "", "", "", "", "", "programa", "baja", W.format('20191117', '/museo/exposiciones/sala-abierta-acciones-para-la-memoria-y-la-reconciliacion'), "Captura nov. 2019"),
("El ruido del silencio", "2019-12-17", "2020-02-28", "", "Diego Hernández", "", "Celsia", "presencial", "alta", W.format('20200621', '/museo/exposiciones/ruido-del-silencio-diego-hernandez-programa-c-celsia'), "Programa C de Celsia"),
("María Thereza Negreiros y 16 mujeres artistas de su generación", "2020-03-24", "", "", "María Thereza Negreiros", "", "", "presencial", "media", W.format('20220119', '/exposicion-hijas-del-agua/'), "Fecha tomada del listado de la web (2020-03-24)"),
("Celeste", "2020-05-07", "", "", "Solimán López", "", "Parque Explora; Planetario de Bogotá; Casa de América", "virtual", "media", W.format('20200621', '/museo/destacados/instalacion-celeste'), "Instalación multimedia en línea"),
("UMBRAL adentro", "2020-05-28", "2020-06-11", "", "Mario Alvarez, Tatiana Cañón, Idamo Correal, Tatiana Díaz, Angélica Franco, Luisa Gallo, María Adelaida Garavito Velásquez, Natalia García, Sebastián García, María José González, Miguel Ángel Gutiérrez, Yaví Leal, Luisa Fernanda Moreno Osuna, Alexander Mueses, Mariana Ortíz Navarro, Luisa Rivera, Tomás Rubio, Paula Rodríguez, Stefany Ordóñez", "", "Universidad El Bosque", "virtual", "alta", W.format('20200621', '/museo/exposiciones/umbral-adentro'), ""),
("Impulsive Habitat. Sonidos para una cuarentena", "2020", "", "", "", "David Vélez", "", "virtual", "media", W.format('20200815', '/museo/exposiciones/impulsive-habitat'), "Compilación sonora en ocho sesiones"),
("Casa Ocupada. La colección cruza el puente", "", "", "Casa Obeso Mejía", "", "", "", "colección", "baja", W.format('20200621', '/museo/exposiciones/casa-ocupada-coleccion-museo-la-tertulia'), "Sin fechas; captura junio 2020"),
("Cuando nace el sonido", "2020-07-15", "", "", "", "", "", "presencial", "baja", L1, "Solo título y fecha en listado"),
("Sigo esperando", "2020-08-29", "2020-12-05", "Exteriores del museo", "", "", "Kadist; Espacio Odeón", "espacio público", "media", W.format('20201022', '/museo/destacados/sigo-esperando'), "Ciclo de video-arte; sesiones 29 ago, 10 oct, 5 dic"),
("El resplandor del desastre", "2020-10-01", "", "Jardines del museo", "Stephanie Montes", "", "", "espacio público", "alta", W.format('20201025', '/museo/exposiciones/el-resplandor-del-desastre-stephanie-montes'), ""),
("Proyecciones para el Sereno", "2020-10-09", "", "Jardines del museo", "Línea Roja Producciones", "", "", "espacio público", "media", W.format('20201025', '/museo/exposiciones/proyecciones-para-el-sereno'), ""),
("La escuela del desencanto", "2020-10-10", "", "Sala Alterna", "Catalina Jaramillo Quijano", "", "Celsia", "presencial", "alta", W.format('20201025', '/museo/exposiciones/la-escuela-del-desencanto-catalina-jaramillo'), "Programa C de Celsia"),
("Máquina monumental", "2020-10-10", "", "Edificio de la Colección, segundo piso", "", "", "", "presencial", "media", W.format('20201025', '/museo/exposiciones/maquina-monumental'), "En listado aparece también como 'Mecánica Monumental'"),
("Manual de instrucciones", "2020-10-10", "", "", "", "", "", "presencial", "baja", W.format('20220119', '/una-piedra-en-el-camino'), "Solo título y fecha en listado"),
("Subterránea 2020", "2020", "", "", "Acumulaciones Taller", "", "", "presencial", "media", W.format('20210302', '/museo/destacados/subterranea-2020'), "Exposición de la Feria Gráfica Subterránea"),
("Amanecer. BLOC 2020", "", "", "Sala Alterna", "Paula Solarte", "", "Lugar a Dudas", "presencial", "media", W.format('20210303', '/museo/destacados/amanecer-bloc-2020'), "Sin fechas; captura marzo 2021"),
("Barrio Adentro", "", "", "Casa Obeso Mejía", "", "", "Fundación Bolívar Davivienda; Gases de Occidente; Biblioteca Pública Centro Cultural Comuna 1", "comunitaria", "media", W.format('20210302', '/museo/destacados/barrio-adentro'), "Sin fechas; captura marzo 2021"),
("El ataque del presente contra el resto de los tiempos", "2021-02-06", "", "Sala Maritza Uribe de Urdinola", "Claudia Patricia Sarria Macías, Jose Ruiz Díaz, Laura Campaz, Juan Mejía, Colectivo Monómero, Dayana Camacho, Johan Samboní, Camilo Restrepo, Carolina Charry, Miguel Escobar, Ana María Millán", "", "", "presencial", "alta", W.format('20210302', '/museo/destacados/el-ataque-del-presente-contra-el-resto-de-los-tiempos'), "Segunda parte anunciada 2021-06-30"),
("VI Salón BAT de Arte Popular", "2021-04-22", "", "Casa Obeso Mejía", "Pablo Wilson Córdoba Saa", "", "BAT", "itinerante", "media", W.format('20210508', '/museo/destacados/vi-salon-bat-de-arte-popular'), "67 piezas; solo un autor nombrado en el extracto"),
("Una piedra en el camino", "2021-09-24", "", "", "", "", "", "presencial", "baja", L1, "Solo título y fecha en listado"),
("Wilson Díaz. Gusto y conflicto, motivos para coleccionar", "2021-09-25", "", "Sala Maritza Uribe de Urdinola", "Wilson Díaz", "", "", "presencial", "alta", W.format('20230327', '/museo/destacados/wilson-diaz-gusto-y-conflicto-motivos-para-coleccionar').replace('museolatertulia.com', 'archivo.museolatertulia.com'), ""),
("Manolo Lago. El entusiasmo de una idea", "2021-11", "", "", "Manuel Lago Franco", "Lina Saavedra de La Cruz, Adriana Castellanos Olmedos, Pavel Andrés Vernaza Ortiz", "", "presencial", "alta", W.format('20250215', '/manolo-lago-el-entusiasmo-de-una-idea'), "Fecha = publicación (2021-11-29); Vernaza: asistente de curaduría"),
("La esquina del barrio", "2021-12", "", "", "Johan Samboní, Sergio Lasso Estudio, Colectivo Deúniti", "Eva Parra, Carlos Uribe", "Fundación SURA; Museo de Antioquia", "presencial", "alta", W.format('20250215', '/la-esquina-del-barrio'), "Fecha = publicación (2021-12-23)"),
("Hijas del Agua", "", "", "", "Ruvén Afanador, Ana González", "", "", "presencial", "baja", L1, "Solo título y descripción en listado (captura ene. 2022)"),
("Transición. Cuarto Salón de Arte Contemporáneo del Pacífico", "", "", "", "", "", "", "salón", "baja", L1, "Captura ene. 2022"),
("Gráfica Subterránea", "", "", "", "", "", "", "presencial", "baja", L1, "Captura ene. 2022"),
("El aroma en construcción", "2022-02", "", "", "Paola Tafur", "", "", "presencial", "baja", W.format('20230120', '/reserva-abiertapor-fin-cali-sabra-lo-que-tiene'), "'Ganadora de Estímulos'; fecha = archivo mensual"),
("VII Salón BAT de Arte Popular. Colombia y el medio ambiente", "2022-03", "", "", "", "", "BAT", "itinerante", "baja", W.format('20250215', '/2022/03/'), "Fecha = archivo mensual"),
("21 obras en el cambio de tiempo", "2022-03", "2023-05-28", "", "", "", "Ministerio de Cultura", "colección", "media", W.format('20250215', '/21-obras-en-el-cambio-de-tiempo'), "Convocatoria Reactivarte 20x21; 21 artistas y colectivos, no nombrados en el extracto"),
("La cura para vos", "2022-05", "", "", "", "", "", "presencial", "baja", W.format('20250215', '/2022/05/'), "Fecha = archivo mensual"),
("Ir adentro", "2022-05", "", "", "", "", "", "presencial", "baja", W.format('20250215', '/2022/05/'), "Fecha = archivo mensual"),
("Exposición de Museo + Escuela", "2022-05", "", "", "", "", "Bancolombia", "educativa", "baja", W.format('20250215', '/exposicion-de-museo-escuela'), "Fecha = publicación"),
("EOCL", "2022-07", "", "", "Alejandra Ramírez", "Juan Pablo Velásquez", "", "presencial", "media", W.format('20241207', '/eoclalejandra-ramirez'), "Fecha = publicación (2022-07-31)"),
("Piel es", "2022-07-28", "2022-11-26", "", "Andrea Rey", "Yohanna M. Roa", "Universidad Icesi; MinCiencias", "presencial", "alta", W.format('20241207', '/piel-es'), ""),
("Deshilar, la revolución cotidiana", "2022-07-28", "", "", "Adrien Chauvin Picard, Alix Quirama, Andrea Rey, Ani Ganzala, Camila Rodríguez Triana, Carmenza Estrada, Cecilia Vicuña, Costurero Dapa, Costurero Electrónico, Daniela Whaley, Edith Medina, Florencia Alonso, Holman Álvarez, Irma Sofía Poeter, Juana Gómez, Juliana Silva, Laura Campaz, Lilia Ziamou, Lina Puerta, Luz Lizarazo, María del Carmen Espinosa, María del Pilar Vergel, María José Durán Steinman, Mariana Guimaraes, Maritza Sánchez H., Miriam Martínez, Miriam Medrez, Ornella Ridone, Pablo Van Wong", "", "", "presencial", "media", W.format('20241207', '/deshilar-la-revolucion-cotidiana'), "Lista de artistas truncada en la captura"),
("Hacer ver. Provocar el archivo, agitar el museo", "2022-12", "", "", "", "", "", "colección", "baja", W.format('20241207', '/hacer-ver-provocar-el-archivo-agitar-el-museo'), "Fecha = publicación; exposición por capítulos (ver Ingeniería de la visión)"),
("Cicatrices", "2023", "", "", "Luz Lizarazo", "", "", "presencial", "baja", W.format('20250215', '/exposicion-de-museo-escuela'), "'Exposición institucional dedicada a la obra de Luz Lizarazo'; año por agenda 2023"),
("Reimaginando Potrero Grande", "", "2023-10-20", "", "", "", "Alianza 4U; Tecnocentro Cultural Somos Pacífico; Artolución", "comunitaria", "media", W.format('20231206', '/exposicion-reimaginando-potrero-grande-un-viaje-artistico-y-tecnologico'), ""),
("Museo + Escuela. Muestra de proyectos 2022-2023", "2023-08-12", "2024-05", "Sala Alterna", "", "", "Bancolombia", "educativa", "media", W.format('20250215', '/museo-escuela-muestra-de-proyectos-2022-2023-2'), ""),
("Entre agua y raíces. Las luchas de La Chiqui en las montañas del Chocó", "2023-08-12", "2024-03", "", "Gabriela Pinilla", "", "", "presencial", "alta", W.format('20250215', '/entre-agua-y-raices-las-luchas-de-la-chiqui-en-las-montanas-del-choco-2-2'), ""),
("Wildlife Photographer of the Year", "2023-10", "", "", "", "", "Museo de Historia Natural de Londres", "itinerante", "baja", W.format('20250215', '/wildlife-photographer-of-the-year-2024-fotografo-de-vida-silvestre-del-ano-2024'), "Publicado 2023-10-25 pero el título dice '2024': verificar"),
("Huellas de desaparición. Los casos de Urabá, Palacio de Justicia y territorio nukak", "2023-12-14", "2024-06-28", "", "Forensic Architecture", "", "Comisión de la Verdad", "presencial", "alta", W.format('20250215', '/huellas-de-desaparicion-los-casos-de-uraba-palacio-de-justicia-y-territorio-nukak'), ""),
("Sendero de las esculturas", "", "", "Exteriores del museo", "", "", "", "permanente", "baja", W.format('20250215', '/2024/01/'), "'Exposición permanente. Entrada libre'"),
("Huellas comunes. Sala de encuentro, escucha y amplificación", "2024-01-14", "2024-05", "", "", "", "", "sala didáctica", "media", W.format('20250215', '/huellas-comunes'), ""),
("Imaginar el fuego de la memoria", "2024-04", "2024-06", "", "", "", "", "presencial", "media", W.format('20250215', '/imaginar-el-fuego-de-la-memoria'), "Resultado de talleres audiovisuales con comunidades afro"),
("Ingeniería de la visión", "2024-06-15", "2024-09", "", "", "", "", "colección", "media", W.format('20250215', '/15129-2'), "Capítulo de 'Hacer ver, provocar el archivo, agitar el museo'"),
("El arte de ser moderno. Ecos bauhausianos en Industrias Metálicas de Palmira", "2024-07-30", "2025-03", "", "Diego Henao", "María Astrid Ríos", "Industrias Metálicas de Palmira", "presencial", "alta", W.format('20250215', '/el-arte-de-ser-moderno-ecos-bauhausianos-en-industrias-metalicas-de-palmira'), "Diego Henao: artista en colaboración curatorial"),
("El mundo entero es una Bauhaus", "2024-07-30", "2025-03", "", "", "Boris Friedewald", "ZKM", "itinerante", "alta", W.format('20241207', '/el-mundo-entero-es-una-bauhaus'), ""),
("El árbol que devoró un mundo: los rumbos del caucho en La vorágine", "2024-10", "2025-03", "", "", "Erna von der Walde, Ximena Gama", "Piedra Tijera Papel; Ministerio de las Culturas, las Artes y los Saberes; Biblioteca Nacional de Colombia", "itinerante", "alta", W.format('20250215', '/el-arbol-que-devoro-un-mundo-los-rumbos-del-caucho-en-la-voragine'), ""),
("Espesuras. Habitar un mundo herido", "2024-10", "2025-03", "", "", "", "", "presencial", "media", W.format('20250215', '/espesura-habitar-un-mundo-herido-2'), ""),
("Fuego", "2024-12", "", "", "Gerson Vargas", "", "", "presencial", "media", W.format('20250215', '/fuego'), "Fecha = publicación (2024-12-04)"),
("Mateo López. Pasado futurista", "2025-10-23", "2026-07-19", "Sala Maritza Uribe de Urdinola", "Mateo López", "Julien Petit", "", "presencial", "alta", V, "Web actual, consultada 2026-10-03"),
("Espejo de luz", "2026-06-12", "2026-08-08", "Edificio de la Colección, tercer piso", "", "", "", "itinerante", "media", V, "Web actual, consultada 2026-10-03"),
("Carlos Garaicoa. Ciudad Armero", "2026-07-17", "2026-08-30", "Edificio de la Colección, primer piso", "Carlos Garaicoa", "Óscar Roldán", "", "presencial", "alta", V, "Web actual, consultada 2026-10-03"),
# Solo título en listados, sin fecha (pendientes de datar)
("La obra arquitectónica de Le Corbusier", "", "", "", "Le Corbusier", "", "", "presencial", "baja", L2, "Sin fecha"),
("Los lirios del campo y las aves del cielo", "", "", "", "", "", "", "presencial", "baja", L2, "Instalación sobre Kierkegaard; sin fecha"),
("Siete intelectuales en el bosque de bambú", "", "", "", "Yang Fudong", "", "", "presencial", "baja", W.format('20241207', '/de-frente-me-escondopower-paola'), "Solo en listado; sin fecha"),
("Requiem NN", "", "", "", "Juan Manuel Echavarría", "", "", "presencial", "baja", W.format('20241207', '/aula-flexiblesala-taller'), "Solo en listado; sin fecha"),
("Ensayos para un mundo perfecto. Salón de Arte BBVA. Nuevos nombres", "", "", "", "", "", "BBVA", "salón", "baja", W.format('20241207', '/aula-flexiblesala-taller'), "Solo en listado; sin fecha"),
("Rogelio Salmona. Espacios abiertos / espacios colectivos", "", "", "", "Rogelio Salmona", "", "", "presencial", "baja", W.format('20250215', '/ir-adentro'), "Solo en listado; sin fecha"),
("Sin novedad en la noche", "", "", "", "", "", "", "presencial", "baja", W.format('20230120', '/el-caracter-de-la-tradicion-en-la-arquitectura-debarney-tavora-coderch'), "Solo en listado; sin fecha"),
("Sala didáctica La escena", "", "", "", "", "", "", "sala didáctica", "baja", W.format('20241207', '/de-frente-me-escondopower-paola'), "Solo en listado; sin fecha"),
("Auditum. Semana de la Escucha 2020", "2020", "", "", "", "", "Parque Explora", "festival", "baja", W.format('20230120', '/la-union-que-separa-las-cosasun-proyecto-de-bloc-2018'), "Solo en listado"),
]

OUT = os.path.join(os.path.dirname(__file__), 'salida', 'exposiciones_2016_2026.csv')
cols = ['id_expo', 'nombre_expo', 'fecha_ini', 'fecha_fin', 'ano', 'espacio', 'artistas', 'curadores',
        'apoyan_auspicia', 'tipo', 'confianza', 'fuente_url', 'notas']
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(cols)
    for i, r in enumerate(R, start=831):
        ano = r[1][:4] if r[1] else ''
        w.writerow([f'ex.{i}', r[0], r[1], r[2], ano, *r[3:]])
print(len(R), 'filas ->', OUT)
