# Red del Museo La Tertulia

Red de exposiciones y agentes del Museo La Tertulia (Cali), 1956–2026. Parte del proyecto *Cartografiar redes del arte. 60 años del Museo La Tertulia*.

**Créditos:** Juan Fernando Correa · Carlos Dussán.

- `index.html` — visualización interactiva (d3 v7): red de exposiciones (fuerzas o cronológica), proyección curadores → artistas por periodos con comunidades, y duración de las exposiciones. Funciona sola, con los datos incluidos.
- `eventos-agentes-MLT.html` — primera versión (2016).

## Datos (`data/`)

Archivos CSV en UTF-8, listos para Gephi (Laboratorio de datos → Importar hoja de cálculo).

| Archivo | Contenido |
|---|---|
| `nodos.csv` | Exposiciones y agentes: `Id, Label, tipo, clase, ano, decada, sede, espacio, roles, n_expos, fuente, modalidad` |
| `aristas.csv` | Exposición → agente: `Source, Target, Type, Label, rol, ano, Weight, fuente` |
| `exposiciones.csv` | Ficha de cada exposición, con `modalidad` (individual, colectiva, n/d), fechas, espacio, fuente y pieza gráfica de origen |
| `agentes.csv` | Personas y organizaciones, con roles y número de exposiciones |
| `exposiciones_2016_2026.csv` | Exposiciones agregadas después de la base de julio de 2016, con la URL de cada fuente |
| `candidatos_homonimia.csv`, `no_cruzados.csv` | Pendientes de revisión manual |
| `informe_vacios.md` | Vacíos conocidos de la base |

**Modalidad:** individual = un artista; colectiva = dos o más; n/d = sin artistas nombrados ("Varios"). Es el criterio de la gráfica "división temporal" del proyecto.

**Fuentes:** base MLT 07/2016; capturas del Archivo de Internet de museolatertulia.org y museolatertulia.com; piezas gráficas de Cactus Taller Gráfico para el museo (2016–2021); web del museo consultada el 3 de octubre de 2026.

`data/MLT_DB_07_2016 - enlaces-MLT.csv` es la lista de enlaces original de 2016 y se conserva sin cambios.

## Regenerar (`scripts/`)

```
python3 scripts/complemento_2016_2026.py
python3 scripts/cactus_fechas.py
python3 scripts/normalizar.py MLT_DB_07_2016.xlsx
python3 scripts/datos_web.py          # requiere networkx
```
Las rutas de los scripts apuntan a una carpeta `salida/`; ajústelas si los ejecuta desde el repositorio.

## Publicación e indexación

La página está pensada para GitHub Pages (Settings → Pages → rama `master`, carpeta raíz): `https://clockgatonegro.github.io/MLT-web/`.

- `index.html` incluye descripción, URL canónica, etiquetas para redes sociales (Open Graph) y datos estructurados `Dataset` de schema.org, que permiten que las bases aparezcan en Google Dataset Search.
- `og-image.png` es la imagen que se muestra al compartir el enlace.
- `sitemap.xml` se envía en Google Search Console. Pegue la etiqueta de verificación de Search Console donde lo indica el comentario en `index.html`.
- `robots.txt` solo tiene efecto en la raíz del dominio (`clockgatonegro.github.io/robots.txt`), es decir, en un repositorio `clockgatonegro.github.io`. En este repositorio sirve como referencia: GitHub Pages permite indexar por defecto.
