"""Contribution streak card (half width, 410 x 392)."""

from ..canvas import Canvas, HALF_W, rect, line, icon, tx, ring, spark, flow
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM, BLUE, ORANGE, YELLOW, GREEN, PURPLE, PALETTE
from ..util import num, fmt, pct, parse_dt, fdate, rel_secs


PAIR_H = 392


def build_streak(d, ctx):
    c = Canvas(HALF_W, PAIR_H, "Contribution streak")
    c.add(rect(16, 48, 105, 132, PANEL, 6, LINE))
    c.add(rect(132, 48, 262, 132, PANEL, 6, LINE))
    c.add(rect(16, 192, 378, 96, PANEL, 6, LINE))
    c.add(rect(16, 296, 378, 48, PANEL, 6, LINE))
    c.header("Streak & Rhythm", "flame", None)

    cal = d.get("calendar") or {}
    cur = num(d.get("currentStreak", cal.get("currentStreak")))
    best = num(d.get("longestStreak", cal.get("longestStreak")))
    days = cal.get("contributionDays", [])
    active = num(d.get("activeDays", cal.get("activeDays")))
    tracked = num(cal.get("days", len(days)))
    bd = d.get("bestDay") or cal.get("bestDay") or {}

    c.defs.append(
        f'<linearGradient id="fl" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{ORANGE}"/>'
        f'<stop offset="1" stop-color="{YELLOW}"/></linearGradient>'
    )
    c.add(
        ring(76, 108, 44, 9, cur / best if best else 0, "url(#fl)")
        + icon("flame", 67, 70, 18, ORANGE, 1.8)
        + tx(76, 116, fmt(cur), 28, TEXT, 800, "middle")
        + tx(76, 132, "day streak", 9.5, MUTED, 400, "middle")
        + tx(
            76,
            172,
            f"{cur / best * 100 if best else 0:.0f}% of best",
            9,
            DIM,
            400,
            "middle",
        ),
    )

    rows = [
        ("trophy", "Longest streak", f"{fmt(best)} days", YELLOW),
        (
            "bolt",
            "Best day",
            f"{fmt(bd.get('count', 0))} commits · {fdate(bd.get('date'))}",
            ORANGE,
        ),
        (
            "calendar",
            "Active days",
            f"{fmt(active)} / {fmt(tracked)}  ({pct(active, tracked):.0f}%)",
            GREEN,
        ),
        (
            "chart",
            "Average / day",
            fmt(d.get("averagePerDay", cal.get("averagePerDay", 0))),
            BLUE,
        ),
    ]
    out = []
    for i, (ico, label, val, col) in enumerate(rows):
        y = 64 + i * 31
        out.append(
            icon(ico, 150, y - 10, 14, col)
            + tx(172, y - 2, label, 9.5, MUTED)
            + tx(172, y + 12, val, 12.5, TEXT, 700)
        )
    c.add("".join(out))

    c.add(line(20, 188, HALF_W - 20, 188, TRACK))
    last = [num(x.get("count")) for x in days[-30:]]
    c.add(
        tx(20, 208, "Last 30 days", 10, MUTED, 600)
        + tx(HALF_W - 20, 208, f"{fmt(sum(last))} contributions", 10, MUTED, 400, "end")
    )
    top = max(last + [1])
    n, bw, gp = len(last), 9.4, 3.0
    out = []
    for i, v in enumerate(last):
        h = max(v / top * 44, 2)
        fill = "url(#acv)" if v else TRACK
        out.append(
            f'<rect class="bar" style="animation-delay:{0.2 + i * 0.015:.3f}s" '
            f'x="{20 + i * (bw + gp):.1f}" y="{222 + 44 - h:.1f}" width="{bw}" height="{h:.1f}" rx="2.5" '
            f'fill="{fill}"/>'
        )
    c.add("".join(out))
    c.add(
        tx(20, 280, "30d ago", 8.5, DIM)
        + tx(HALF_W - 20, 280, "today", 8.5, DIM, 400, "end")
    )

    wk, we = (
        num(d.get("weekdayContributions", cal.get("weekdayContributions"))),
        num(d.get("weekendContributions", cal.get("weekendContributions"))),
    )
    tot = (wk + we) or 1
    bw_ = HALF_W - 40
    c.add(
        tx(20, 304, f"Weekdays {fmt(wk)} ({wk / tot * 100:.0f}%)", 10, MUTED)
        + tx(
            HALF_W - 20,
            304,
            f"Weekends {fmt(we)} ({we / tot * 100:.0f}%)",
            10,
            MUTED,
            400,
            "end",
        )
        + rect(20, 311, bw_, 10, PURPLE, 5)
        + rect(20, 311, bw_ * wk / tot, 10, BLUE, 5)
        + rect(20 + bw_ * wk / tot - 5, 311, 6, 10, BLUE, 0),
    )

    yrs = d.get("contributionYears") or []
    if yrs:
        c.add(tx(20, 338, "Contribution years", 10, MUTED, 600))
        svg, _ = flow(
            20,
            348,
            bw_,
            [(str(y), PALETTE[i % len(PALETTE)]) for i, y in enumerate(sorted(yrs))],
            10,
            rowh=22,
        )
        c.add(svg)
    return c.render()
