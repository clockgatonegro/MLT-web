# Red MLT exposición–agente: datos y vacíos (octubre 2026)

## Archivos

| Archivo | Contenido |
|---|---|
| `nodos.csv` | 926 exposiciones y 3.563 agentes. Columnas Gephi: `Id`, `Label`, `tipo`, `clase`, `ano`, `decada`, `sede`, `espacio`, `roles`, `n_expos`, `fuente` |
| `aristas.csv` | 8.249 aristas no dirigidas `Source` (exposición) → `Target` (agente), con `rol` (artista, curador, presentador, apoyo), `ano` y `fuente` |
| `exposiciones.csv` | Tabla de exposiciones con fechas, espacio, sede, tipo, `confianza` y `fuente_url` |
| `agentes.csv` | Agentes con atributos del catálogo de personas y organizaciones de 2016 |
| `exposiciones_2016_2026.csv` | Las 96 exposiciones nuevas transcritas, con su URL de captura |
| `candidatos_homonimia.csv` | Coincidencias de nombres que no apliqué y que debes decidir tú |
| `no_cruzados.csv` | Menciones que no aparecen en el catálogo de 2016 (se crearon como `n.*`) |

Los IDs `ex.*`, `p.*` y `o.*` son los de la base original. Los agentes nuevos usan `n.*` y las exposiciones nuevas van de `ex.831` a `ex.926`.

## Base de 2016: qué hice

- Separé los nombres que estaban como texto en `artistas`, `curadores`, `presentadores` y `apoyan_auspicia`, y los crucé contra `personas` y `organizaciones`. Sobre la base de 2016 quedó una sola mención sin cruzar: "Dirección de cultura del municipio de Cali". Corté por " y " solo cuando ambas partes existían en el catálogo; así "Lago y Sáenz" quedó como una sola entidad.
- "Varios" no se convierte en nodo. Por eso 40 exposiciones de la base no tienen aristas.
- Las fórmulas de Sheets (fechas, `DATEDIF`, `VLOOKUP`) las volví a calcular en código.

**Diferencia con el CSV del repositorio:** ese archivo tiene 8.523 pares y la red nueva tiene 8.040 sobre la misma base. Inferencia mía, no verificada: la diferencia viene de que el CSV anterior incluía "Varios" como agente (115 menciones) y no separaba los roles. Los IDs `a.*` de ese CSV no coinciden con los `id_persona` del xlsx (por ejemplo, Julio Abril es `a.1334` allá y `p.3252` acá), así que no se pueden comparar fila por fila.

## Complemento 2016–2026: de dónde salió

La web actual (museolatertulia.co) se rehízo y solo muestra tres exposiciones vigentes. El resto lo reconstruí con capturas del Archivo de Internet de tres sitios anteriores:

- museolatertulia.org (2015–2017)
- museolatertulia.com, con rutas `/museo/exposiciones/` (2017–2021)
- museolatertulia.com en WordPress (2021–2025)

Cada fila trae su URL de captura. Transcribí solo lo que aparece escrito en la página; no completé nada de memoria.

| Confianza | Filas | Qué significa |
|---|---|---|
| alta | 28 | Fechas y agentes explícitos |
| media | 38 | Falta la fecha o la lista de agentes está incompleta |
| baja | 30 | Solo el título en un listado. Cuando hay año, sale del archivo mensual o de la fecha de publicación, no de la exposición |

## II Bienal Americana de Artes Gráficas (1973)

La base de 2016 traía la II Bienal (`ex.181`) sin artistas. Los 196 participantes se tomaron del catálogo de la bienal (lista en `scripts/fuentes/catalogo_II_bienal_1973.txt`); sus aristas llevan `fuente = catalogo_II_bienal_1973`. 141 coinciden con el catálogo de personas de 2016: 126 por nombre exacto, 9 por variantes de grafía claras (por ejemplo, Roser Brau → Roser Bru, Ken Danby → Ken Damby) y 6 confirmadas por los autores (por ejemplo, Francisco Rocca → Francisco Rocca-Lynn), documentadas en `ALIAS`. El registro «Francisco Jung» del catálogo de 2016 se corrigió a Francisco Hung. Nelson Romero y Nelson Román son personas distintas. Los otros 55 se crearon como agentes nuevos (`n.*`).

## Cali 71, ciudad de América (2016–2019)

