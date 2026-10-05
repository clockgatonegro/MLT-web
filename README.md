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

Sitio: **https://mlt.cactus.com.co/** (GitHub Pages con dominio propio).

1. En GitHub: Settings → Pages → *Deploy from a branch*, rama `master`, carpeta raíz. En *Custom domain* debe aparecer `mlt.cactus.com.co` (lo toma del archivo `CNAME`). Active *Enforce HTTPS* cuando GitHub emita el certificado.
2. En el DNS de cactus.com.co: registro `CNAME` con nombre `mlt` y valor `clockgatonegro.github.io`.
3. En Google Search Console: agregue la propiedad `https://mlt.cactus.com.co/`, pegue la etiqueta de verificación donde lo indica el comentario en `index.html` y envíe `sitemap.xml`.

- `index.html` incluye descripción, URL canónica, etiquetas Open Graph y datos estructurados `Dataset` de schema.org (Google Dataset Search).
- `og-image.png` es la imagen que se muestra al compartir el enlace.
- `robots.txt` y `sitemap.xml` quedan en la raíz del dominio.

## Analítica

Google Analytics 4 (ID `G-SYWHRKMC3T`) con modo de consentimiento: mientras la persona no acepte el aviso, GA4 solo recibe señales sin cookies. La decisión se guarda en el navegador (`localStorage`, clave `mlt_consent`).

Eventos propios de la visualización:

| Evento | Parámetros | Cuándo |
|---|---|---|
| `cambiar_vista` | `vista` (red, pro, dur) | Cambio de pestaña |
| `elegir_periodo` | `periodo` (p. ej. 1983-1992) | Botón de periodo en curadores → artistas |
| `cambiar_disposicion` | `disposicion` (fuerzas, cronologica) | Botones de disposición |
| `cambiar_color` | `color` (rol, com) | Color por rol o comunidad |
| `search` | `search_term`, `tipo` | Búsqueda de un agente o exposición |
| `ver_ficha` | `nombre`, `tipo`, `vista` | Apertura de una ficha |
| `file_download` | `file_name`, `origen` (pagina, github) | Descarga de una base |

Para ver `nombre`, `periodo`, `vista` y los demás parámetros en los informes, regístrelos en GA4 en Administrar → Definiciones personalizadas → Dimensiones personalizadas (alcance: evento).
