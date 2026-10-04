"""Normaliza la base MLT (xlsx 07/2016) y genera red bipartita exposición–agente para Gephi.
Salidas en mlt/salida/: exposiciones.csv, agentes.csv, nodos.csv, aristas.csv, no_cruzados.csv
"""
import openpyxl, csv, re, unicodedata, collections, os, sys

XLSX = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), 'salida'); os.makedirs(OUT, exist_ok=True)
wb = openpyxl.load_workbook(XLSX, read_only=True)

def filas(hoja):
    it = wb[hoja].iter_rows(values_only=True)
    cab = [c for c in next(it)]
    return [dict(zip(cab, r)) for r in it if r and r[0] not in (None, '')]

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def entero(v):
    try: return int(float(v))
    except (TypeError, ValueError): return None

VACIOS = {'varios', 'varios artistas', 'n a', 'na', 'sin informacion', 'anonimo', 'otros', ''}

def separar(txt):
    """Separa listas de nombres en texto: comas, punto y coma, ' y ' final, saltos de línea."""
    if not txt: return []
    t = str(txt).replace('\n', ',').replace(';', ',')
    partes = []
    for p in t.split(','):
        p = p.strip(' .')
        # 'A y B' solo si ambos lados parecen nombres (evita 'Ministerio de Cultura y Turismo' rara vez; se reporta)
        sub = [s.strip(' .') for s in re.split(r'\s+y\s+(?=[A-ZÁÉÍÓÚÑ])', p) if s.strip(' .')]
        # solo se parte por ' y ' si cada parte existe en un catálogo; si no, el nombre queda entero
        en_cat = lambda s: norm(s) in idx_p or norm(s) in idx_o
        if len(sub) > 1 and not en_cat(p) and all(en_cat(s) for s in sub):
            partes += sub
        else:
            partes.append(p)
    return [p for p in partes if norm(p) not in VACIOS]

# ---------- catálogos ----------
personas = filas('personas')
orgs = filas('organizaciones')
espacios = {r['nombre_espacio']: r for r in filas('espacios')}

idx_p, idx_o = {}, {}
for r in personas:
    pid = entero(r['id_persona'])
    if pid is None: continue
    for campo in ('nombre_registro_creador', 'seudonimo_persona', 'otros_nombres'):
        if r.get(campo): idx_p.setdefault(norm(r[campo]), pid)
    if r.get('nombres_persona') and r.get('apellidos_persona'):
        idx_p.setdefault(norm(f"{r['nombres_persona']} {r['apellidos_persona']}"), pid)
for r in orgs:
    oid = entero(r['id_organizaciones'])
    if oid is not None: idx_o.setdefault(norm(r['nombre_institucion']), oid)

agentes = {}   # id -> dict
for r in personas:
    pid = entero(r['id_persona'])
    if pid is None: continue
    agentes[f'p.{pid}'] = dict(Id=f'p.{pid}', Label=str(r['nombre_registro_creador']).strip(), clase='persona',
        ocupacion=r.get('ocupaciones') or '', nacionalidad=r.get('nacionalidad') or '', sexo=r.get('sexo') or '',
        ano_nacimiento=entero(r.get('ano_nacimiento')) or '', ano_muerte=entero(r.get('ano_muerte')) or '', origen='catalogo_personas')
for r in orgs:
    oid = entero(r['id_organizaciones'])
    if oid is None: continue
    agentes[f'o.{oid}'] = dict(Id=f'o.{oid}', Label=str(r['nombre_institucion']).strip(), clase='organizacion',
        ocupacion='', nacionalidad=r.get('pais') or '', sexo='', ano_nacimiento=entero(r.get('ano_constitucion')) or '',
        ano_muerte=entero(r.get('ano_cierre')) or '', origen='catalogo_organizaciones')

nuevos = {}  # norm -> id para nombres no catalogados
# Equivalencias revisadas a mano (nombre en archivo web -> registro del catálogo 2016)
ALIAS = {'alejandro martin': 'p.3153', 'claudia patricia sarria macias': 'p.2258', 'ericka florez hidalgo': 'p.2708',
         'luz lizarazo': 'p.166', 'manuel lago franco': 'p.1212', 'yohanna m roa': 'p.3243', 'oscar roldan': 'p.3223',
         'embajada de suiza en colombia': 'o.173', 'equipo museo la tertulia': 'o.332'}