La base de 2016 traía 6 artistas para `ex.827`. Con las fichas técnicas, el listado de obras de la curaduría (`FTECNICAS_obras_CALI71_AM`) y el programa de mano de la exposición y de sus rotaciones (archivos de Cactus Taller Gráfico, 2016–2019) quedan 110. La lista, con el documento de origen de cada nombre, está en `scripts/fuentes/participantes_cali71.csv`. 73 de los 110 participaron también en alguna Bienal Americana de Artes Gráficas. No se incluyeron las personas que solo aparecen retratadas en fotografías ni los nombres que solo se citan en los textos de sala.

## Otras exposiciones completadas con fichas técnicas de Cactus

`scripts/fuentes/participantes_fichas_cactus.csv` agrega artistas (y, cuando consta, curadores) a exposiciones que en la base tenían pocos o ningún agente: Artist Talking Back to the Media (2016), (El otro lado de la) Carretera al mar (2018), Reserva abierta (2018), Casa Ocupada (2019–2020), Las populares Gráficas Molinari (2018), María Thereza Negreiros y 16 mujeres artistas (2020), Manglaria (2019), Aula Flexible (2018), el cuarto y quinto guion de la colección (2014) y la sexta rotación (2015). También completa Universo Holograma, ¡Oído pueblo!, Territorio en discusión y Rojo y más rojo. Los curadores de Las populares Gráficas Molinari salen del informe de gestión de 2018.

## Triangulación con el archivo de Cactus Taller Gráfico (2009–2021)

Cactus diseñó las piezas del museo desde *Eros, dolor y muerte* (2009) hasta *El ataque del presente contra el resto de los tiempos* (2021). Para ese tramo se buscó cada exposición en su archivo (programas de mano, invitaciones, fichas técnicas, boletines y cuadernillos de programación) y se anotó el resultado en `scripts/fuentes/triangulacion_cactus.csv`, con el documento de cada dato. Reglas:

- **confirma / corrige / agrega**: se aplican. Una ficha que solo venía de la web y queda respaldada por un documento de Cactus pasa a confianza «alta» (●). Los documentos quedan en la columna `fuentes_cactus` de `exposiciones.csv`.
- **conflicto**: no se aplica; el dato de la base se mantiene y la discrepancia queda en `conflictos_cactus.csv` para que la resuelvan los autores.
- **duplicado**: cinco filas web sin fecha repetían exposiciones ya fechadas y se unieron con ellas: La guerra que no hemos visto, Siete intelectuales en el bosque de bambú, Réquiem NN, Rogelio Salmona (las cuatro de 2011) y la sala didáctica La Escena (2017). La película *Réquiem NN* que la Cinemateca proyectó en 2014 no es una exposición.

Resultado: 101 exposiciones con al menos un documento de Cactus y 14 conflictos. También se agregaron participantes que la web no traía: los finalistas y curadores de BLOC 2018 (*La unión que separa las cosas*), los fotógrafos y curadores de *Bifurcaciones*, los curadores de *Fractales*, los artistas de *Manual de instrucciones* (según la publicación del programa) y Sandra Rengifo en *Los lirios del campo y las aves del cielo*. Dos grafías se corrigieron con los documentos: Adriana Castellanos Olmedo (la web decía «Olmedos») y Manuel Augusto Soares Mendes.

Exposiciones de 2009–2021 que solo vienen de la web y no tienen rastro en el archivo de Cactus: El mundo según Mafalda, UMBRAL adentro, Impulsive Habitat, Cuando nace el sonido, El resplandor del desastre, Proyecciones para el Sereno, Máquina monumental, Subterránea 2020, VI Salón BAT de Arte Popular, Una piedra en el camino, Wilson Díaz. Gusto y conflicto, La esquina del barrio, Hijas del Agua, Transición (Cuarto Salón del Pacífico), Gráfica Subterránea, EOCL, Reimaginando Potrero Grande, Ensayos para un mundo perfecto y Auditum 2020. Varias son ciclos sonoros o virtuales de la pandemia, que no necesitaban pieza impresa.

## Contraste con el Flickr del museo (2021–2025)

