"""Languages card (half width, 410 x 392)."""

from ..canvas import Canvas, HALF_W, rect, line, tx, donut
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM, BLUE, PURPLE, PINK, PALETTE
from ..util import num, fmt, fit, pct


PAIR_H = 392


def build_languages(d, ctx):
    c = Canvas(HALF_W, PAIR_H, "Languages")
    c.add(rect(16, 48, 140, 136, PANEL, 6, LINE))
    c.add(rect(164, 48, 230, 136, PANEL, 6, LINE))
    c.add(rect(16, 198, 378, 178, PANEL, 6, LINE))
    c.header("Languages", "code", "by repository count")
    langs = d.get("languages") or []
    total = sum(num(l.get("repos")) for l in langs) or 1
    parts = [
        (num(l["repos"]) / total * 100, l.get("color") or PALETTE[i % 8])
        for i, l in enumerate(langs)
    ]
    c.add(donut(86, 120, 50, 17, parts))
    c.add(
        tx(86, 123, fmt(total), 21, TEXT, 800, "middle")
        + tx(86, 138, "tagged repos", 8.5, MUTED, 400, "middle"),
    )
    top = d.get("topLanguage") or (langs[0] if langs else None)
    if top:
        col = top.get("color") or BLUE
        c.add(
            tx(170, 84, "TOP LANGUAGE", 9, MUTED, 600, extra='letter-spacing=".8"')
            + f'<circle cx="177" cy="106" r="6" fill="{col}"/>'
            + tx(190, 112, top["name"], 21, TEXT, 800)
            + tx(
                170,
                136,
                f"{fmt(top['repos'])} repos · {fmt(top['stars'])} ★",
                12,
                MUTED,
            )
            + tx(
                170,
                156,
                f"{pct(num(top['repos']), total):.0f}% of tagged repos · {len(langs)} languages",
                10.5,
                DIM,
            ),
        )

    # stacked bar
    bx, bw_ = 20, HALF_W - 40
    c.defs.append(
        f'<clipPath id="sb"><rect x="{bx}" y="188" width="{bw_}" height="9" rx="4.5"/></clipPath>'
    )
    seg, xx = [], bx
    for p, col in parts:
        w = bw_ * p / 100
        seg.append(rect(xx, 188, w + 0.6, 9, col))
        xx += w
    c.add(f'<g clip-path="url(#sb)">{"".join(seg)}</g>')

    out = []
    for i, l in enumerate(langs[:16]):
        col_i, row = divmod(i, 8)
        x, y = 20 + col_i * 195, 222 + row * 19.5
        out.append(
            f'<circle cx="{x + 4}" cy="{y - 4}" r="4" fill="{l.get("color") or PALETTE[i % 8]}"/>'
            + tx(x + 14, y, fit(l["name"], 90, 11), 11, TEXT)
            + tx(x + 130, y, fmt(l["repos"]), 11, TEXT, 700, "end")
            + tx(x + 172, y, f"{fmt(l['stars'])} ★", 10, MUTED, 400, "end")
        )
    c.add("".join(out))
    c.add(tx(20, PAIR_H - 10, "repos · stars per language", 9, DIM))
    return c.render()
