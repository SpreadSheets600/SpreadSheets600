"""WakaTime coding-time card (half width, 410 wide, height fits content)."""

import math

from ..canvas import Canvas, HALF_W, rect, line, tx, hbar, vbars
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM, CYAN, BLUE, PALETTE
from ..util import num, fmt, hm, parse_dt, fit


PAIR_H = 392


def build_wakatime(d, ctx):
    c = Canvas(HALF_W, PAIR_H, "WakaTime")
    c.add(rect(16, 48, 378, 48, PANEL, 6, LINE))
    c.add(rect(16, 106, 378, 86, PANEL, 6, LINE))
    c.header("Coding Time", "clock", "WakaTime")
    week = num(d.get("weekSeconds"))
    daily = d.get("daily") or []
    c.add(
        tx(20, 70, d.get("total", hm(d.get("totalSeconds"))), 19, TEXT, 800)
        + tx(20, 86, "all-time total", 10, MUTED)
        + tx(HALF_W - 20, 70, hm(week), 23, CYAN, 800, "end")
        + tx(HALF_W - 20, 86, "last 7 days", 10, MUTED, 400, "end")
        + tx(HALF_W / 2 + 52, 70, hm(week / max(len(daily), 1)), 15, TEXT, 700, "middle")
        + tx(HALF_W / 2 + 52, 86, "avg / day", 10, MUTED, 400, "middle"),
    )

    items = []
    for x in daily:
        dt = parse_dt(x["date"] + "T00:00:00+00:00")
        items.append((dt, num(x["seconds"]) / 3600.0))
    if items:
        c.add(line(20, 102, HALF_W - 20, 102, TRACK))
        c.add(
            vbars(
                20,
                130,
                HALF_W - 40,
                52,
                items,
                lambda i, v, top: "url(#acv)" if i == len(items) - 1 else "#303030",
                lambda dt: f"{dt:%a}",
                lambda v: f"{v:.1f}h",
                0.15,
            )
        )

    def block(y, title, rows, color_off):
        tot = sum(num(r["seconds"]) for r in rows) or 1
        out = [tx(20, y, title, 10.5, MUTED, 600)]
        for i, r in enumerate(rows):
            yy = y + 18 + i * 20
            out.append(
                f'<circle cx="24" cy="{yy - 4}" r="3.5" fill="{PALETTE[(i + color_off) % 8]}"/>'
                + tx(34, yy, fit(r["name"], 80, 11), 11, TEXT)
                + hbar(
                    122,
                    yy - 8,
                    170,
                    num(r["seconds"]) / tot,
                    PALETTE[(i + color_off) % 8],
                    6,
                )
                + tx(
                    HALF_W - 20,
                    yy,
                    f"{hm(r['seconds'])} · {num(r['seconds']) / tot * 100:.0f}%",
                    10,
                    MUTED,
                    400,
                    "end",
                )
            )
        return "".join(out), y + 18 + len(rows) * 20

    langs = d.get("languages") or []
    svg, endy = block(208, "Languages · last 7 days", langs, 0)
    c.add(rect(16, 194, HALF_W - 32, max(38, endy - 190), PANEL, 6, LINE))
    c.add(svg)
    c.h = max(c.h, endy + 8)
    eds = d.get("editors") or []
    if eds:
        ey = endy + 12
        tot = sum(num(e["seconds"]) for e in eds) or 1
        c.add(
            rect(
                16,
                ey - 14,
                HALF_W - 32,
                28 + math.ceil(len(eds) / 2) * 26,
                PANEL,
                6,
                LINE,
            )
        )
        c.add(tx(20, ey, "Editors", 10.5, MUTED, 600))
        for i, e in enumerate(eds):
            col, row = i % 2, i // 2
            x, yy = 20 + col * 190, ey + 22 + row * 26
            color = PALETTE[(i + 3) % len(PALETTE)]
            c.add(
                f'<circle cx="{x + 3}" cy="{yy - 4}" r="3" fill="{color}"/>'
                + tx(x + 11, yy, fit(e.get("name", ""), 95, 9.5), 9.5, MUTED)
                + tx(x + 178, yy, hm(e.get("seconds")), 9.5, TEXT, 500, "end")
                + hbar(x, yy + 5, 170, num(e.get("seconds")) / tot, color, 3)
            )
        c.h = max(c.h, ey + 24 + math.ceil(len(eds) / 2) * 26 + 24)
    else:
        c.h = max(c.h, endy + 24)
    return c.render()