El [Flickr del Museo La Tertulia](https://www.flickr.com/photos/museo-la-tertulia/albums) tiene 24 álbumes; se dejaron de lado los de Vacaciones Creativas y la Feria Subterránea. Los 20 álbumes de exposiciones se cruzaron con la Base de datos y el resultado está en `scripts/fuentes/triangulacion_flickr.csv` (fechas, salas, curadurías) y `scripts/fuentes/participantes_flickr.csv` (curadores y artistas, con `fuente = participantes_flickr`). La ficha de cada exposición enlaza su álbum.

- Se precisaron fechas de Espesuras, Entre agua y raíces, Hacer ver, Deshilar, 21 obras en el cambio de tiempo, El aroma en construcción, La esquina del barrio y Fuego.
- Se agregaron las curadurías de Espesuras (Melissa Aguilar y Carolina Chacón), Hacer ver (Melissa Aguilar, Mónica Restrepo y Nicolás Bonilla), Deshilar (Yohanna M. Roa), Cicatrices (Eugenio Viola), 21 obras en el cambio de tiempo (Yolanda Chois Rivera) y El aroma en construcción (Miguel González), y los artistas de Hacer ver (81), Deshilar y 21 obras en el cambio de tiempo.
- Las fechas de los álbumes no se usan para discutir las de la Base de datos, salvo en ¡A la gráfica! y 21 obras en el cambio de tiempo, que quedaron en `conflictos_cactus.csv` sin aplicar.
- Se agregaron tres exposiciones que solo aparecían en Flickr: Cuerpo transgresivo. Rosemberg Sandoval (2025), Barrio Adentro. La unión popular hace los barrios (2024) y Barrio Adentro. Montebello (2023). Barrio Adentro es una curaduría con comunidades que usan obras de la colección para contar su barrio; cada versión lleva el nombre del barrio, y la de 2021 quedó como Barrio Adentro. Vista Hermosa.

## Vacíos por resolver

1. **Conflictos de fecha con el archivo de Cactus** (14, en `conflictos_cactus.csv`): entre otros, el cierre de Cali 71 (2017 o 2019, por sus rotaciones), El Testigo (17 de noviembre de 2019 o 1 de marzo de 2020), El ruido del silencio, Celeste (marzo o mayo de 2020), el espacio de Le Corbusier (Casa Obeso Mejía o jardines) y el nombre de Catalina o Carolina Torres en ¡Oído pueblo!
2. **6 exposiciones siguen sin fecha:** Hijas del Agua, Transición, Gráfica Subterránea, Reimaginando Potrero Grande, Sendero de las esculturas y Ensayos para un mundo perfecto.
3. **Listas truncadas:** en Universo Holograma y Deshilar la captura corta la lista de artistas, y en 21 obras en el cambio de tiempo y el VI Salón BAT no aparecen los nombres (los de BLOC 2018 ya se completaron con el programa de mano).
4. **Fechas que se contradicen** (anotadas en `notas`): Costurero Viajero (2017 o 2018), Savia Solaris (cierre 28 de octubre o 12 de noviembre de 2018), Trazar el umbral (cierre 3 o 24 de marzo de 2019) y Wildlife Photographer (publicada en 2023 con "2024" en el título).
5. **Sedes:** en los registros nuevos casi nunca aparece la sala, así que `sede` quedó vacía en la mayoría.
6. **Homonimias:** apliqué solo las equivalencias claras, que están documentadas en `ALIAS` dentro de `normalizar.py`. Por ejemplo, Ericka Flórez Hidalgo → Éricka Flórez, Luz Lizarazo → Luz Ángela Lizarazo y Óscar Roldán → Oscar Roldán-Alzate. Tres casos más (Camila Rodríguez Triana, Jose Ruiz Díaz y María del Carmen Espinosa) fueron confirmados por los autores y están en `candidatos_homonimia.csv`.
7. **El catálogo de personas termina en 2016.** Los 142 agentes nuevos (`n.*`) no tienen nacionalidad, ocupación ni fechas.
8. **Programas que no son exposiciones:** Sigo esperando, Impulsive Habitat, Celeste y UMBRAL adentro son ciclos de video, sonoros o virtuales. Quedaron marcados en `tipo` para que puedas filtrarlos.

Para cerrar los puntos 1 a 4, lo más directo sería el archivo del CEDOC del museo o los programas de mano.

## Reproducir

```
python3 complemento_2016_2026.py
python3 cactus_fechas.py
python3 normalizar.py MLT_DB_07_2016.xlsx
```
