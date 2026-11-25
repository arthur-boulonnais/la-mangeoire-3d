#!/usr/bin/env python3
"""
Extraction du catalogue Atelier Paris (usage interne, rien n'est publié).

  python3 scripts/extract-catalogue.py [--pdf source/catalogue-paris.pdf] [--out source/extracted]

Produit :
  source/extracted/page-<n>.png          rendu HD de chaque page (analyse coloris / mise en page)
  source/extracted/p<n>/lifestyle.<ext>  la plus grande image de la page (photo portée)
  source/extracted/p<n>/packshot-<i>.<ext> images moyennes (packshots à plat)
  source/extracted/p<n>/swatches.json    pastilles de couleur détectées (tracés vectoriels + texte voisin)
  source/extracted/index.json            récapitulatif

Ignorés : le petit logo de l'imprimeur (~195×97 px, répété sur chaque page) et les bandeaux
de pastilles (images très allongées).
"""
import argparse
import json
import pathlib
import sys

try:
    import pymupdf as fitz
except ImportError:
    sys.exit("PyMuPDF manquant : pip install pymupdf")

LOGO_SIZE = (195, 97)
LOGO_TOL = 0.15


def is_logo(w, h):
    lw, lh = LOGO_SIZE
    return abs(w - lw) / lw < LOGO_TOL and abs(h - lh) / lh < LOGO_TOL


def is_strip(w, h):
    ratio = max(w, h) / max(1, min(w, h))
    return ratio > 4.5  # bandeau de pastilles


def hexcolor(rgb):
    return "#{:02X}{:02X}{:02X}".format(*(round(c * 255) for c in rgb[:3]))


def detect_swatches(page):
    """Pastilles = petites formes remplies, à peu près carrées (cercles ou carrés)."""
    out = []
    words = page.get_text("words")  # (x0, y0, x1, y1, text, ...)
    for d in page.get_drawings():
        fill = d.get("fill")
        if not fill:
            continue
        r = d["rect"]
        if not (6 <= r.width <= 70 and 6 <= r.height <= 70):
            continue
        if abs(r.width - r.height) > 0.25 * max(r.width, r.height):
            continue
        # texte le plus proche sous ou à droite de la pastille (noms de coloris)
        label = None
        best = 1e9
        for x0, y0, x1, y1, t, *_ in words:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            dx, dy = cx - (r.x0 + r.x1) / 2, cy - (r.y0 + r.y1) / 2
            if -5 < dy < 40 and abs(dx) < 60 or (0 < dx < 120 and abs(dy) < 12):
                dist = abs(dx) + abs(dy)
                if dist < best:
                    best, label = dist, t
        out.append({"hex": hexcolor(fill), "bbox": [round(v, 1) for v in r], "label": label})
    # dédoublonnage (même couleur, même position)
    seen, uniq = set(), []
    for s in sorted(out, key=lambda s: (s["bbox"][1], s["bbox"][0])):
        key = (s["hex"], round(s["bbox"][0]), round(s["bbox"][1]))
        if key not in seen:
            seen.add(key)
            uniq.append(s)
    return uniq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default="source/catalogue-paris.pdf")
    ap.add_argument("--out", default="source/extracted")
    ap.add_argument("--zoom", type=float, default=2.5, help="facteur de rendu des pages")
    args = ap.parse_args()

    pdf = pathlib.Path(args.pdf)
    if not pdf.exists():
        sys.exit(f"Catalogue introuvable : {pdf}")
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf)
    index = []
    for pno in range(doc.page_count):
        n = pno + 1
        page = doc[pno]
        page.get_pixmap(matrix=fitz.Matrix(args.zoom, args.zoom)).save(out / f"page-{n}.png")

        pdir = out / f"p{n}"
        pdir.mkdir(exist_ok=True)
        imgs = []
        for info in page.get_images(full=True):
            xref = info[0]
            try:
                base = doc.extract_image(xref)
            except Exception:
                continue
            w, h = base["width"], base["height"]
            if is_logo(w, h) or is_strip(w, h) or w * h < 150 * 150:
                continue
            rects = page.get_image_rects(xref)
            imgs.append({"xref": xref, "w": w, "h": h, "ext": base["ext"], "data": base["image"],
                         "rect": [round(v, 1) for v in rects[0]] if rects else None})

        imgs.sort(key=lambda i: i["w"] * i["h"], reverse=True)
        saved = []
        for i, im in enumerate(imgs):
            name = "lifestyle" if i == 0 and len(imgs) > 1 else f"packshot-{i if len(imgs) > 1 else 1}"
            fname = f"{name}.{im['ext']}"
            (pdir / fname).write_bytes(im["data"])
            saved.append({"file": f"p{n}/{fname}", "w": im["w"], "h": im["h"], "rect": im["rect"]})

        sw = detect_swatches(page)
        (pdir / "swatches.json").write_text(json.dumps(sw, ensure_ascii=False, indent=2))
        index.append({"page": n, "images": saved, "swatches": len(sw), "text": page.get_text()[:400]})
        print(f"page {n:>2}: {len(saved)} images, {len(sw)} pastilles")

    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2))
    print(f"→ {out}/index.json")


if __name__ == "__main__":
    main()
