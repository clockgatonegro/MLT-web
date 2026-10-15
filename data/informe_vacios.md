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

## Cali 71, ciudad de América (2016–2018)

La base de 2016 traía 6 artistas para `ex.827`. Con las fichas técnicas, el listado de obras de la curaduría (`FTECNICAS_obras_CALI71_AM`) y el programa de mano de la exposición y de sus rotaciones (archivos de Cactus Taller Gráfico, 2016–2018) quedan 110. La lista, con el documento de origen de cada nombre, está en `scripts/fuentes/participantes_cali71.csv`. 73 de los 110 participaron también en alguna Bienal Americana de Artes Gráficas. No se incluyeron las personas que solo aparecen retratadas en fotografías ni los nombres que solo se citan en los textos de sala.

## Otras exposiciones completadas con fichas técnicas de Cactus

`scripts/fuentes/participantes_fichas_cactus.csv` agrega artistas (y, cuando consta, curadores) a exposiciones que en la base tenían pocos o ningún agente: Artist Talking Back to the Media (2016), (El otro lado de la) Carretera al mar (2018), Reserva abierta (2018), Casa Ocupada (2019–2020), Las populares Gráficas Molinari (2018), María Thereza Negreiros y 16 mujeres artistas (2020), Manglaria (2019), Aula Flexible (2018), el cuarto y quinto guion de la colección (2014) y la sexta rotación (2015). También completa Universo Holograma, ¡Oído pueblo!, Territorio en discusión y Rojo y más rojo. Los curadores de Las populares Gráficas Molinari salen del informe de gestión de 2018.

## Vacíos por resolver

1. **2019 está casi vacío** (2 exposiciones con fecha). Las fichas archivadas de ese año no traen fechas. Siete exposiciones con captura en 2019 quedaron sin año: Barney/Távora/Coderch, Julieth Morales, BLOC 2018, El Testigo, Manglaria, Bifurcaciones y Fractales.
2. **26 exposiciones no tienen fecha.** Entre ellas Le Corbusier, Rogelio Salmona, Requiem NN (Juan Manuel Echavarría), Yang Fudong, Hijas del Agua y Sendero de las esculturas.
3. **Listas truncadas:** en Universo Holograma y Deshilar la captura corta la lista de artistas, y en 21 obras en el cambio de tiempo, VI Salón BAT y BLOC 2018 no aparecen los nombres.
4. **Fechas que se contradicen** (anotadas en `notas`): Costurero Viajero (2017 o 2018), Savia Solaris (cierre 28 de octubre o 12 de noviembre de 2018), Trazar el umbral (cierre 3 o 24 de marzo de 2019) y Wildlife Photographer (publicada en 2023 con "2024" en el título).
5. **Sedes:** en los registros nuevos casi nunca aparece la sala, así que `sede` quedó vacía en la mayoría.
6. **Homonimias:** apliqué solo las equivalencias claras, que están documentadas en `ALIAS` dentro de `normalizar.py`. Por ejemplo, Ericka Flórez Hidalgo → Éricka Flórez, Luz Lizarazo → Luz Ángela Lizarazo y Óscar Roldán → Oscar Roldán-Alzate. Tres casos más (Camila Rodríguez Triana, Jose Ruiz Díaz y María del Carmen Espinosa) fueron confirmados por los autores y están en `candidatos_homonimia.csv`.
7. **El catálogo de personas termina en 2016.** Los 142 agentes nuevos (`n.*`) no tienen nacionalidad, ocupación ni fechas.
8. **Programas que no son exposiciones:** Sigo esperando, Impulsive Habitat, Celeste y UMBRAL adentro son ciclos de video, sonoros o virtuales. Quedaron marcados en `tipo` para que puedas filtrarlos.

Para cerrar los puntos 1 a 4, lo más directo sería el archivo del CEDOC del museo o los programas de mano.

## Reproducir

```
python3 complemento_2016_2026.py
python3 normalizar.py MLT_DB_07_2016.xlsx
```
