"""Programas de mano y catálogos enlazados a las exposiciones.

Entrada:  data/programas_fuentes.csv  (cruce hecho a mano: exposición, archivo original, recorte de portada)
          Los originales están en el disco Mackup (variable MLT_ORIGINALES, por defecto /Volumes/Mackup/Proyectos);
          los de origen «web» se bajan de la URL que trae la columna ruta.
Salida:   programas/pdf/<id>.pdf        copia liviana para la web
          programas/portadas/<id>.jpg   portada
          data/programas.csv            un renglón por programa y exposición
          index.html y scripts/plantilla.html, con el índice de programas entre /*PROGRAMAS*/ y /*FIN*/

Uso:      uv run --with pymupdf --with pillow python scripts/programas.py [--solo-web]
          --solo-web no toca PDF ni portadas: solo reescribe data/programas.csv y las páginas.
"""
import csv, io, json, os, re, shutil, sys, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIG = Path(os.environ.get("MLT_ORIGINALES", "/Volumes/Mackup/Proyectos"))
PDF, PORT = RAIZ / "programas/pdf", RAIZ / "programas/portadas"
LADO_ESC, CAL_ESC = 1400, 58      # escaneados: lado mayor en px y calidad JPEG
LADO_DIG, CAL_DIG = 2600, 72      # digitales pesados que se rasterizan
MAX_DIG = 6e6                     # los digitales de menos de 6 MB se copian tal cual


def ids(filas):
    """ex.154 -> ex154; si una exposición tiene varios programas: ex154a, ex154b…"""
    n = {}
    for f in filas:
        n[f["id_expo"].split(";")[0]] = n.get(f["id_expo"].split(";")[0], 0) + 1
    k = {}
    for f in filas:
        e = f["id_expo"].split(";")[0]
        k[e] = k.get(e, 0) + 1
        f["id"] = e.replace(".", "") + ("abcdefgh"[k[e] - 1] if n[e] > 1 else "")


def raster(doc, lado, cal):
    import fitz
    from PIL import Image
    out = fitz.open()
    for pg in doc:
        z = lado / max(pg.rect.width, pg.rect.height)
        pm = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
        b = io.BytesIO()
        Image.frombytes("RGB", (pm.width, pm.height), pm.samples).save(b, "JPEG", quality=cal, optimize=True)
        out.new_page(width=pg.rect.width, height=pg.rect.height).insert_image(pg.rect, stream=b.getvalue())
    return out


def portada(doc, recorte, destino):
    import fitz
    from PIL import Image
    pg = doc[0]
    z = 1600 / max(pg.rect.width, pg.rect.height)
    pm = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
    im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    if recorte:
        x0, y0, x1, y1, giro = [float(v) for v in recorte.split()]
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
        if giro:
            im = im.rotate(giro, expand=True)
    im.thumbnail((520, 720))
    im.save(destino, "JPEG", quality=82, optimize=True)


def generar(filas):
    import fitz
    PDF.mkdir(parents=True, exist_ok=True); PORT.mkdir(parents=True, exist_ok=True)
    for f in filas:
        src, dp, dj = ORIG / f["ruta"], PDF / (f["id"] + ".pdf"), PORT / (f["id"] + ".jpg")
        if dp.exists() and dj.exists():
            continue
        if f["origen"] == "web":      # la ruta es una URL: se baja tal cual
            req = urllib.request.Request(f["ruta"], headers={"User-Agent": "Mozilla/5.0"})
            dp.write_bytes(urllib.request.urlopen(req, timeout=120).read())
            portada(fitz.open(dp), f["recorte"], dj)
            print(f["id"], f["paginas"], "pág.", round(dp.stat().st_size / 1e6, 1), "MB", flush=True)
            continue
        doc = fitz.open(src, filetype="pdf")
        portada(doc, f["recorte"], dj)
        if f["origen"] == "digital" and src.stat().st_size <= MAX_DIG and src.suffix.lower() == ".pdf":
            shutil.copyfile(src, dp)
        else:
            out = raster(doc, LADO_ESC if f["origen"] == "escaneado" else LADO_DIG, CAL_ESC if f["origen"] == "escaneado" else CAL_DIG)
            out.save(dp, garbage=3, deflate=True); out.close()
        print(f["id"], f["paginas"], "pág.", round(dp.stat().st_size / 1e6, 1), "MB", flush=True)


def tipo(f):
    if f["origen"] in ("digital", "web"):
        return "programa de mano"
    return "catálogo" if int(f["paginas"]) > 6 else "programa de mano"


def main():
    filas = [f for f in csv.DictReader(open(RAIZ / "data/programas_fuentes.csv", encoding="utf-8")) if f["id_expo"]]
    ids(filas)
    if "--solo-web" not in sys.argv:
        generar(filas)
    expos = {e["Id"]: e for e in csv.DictReader(open(RAIZ / "data/exposiciones.csv", encoding="utf-8"))}
    indice, tabla = {}, []
    for f in filas:
        dp = PDF / (f["id"] + ".pdf")
        if not dp.exists():
            print("FALTA", f["id"]); continue
        mb = round(dp.stat().st_size / 1e6, 1)
        for e in f["id_expo"].split(";"):
            indice.setdefault(e, []).append([f["id"], int(f["paginas"]), mb, tipo(f)])
            tabla.append(dict(id_programa=f["id"], id_expo=e, exposicion=expos[e]["Label"], ano=expos[e]["ano"], tipo=tipo(f),
                              paginas=f["paginas"], mb=mb, pdf=f"programas/pdf/{f['id']}.pdf", portada=f"programas/portadas/{f['id']}.jpg",
                              origen=f["origen"], confianza=f["confianza"], archivo_original=f["ruta"].split("/")[-1]))
    with open(RAIZ / "data/programas.csv", "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(tabla[0])); w.writeheader(); w.writerows(tabla)
    js = json.dumps(indice, ensure_ascii=False, separators=(",", ":"))
    for p in ("index.html", "scripts/plantilla.html"):
        t = (RAIZ / p).read_text(encoding="utf-8")
        t2, n = re.subn(r"/\*PROGRAMAS\*/.*?/\*FIN\*/", lambda m: "/*PROGRAMAS*/" + js + "/*FIN*/", t, flags=re.S)
        if not n:
            sys.exit(f"{p}: falta el marcador /*PROGRAMAS*/…/*FIN*/")
        (RAIZ / p).write_text(t2, encoding="utf-8")
    print(len(filas), "programas,", len(indice), "exposiciones,", round(sum(r["mb"] for r in {r["id_programa"]: r for r in tabla}.values())), "MB en total")


if __name__ == "__main__":
    main()
