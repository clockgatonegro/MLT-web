"""Piezas gráficas (invitaciones, afiches, banners) de exposiciones sin programa de mano.

Entrada: data/piezas_fuentes.csv (id_expo, tipo, ruta relativa a MLT_ORIGINALES), aprobadas por los autores.
Salida:  programas/piezas/<id>.jpg (imagen completa, lado mayor 2000 px) y programas/portadas/<id>.jpg
Uso:     MLT_ORIGINALES=<raíz> uv run --with pymupdf --with pillow python scripts/piezas.py
"""
import csv, io, os
from pathlib import Path
import fitz
from PIL import Image
RAIZ = Path(__file__).resolve().parent.parent
ORIG = Path(os.environ.get("MLT_ORIGINALES", "/Volumes/Mackup/Proyectos"))
PZ, PORT = RAIZ / "programas/piezas", RAIZ / "programas/portadas"
PZ.mkdir(parents=True, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None
for f in csv.DictReader(open(RAIZ / "data/piezas_fuentes.csv", encoding="utf-8")):
    src = ORIG / f["ruta"]; i = f["id_expo"].replace(".", "")
    if src.suffix.lower() in (".pdf", ".ai"):
        pg = fitz.open(src, filetype="pdf")[0]
        if pg.trimbox.width < pg.mediabox.width - 1: pg.set_cropbox(pg.trimbox)   # a ras, sin marcas de corte
        z = 2000 / max(pg.rect.width, pg.rect.height)
        pm = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
        im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    else:
        im = Image.open(src)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert("RGB")
    im.thumbnail((2000, 2000)); (PZ / f"{i}.jpg").write_bytes(b"")
    b = io.BytesIO(); im.save(b, "JPEG", quality=82, optimize=True); (PZ / f"{i}.jpg").write_bytes(b.getvalue())
    t = im.copy(); t.thumbnail((520, 720)); b = io.BytesIO(); t.save(b, "JPEG", quality=82, optimize=True); (PORT / f"{i}.jpg").write_bytes(b.getvalue())
    print(i, f["tipo"], im.size, round(len(b.getvalue()) / 1e3), "kB portada", flush=True)
