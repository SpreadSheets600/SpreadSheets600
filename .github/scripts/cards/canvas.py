"""Canvas + shared SVG drawing primitives.

All cards share one canvas engine so spacing, borders, radii and animations
stay identical everywhere.
"""

import math

from .icons import icon
from .theme import PANEL, LINE, TRACK, LIVE, BLUE, PURPLE, RADIUS, STYLE
from .util import tx

# Only two canvas widths exist; every builder uses one of them.
FULL_W = 830
HALF_W = 410


def rect(x, y, w, h, fill, rx=0, stroke=None, extra=""):
    st = f' stroke="{stroke}"' if stroke else ""
    if rx > 6 and h > 28 and fill in (PANEL, TRACK):
        rx = 6
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{max(h, 0):.1f}" '
        f'rx="{rx}" fill="{fill}"{st} {extra}/>'
    )


def line(x1, y1, x2, y2, stroke=TRACK):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}"/>'


def hbar(x, y, w, frac, color, h=6):
    frac = max(0.0, min(1.0, frac))
    out = rect(x, y, w, h, TRACK, h / 2)
    if frac > 0:
        out += rect(x, y, max(w * frac, h), h, color, h / 2)
    return out


def ring(cx, cy, r, sw, frac, stroke="url(#ac)"):
    frac = max(0.0, min(1.0, frac))
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{TRACK}" stroke-width="{sw}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" '
        f'pathLength="100" stroke-dasharray="{frac * 100:.2f} 100" transform="rotate(-90 {cx} {cy})"/>'
    )


def donut(cx, cy, r, sw, parts, gap=0.6):
    """parts: [(percent, color)] summing to ~100"""
    out, off = (
        [f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{TRACK}" stroke-width="{sw}"/>'],
        0.0,
    )
    for p, color in parts:
        if p <= 0:
            continue
        seg = max(p - gap, 0.2)
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{color}" stroke-width="{sw}" pathLength="100" '
            f'stroke-dasharray="{seg:.3f} {100 - seg:.3f}" stroke-dashoffset="{-off:.3f}" '
            f'transform="rotate(-90 {cx} {cy})"/>'
        )
        off += p
    return "".join(out)


def spark(x, y, w, h, vals):
    if len(vals) < 2:
        return ""
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1
    pts = [
        (x + i * w / (len(vals) - 1), y + h - (v - lo) / span * h)
        for i, v in enumerate(vals)
    ]
    line_ = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{line_} L{x + w:.1f},{y + h:.1f} L{x:.1f},{y + h:.1f} Z"
    lx, ly = pts[-1]
    return (
        f'<path d="{area}" fill="url(#fillv)"/><path d="{line_}" stroke="url(#ac)" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3.2" fill="#f2f2f2" stroke="#a6a9ad" stroke-width="2"/>'
    )


def vbars(x, y, w, h, items, color_fn, label_fn, value_fn, delay=0.0, label_size=9):
    """Vertical bar chart. items: list of (label, value). returns svg string."""
    n = len(items)
    top = max([v for _, v in items] + [1])
    slot = w / n
    bw = min(slot * 0.62, 34)
    out = []
    for i, (lab, v) in enumerate(items):
        bh = max(v / top * h, 2 if v else 1.5)
        bx = x + i * slot + (slot - bw) / 2
        by = y + h - bh
        out.append(
            f'<rect class="bar" style="animation-delay:{delay + i * 0.04:.2f}s" x="{bx:.1f}" y="{by:.1f}" '
            f'width="{bw:.1f}" height="{bh:.1f}" rx="{min(bw / 3, 4):.1f}" fill="{color_fn(i, v, top)}"/>'
        )
        cx_ = x + i * slot + slot / 2
        out.append(tx(cx_, y + h + 13, label_fn(lab), label_size, "#8a8d91", 400, "middle"))
        if v and slot >= 22:
            out.append(tx(cx_, by - 4, value_fn(v), 8.5, "#f2f2f2", 600, "middle"))
    return "".join(out)


def pill(x, y, label, color, on=True, size=10):
    from .util import tw

    w = tw(label, size) + 16
    if on:
        body = (
            rect(x, y, w, 20, color, 10, extra='fill-opacity=".14"')
            + f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="20" rx="10" fill="none" stroke="{color}" stroke-opacity=".5"/>'
        )
        col = color
    else:
        body = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="20" rx="10" fill="none" stroke="{LINE}"/>'
        col = "#8a8d91"
    return body + tx(x + w / 2, y + 13.5, label, size, col, 600, "middle"), w


def flow(x0, y0, maxw, items, size=10, rowh=26):
    """Lay out (label, color) chips in wrapping rows. Returns (svg, next_y)."""
    from .util import tw

    out, x, y = [], x0, y0
    for label, color in items:
        w = tw(label, size) + 16
        if x + w > x0 + maxw:
            x, y = x0, y + rowh
        chip, _ = pill(x, y, label, color, True, size)
        out.append(chip)
        x += w + 6
    return "".join(out), y + rowh


class Canvas:
    def __init__(self, w, h, title, c1=BLUE, c2=PURPLE):
        self.w, self.h, self.title = w, h, title
        self.c1, self.c2 = c1, c2
        self.defs, self.parts, self._n = [], [], 0

    def uid(self, prefix="u"):
        self._n += 1
        return f"{prefix}{self._n}"

    def add(self, s, delay=None):
        self.parts.append(
            s
            if delay is None
            else f'<g class="a" style="animation-delay:{delay:.2f}s">{s}</g>'
        )

    def header(self, title, ico, sub=None):
        self.add(
            icon(ico, 20, 16, 17, self.c1, 1.6)
            + tx(44, 29, title, 14, "#f2f2f2", 700)
            + (tx(self.w - 20, 29, sub, 11, "#a6a9ad", 400, "end") if sub else "")
        )

    def clip_img(self, href, x, y, w, h, r, fallback_text=""):
        """Rounded image (or placeholder tile when the download failed)."""
        r = min(r, 6)
        if not href:
            ph = rect(x, y, w, h, TRACK, r)
            if fallback_text:
                ph += tx(
                    x + w / 2,
                    y + h / 2 + 5,
                    fallback_text[:1].upper(),
                    min(h * 0.45, 22),
                    "#a6a9ad",
                    700,
                    "middle",
                )
            return ph
        cid = self.uid("cl")
        self.defs.append(
            f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
        )
        return (
            f'<image href="{href}" xlink:href="{href}" x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>'
        )

    def render(self):
        w, h = self.w, int(math.ceil(self.h))
        defs = (
            f'<linearGradient id="bgg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101010"/>'
            f'<stop offset="1" stop-color="{PANEL}"/></linearGradient>'
            f'<linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{LIVE}"/>'
            f'<stop offset="1" stop-color="#a6a9ad"/></linearGradient>'
            f'<linearGradient id="acv" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{LIVE}"/>'
            f'<stop offset="1" stop-color="{LIVE}"/></linearGradient>'
            f'<linearGradient id="fillv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LIVE}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{LIVE}" stop-opacity="0"/></linearGradient>'
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{self.title}">'
            f"<title>{self.title}</title><defs>{defs}{''.join(self.defs)}</defs><style>{STYLE}</style>"
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{RADIUS}" fill="url(#bgg)" stroke="{LINE}"/>'
            f"{''.join(self.parts)}"
            f"</svg>"
        )
