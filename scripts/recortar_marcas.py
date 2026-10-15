"""Recorta a ras (TrimBox) los programas de imprenta que traen marcas de corte.

Para cada programa «digital» cuyo PDF original tiene un TrimBox menor que el MediaBox,
rehace programas/pdf/<id>.pdf y programas/portadas/<id>.jpg con la página recortada al TrimBox.
El recorte de portada de programas_fuentes.csv (fracciones de la página completa) se traslada al área recortada.
Uso: MLT_ORIGINALES=<raíz de originales> uv run --with pymupdf --with pillow python scripts/recortar_marcas.py [ids…]
"""
import csv, shutil, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import programas as P
import fitz

def recortar(doc):
    hubo = False
    for pg in doc:
        m, t = pg.mediabox, pg.trimbox
        if t.width < m.width - 1 or t.height < m.height - 1:
            pg.set_cropbox(t); hubo = True
    return hubo

def traslada(recorte, m, t):
    if not recorte: return recorte
    x0, y0, x1, y1, giro = [float(v) for v in recorte.split()]
    fx = lambda v: min(1, max(0, (v * m.width - (t.x0 - m.x0)) / t.width))
    fy = lambda v: min(1, max(0, (v * m.height - (t.y0 - m.y0)) / t.height))
    return f"{fx(x0):.4f} {fy(y0):.4f} {fx(x1):.4f} {fy(y1):.4f} {giro:g}"

filas = [f for f in csv.DictReader(open(P.RAIZ / "data/programas_fuentes.csv", encoding="utf-8")) if f["id_expo"]]
P.ids(filas)
solo = set(sys.argv[1:])
hechos = []
for f in filas:
    if f["origen"] != "digital" or (solo and f["id"] not in solo): continue
    src = P.ORIG / f["ruta"]
    doc = fitz.open(src, filetype="pdf")
    m, t = doc[0].mediabox, doc[0].trimbox
    if not recortar(doc): continue
    rec = traslada(f["recorte"], m, t)
    P.portada(doc, rec, P.PORT / (f["id"] + ".jpg"))
    dp = P.PDF / (f["id"] + ".pdf")
    if src.stat().st_size <= P.MAX_DIG and src.suffix.lower() == ".pdf":
        dp.write_bytes(doc.tobytes(garbage=3, deflate=True))
    else:
        out = P.raster(doc, P.LADO_DIG, P.CAL_DIG); dp.write_bytes(out.tobytes(garbage=3, deflate=True)); out.close()
    hechos.append(f["id"]); print(f["id"], round(dp.stat().st_size / 1e6, 1), "MB", flush=True)
print(len(hechos), "recortados:", " ".join(hechos))