def resolver(nombre, preferir):
    k = norm(nombre)
    if k in ALIAS: return ALIAS[k], True
    orden = [('p', idx_p), ('o', idx_o)] if preferir == 'p' else [('o', idx_o), ('p', idx_p)]
    for pref, idx in orden:
        if k in idx: return f'{pref}.{idx[k]}', True
    if k not in nuevos:
        nid = f'n.{len(nuevos)+1}'
        nuevos[k] = nid
        agentes[nid] = dict(Id=nid, Label=nombre, clase='sin_catalogar', ocupacion='', nacionalidad='', sexo='',
                            ano_nacimiento='', ano_muerte='', origen='texto_exposiciones')
    return nuevos[k], False

# ---------- exposiciones ----------
expos, aristas, no_cruzados = [], [], []
ROLES = [('artistas', 'artista', 'p'), ('curadores', 'curador', 'p'),
         ('presentadores', 'presentador', 'p'), ('apoyan_auspicia', 'apoyo', 'o')]
for r in filas('Exposiciones-agentes'):
    eid = entero(r['id_expo'])
    if eid is None: continue
    a0, m0, d0 = entero(r['ano_ini']), entero(r['mes_ini']), entero(r['dia_ini'])
    a1, m1, d1 = entero(r['ano_fin']), entero(r['mes_fin']), entero(r['dia_fin'])
    fi = f'{a0:04d}-{m0 or 1:02d}-{d0 or 1:02d}' if a0 else ''
    ff = f'{a1:04d}-{m1 or 1:02d}-{d1 or 1:02d}' if a1 else ''
    esp = (r.get('nombre_espacio') or '').strip()
    sedes = {(espacios.get(s.strip()) or {}).get('sede') for s in esp.split(',')} - {None, ''}
    sede = '|'.join(sorted(sedes))
    nombre = str(r['nombre_expo']).strip()
    e = dict(Id=f'ex.{eid}', Label=nombre, ano=a0 or '', decada=(a0 // 10 * 10) if a0 else '',
             fecha_ini=fi, fecha_fin=ff, espacio=esp, sede=sede, tipo_expo=r.get('tipo_expo') or '',
             autor_texto=r.get('autor_texto') or '', artistas_varios=int(norm(r.get('artistas') or '') in ('varios',)),
             fuente='MLT_DB_07_2016')
    expos.append(e)
    vistos = set()
    for campo, rol, pref in ROLES:
        for nom in separar(r.get(campo)):
            aid, ok = resolver(nom, pref)
            if (aid, rol) in vistos: continue
            vistos.add((aid, rol))
            aristas.append(dict(Source=f'ex.{eid}', Target=aid, Type='Undirected', rol=rol, ano=a0 or '',
                                Label=rol, Weight=1, fuente='MLT_DB_07_2016'))
            if not ok: no_cruzados.append(dict(id_expo=f'ex.{eid}', campo=campo, texto=nom, id_asignado=aid))

# ---------- complemento 2016–2026 (archivo web) ----------
COMP = os.path.join(OUT, 'exposiciones_2016_2026.csv')
if os.path.exists(COMP):
    for r in csv.DictReader(open(COMP, encoding='utf-8')):
        a0 = entero(r['ano'])
        fuente = 'web_actual_2026' if 'museolatertulia.co/' in r['fuente_url'] else ('archivo_web' if r['fuente_url'] else 'piezas_cactus')
        esp = r['espacio']
        sedes = {(espacios.get(s.strip()) or {}).get('sede') for s in esp.split(',')} - {None, ''}
        expos.append(dict(Id=r['id_expo'], Label=r['nombre_expo'], ano=a0 or '', decada=(a0 // 10 * 10) if a0 else '',
                          fecha_ini=r['fecha_ini'], fecha_fin=r['fecha_fin'], espacio=esp, sede='|'.join(sorted(sedes)),
                          tipo_expo=r['tipo'], autor_texto='', fuente=fuente,
                          confianza=r['confianza'], fuente_url=r['fuente_url'], pieza_cactus=r.get('pieza_cactus',''),
                          modalidad_fija=r.get('modalidad',''), artistas_varios=int('varios' in (r['notas'] or '').lower() and 'artistas' in (r['notas'] or '').lower())))
        vistos = set()
        for campo, rol, pref in [('artistas', 'artista', 'p'), ('curadores', 'curador', 'p'), ('apoyan_auspicia', 'apoyo', 'o')]:
            noms = [x.strip() for x in r[campo].split(';') if x.strip()] if campo == 'apoyan_auspicia' else separar(r[campo])
            for nom in noms:
                aid, ok = resolver(nom, pref)
                if (aid, rol) in vistos: continue
                vistos.add((aid, rol))
                aristas.append(dict(Source=r['id_expo'], Target=aid, Type='Undirected', rol=rol, ano=a0 or '',
                                    Label=rol, Weight=1, fuente=fuente))
                if not ok: no_cruzados.append(dict(id_expo=r['id_expo'], campo=campo, texto=nom, id_asignado=aid))

# ---------- salidas ----------
grado = collections.Counter(a['Target'] for a in aristas)
roles_ag = collections.defaultdict(set)
for a in aristas: roles_ag[a['Target']].add(a['rol'])
ag_usados = [dict(v, roles='|'.join(sorted(roles_ag[k])), n_expos=grado[k]) for k, v in agentes.items() if k in grado]

def esc(nombre, filas_, campos):
    with open(os.path.join(OUT, nombre), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore'); w.writeheader(); w.writerows(filas_)

# modalidad (mismo criterio que la gráfica 'división temporal' del proyecto): individual = 1 artista; colectiva = 2 o más; n/d = sin artistas nombrados ('varios')
n_art = collections.Counter(a['Source'] for a in aristas if a['rol'] == 'artista')
for e in expos:
    k = n_art[e['Id']]
    e['n_artistas'] = k
    e['modalidad'] = e.get('modalidad_fija') or ('individual' if k == 1 else 'colectiva' if k >= 2 else 'n/d')
CE=['Id','Label','ano','decada','fecha_ini','fecha_fin','espacio','sede','tipo_expo','modalidad','n_artistas','autor_texto','artistas_varios','fuente','confianza','fuente_url','pieza_cactus']
for e in expos:
    e.setdefault('confianza','base_MLT'); e.setdefault('fuente_url',''); e.setdefault('pieza_cactus','')
esc('exposiciones.csv', expos, CE)
camp_ag = ['Id', 'Label', 'clase', 'roles', 'n_expos', 'ocupacion', 'nacionalidad', 'sexo', 'ano_nacimiento', 'ano_muerte', 'origen']
esc('agentes.csv', ag_usados, camp_ag)
nodos = [dict(Id=e['Id'], Label=e['Label'], tipo='exposicion', clase='exposicion', ano=e['ano'], decada=e['decada'],
              sede=e['sede'], espacio=e['espacio'], roles='', n_expos='', fuente=e['fuente'], modalidad=e['modalidad']) for e in expos] + \
        [dict(Id=a['Id'], Label=a['Label'], tipo='agente', clase=a['clase'], ano='', decada='', sede='', espacio='',
              roles=a['roles'], n_expos=a['n_expos'], fuente=a['origen'], modalidad='') for a in ag_usados]
esc('nodos.csv', nodos, ['Id', 'Label', 'tipo', 'clase', 'ano', 'decada', 'sede', 'espacio', 'roles', 'n_expos', 'fuente', 'modalidad'])
esc('aristas.csv', aristas, ['Source', 'Target', 'Type', 'Label', 'rol', 'ano', 'Weight', 'fuente'])
esc('no_cruzados.csv', no_cruzados, ['id_expo', 'campo', 'texto', 'id_asignado'])

print('exposiciones', len(expos), '| agentes', len(ag_usados), '| aristas', len(aristas))
print('por rol', collections.Counter(a['rol'] for a in aristas))
print('por clase', collections.Counter(a['clase'] for a in ag_usados))
print('menciones sin cruzar', len(no_cruzados), '| nombres nuevos', len(nuevos))
print('expos sin aristas', sum(1 for e in expos if e['Id'] not in {a['Source'] for a in aristas}))
