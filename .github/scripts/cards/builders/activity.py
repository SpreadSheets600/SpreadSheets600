"""Contribution activity card (full width, 830 x 360)."""

from ..canvas import Canvas, FULL_W, rect, line, icon, tx, vbars
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM, CYAN, BLUE, PURPLE, HEAT
from ..util import num, fmt, compact, parse_dt, fdate as fmt_date


def build_activity(d, ctx):
    c = Canvas(FULL_W, 360, "Contribution activity")
    cal = d.get("calendar") or {}
    days = cal.get("contributionDays", [])
    c.add(rect(16, 48, FULL_W - 32, 144, PANEL, 6, LINE))
    c.add(rect(16, 198, 496, 145, PANEL, 6, LINE))
    if len(d.get("weekdayCounts") or cal.get("weekdayCounts") or []) == 7:
        c.add(rect(526, 198, FULL_W - 542, 145, PANEL, 6, LINE))
    c.header(
        "Contribution Activity",
        "calendar",
        f"{fmt(cal.get('total', d.get('contributions', 0)))} contributions · "
        f"{fmt_date(cal.get('firstDay'))} → {fmt_date(cal.get('lastDay'))}",
    )
    if not days:
        return c.render()

    counts = sorted(num(x["count"]) for x in days if num(x["count"]) > 0) or [1]
    q = lambda p: counts[min(int(len(counts) * p), len(counts) - 1)]
    t1, t2, t3 = q(0.25), q(0.5), q(0.75)

    def level(v):
        return 0 if v <= 0 else 1 if v <= t1 else 2 if v <= t2 else 3 if v <= t3 else 4

    first = parse_dt(days[0]["date"] + "T00:00:00+00:00")
    col0 = int(days[0].get("weekday", 0))
    step, cell, x0, y0 = 14, 11, 52, 66
    out, last_label_col = [], -9
    for i, day in enumerate(days):
        col, row = (i + col0) // 7, (i + col0) % 7
        v = num(day["count"])
        out.append(
            f'<rect x="{x0 + col * step}" y="{y0 + row * step}" width="{cell}" height="{cell}" rx="2.5" '
            f'fill="{HEAT[level(v)]}"><title>{day["date"]}: {fmt(v)}</title></rect>'
        )
        if day["date"].endswith("-01") and col - last_label_col >= 3:
            dt = parse_dt(day["date"] + "T00:00:00+00:00")
            out.append(tx(x0 + col * step, y0 - 7, f"{dt:%b}", 9, MUTED))
            last_label_col = col
    for r, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(tx(20, y0 + r * step + 9, lab, 9, MUTED))
    # legend
    lx = FULL_W - 20 - 5 * 14 - 62
    out.append(tx(lx, y0 + 7 * step + 12, "Less", 9, MUTED, 400, "end"))
    for i, col in enumerate(HEAT):
        out.append(rect(lx + 6 + i * 14, y0 + 7 * step + 3, 11, 11, col, 2.5))
    out.append(tx(lx + 6 + 5 * 14 + 4, y0 + 7 * step + 12, "More", 9, MUTED))
    c.add("".join(out))

    # monthly bars
    months = {}
    for day in days:
        key = day["date"][:7]
        months[key] = months.get(key, 0) + num(day["count"])
    mitems = [(parse_dt(k + "-01T00:00:00+00:00"), v) for k, v in months.items()]
    cy = 212
    c.add(line(20, cy - 14, FULL_W - 20, cy - 14, TRACK))
    c.add(tx(20, cy + 4, "Contributions per month", 10.5, MUTED, 600))
    c.add(
        vbars(
            20,
            cy + 26,
            480,
            78,
            [(m, v) for m, v in mitems],
            lambda i, v, top: (
                "url(#acv)" if v == top else "#343434" if i % 2 == 0 else "#252525"
            ),
            lambda m: f"{m:%b}",
            compact,
            0.2,
        )
    )

    # weekday bars (API order is Mon..Sun - checked against weekday/weekend totals)
    wk = d.get("weekdayCounts") or cal.get("weekdayCounts") or []
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if len(wk) == 7:
        c.add(line(528, cy - 6, 528, cy + 126, TRACK))
        c.add(tx(548, cy + 4, "By weekday", 10.5, MUTED, 600))
        c.add(
            vbars(
                548,
                cy + 26,
                258,
                78,
                list(zip(names, [num(v) for v in wk])),
                lambda i, v, top: (
                    "url(#acv)" if v == top else (PURPLE if i >= 5 else BLUE)
                ),
                lambda n: n,
                compact,
                0.3,
            )
        )
    return c.render()
