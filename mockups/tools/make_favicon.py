"""Render the circuit-brain mark into the site's favicon set.

The mark in assets/mark.svg is line art: twenty-odd small circles joined by thin traces,
drawn at a stroke 2% of its width. That is right on a page at 40 px and upward, and it is
mush at 16. So this does not scale one drawing down -- it draws the mark once per target
size with the stroke thickened to suit, which is ordinary optical sizing for an icon.

The tile is deliberately opaque: the site's own --deep (#010a08) behind the accent teal
(#14b899). A transparent icon takes the browser's chrome color, and in dark mode that is
a mid grey the teal nearly vanishes against. An opaque near-black tile carries its own
contrast and reads on light and dark chrome alike.

    python tools/make_favicon.py             # write static/favicon.ico + the PNGs
    python tools/make_favicon.py --check     # also write a magnified contact sheet

Writes static/favicon.ico (16/32/48), static/favicon-32.png, static/favicon-180.png
(apple-touch), and with --check, tools/favicon_check.png. Nothing bigger: a 512 px icon
is only read from a web app manifest, and this site has none.
"""
import argparse
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MARK = ROOT / "assets/mark.svg"
STATIC = ROOT / "static"

DEEP = "#010a08"        # palette teal --deep
TEAL = "#14b899"        # palette teal --accent

SS = 8                  # supersample factor before the final downsample
PAD = 0.10              # blank margin, as a fraction of the tile

# Stroke width per target size, as a fraction of the tile, chosen by eye from the sweep
# --check prints. Large sizes stay near the proportions the mark is actually drawn at and
# show the circuit. 32 is the size a HiDPI browser tab uses and is the one to get right:
# 0.048 keeps the traces separate and legible.
#
# 16 is a different problem. There is no stroke at which twenty circles and their traces
# survive 16 px -- the middle of the range just turns the mark into speckle that reads as
# a compression artifact. So 16 goes deliberately the other way, fat enough to close into
# a clean brain silhouette. An intentional silhouette beats a faithful smudge.
STROKE = {16: 0.090, 32: 0.048, 48: 0.046, 180: 0.042}

ICO_SIZES = (16, 32, 48)


def load_mark():
    """(vertices, codes, viewBox) for the single path in mark.svg."""
    s = MARK.read_text(encoding="utf-8")
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    d = re.search(r'\bd="([^"]*)"', s).group(1)

    verts, codes = [], []
    for cm in re.finditer(r"([MLCZ])([^MLCZ]*)", d):
        cmd = cm.group(1)
        ns = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", cm.group(2))]
        pts = [(ns[i], ns[i + 1]) for i in range(0, len(ns) - 1, 2)]
        if cmd == "M":
            verts.append(pts[0])
            codes.append(MPath.MOVETO)
            for q in pts[1:]:
                verts.append(q)
                codes.append(MPath.LINETO)
        elif cmd == "L":
            for q in pts:
                verts.append(q)
                codes.append(MPath.LINETO)
        elif cmd == "C":
            for i in range(0, len(pts) - 2, 3):
                verts.extend(pts[i:i + 3])
                codes.extend([MPath.CURVE4] * 3)
        elif cmd == "Z":
            verts.append((0.0, 0.0))
            codes.append(MPath.CLOSEPOLY)
    return verts, codes, vb


def render(size: int, stroke: float, verts, codes, vb) -> Image.Image:
    """One square tile at `size` px, drawn at SS x and downsampled."""
    n = size * SS
    dpi = 100
    fig = plt.figure(figsize=(n / dpi, n / dpi), dpi=dpi, facecolor=DEEP)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(DEEP)

    # matplotlib points -> device pixels at this dpi
    lw_pt = stroke * n * 72.0 / dpi
    ax.add_patch(PathPatch(MPath(verts, codes), fill=False, ec=TEAL, lw=lw_pt,
                           joinstyle="round", capstyle="round"))

    # square the viewBox about its center, then pad, so the mark is not stretched
    x0, y0, x1, y1 = vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    half = max(x1 - x0, y1 - y0) / 2 / (1 - 2 * PAD)
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy + half, cy - half)        # SVG y runs down
    ax.set_aspect("equal")
    ax.axis("off")

    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    im = Image.frombuffer("RGBA", fig.canvas.get_width_height(), buf, "raw", "RGBA", 0, 1)
    plt.close(fig)
    return im.convert("RGB").resize((size, size), Image.LANCZOS)


def main(argv):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true",
                   help="also write tools/favicon_check.png, magnified for eyeballing")
    p.add_argument("--stroke", type=float, default=None,
                   help="override the per-size stroke fraction, for experimenting")
    args = p.parse_args(argv)

    verts, codes, vb = load_mark()
    STATIC.mkdir(exist_ok=True)
    tiles = {s: render(s, args.stroke or STROKE[s], verts, codes, vb)
             for s in sorted(set(list(STROKE) + list(ICO_SIZES)))}

    ico = STATIC / "favicon.ico"
    tiles[max(ICO_SIZES)].save(ico, format="ICO",
                               sizes=[(s, s) for s in ICO_SIZES])
    print(f"  {ico.name:20s} {ico.stat().st_size / 1024:5.1f} KB  "
          f"{'/'.join(str(s) for s in ICO_SIZES)}")
    for s, name in ((32, "favicon-32.png"), (180, "favicon-180.png")):
        q = STATIC / name
        tiles[s].save(q, format="PNG", optimize=True)
        print(f"  {name:20s} {q.stat().st_size / 1024:5.1f} KB  {s}x{s}")

    if args.check:
        order = [16, 32, 48, 180]
        fig, axs = plt.subplots(2, len(order), figsize=(2.6 * len(order), 5.6), dpi=130)
        for col, s in enumerate(order):
            # top row: shown at the pixel size a browser actually uses
            axs[0, col].imshow(tiles[s], interpolation="nearest")
            axs[0, col].set_title(f"{s} px, magnified", fontsize=9)
            # bottom row: the same tile on the two chrome colors it has to survive
            for i, bg in enumerate(("#f2f2f2", "#202124")):
                strip = Image.new("RGB", (60, 30), bg)
                strip.paste(tiles[s].resize((22, 22), Image.LANCZOS), (19, 4))
                axs[1, col].imshow(strip, extent=(0, 60, 30 * i, 30 * (i + 1)),
                                   interpolation="nearest")
            axs[1, col].set_xlim(0, 60)
            axs[1, col].set_ylim(0, 60)
            axs[1, col].set_title("on light / dark chrome", fontsize=9)
        for ax in axs.ravel():
            ax.axis("off")
        fig.tight_layout()
        out = Path(__file__).resolve().parent / "favicon_check.png"
        fig.savefig(out, facecolor="white")
        print(f"  {out.name} written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
