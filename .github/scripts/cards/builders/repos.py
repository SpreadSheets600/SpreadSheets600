"""Top repositories card (full width, 830 wide, height fits content)."""

from ..canvas import Canvas, FULL_W, rect, line, icon, tx, hbar, flow
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM, BLUE, PURPLE, ORANGE, YELLOW, PALETTE
from ..util import num, fmt, fit, parse_dt, rel_secs, size_from_kb, fdate, tw


def build_repos(d, ctx):
    c = Canvas(FULL_W, 440, "Top repositories")
    c.header(
        "Top Repositories",
        "repo",
        f"{fmt(d.get('repos'))} repos · {fmt(d.get('stars'))} ★ · {fmt(d.get('forks'))} forks",
    )
    out = []
    for i, r in enumerate(d.get("topRepos") or []):
        y = 56 + i * 54
        out.append(
            rect(20, y, 520, 46, PANEL, 9, TRACK)
            + icon("repo", 32, y + 9, 14, BLUE)
            + tx(54, y + 20, r.get("name", ""), 13, BLUE, 700)
            + tx(
                54 + tw(r.get("name", ""), 13) + 8,
                y + 20,
                "archived" if r.get("isArchived") else "",
                9,
                ORANGE,
            )
            + tx(
                54,
                y + 37,
                fit(r.get("description") or "No description", 300, 10.5),
                10.5,
                MUTED,
            )
        )
        lx = 360
        if r.get("language"):
            out.append(
                f'<circle cx="{lx + 4}" cy="{y + 36}" r="4" fill="{r.get("languageColor") or MUTED}"/>'
                + tx(lx + 13, y + 40, r["language"], 10, MUTED)
            )
        out.append(
            icon("star", 463, y + 10, 12, YELLOW)
            + tx(479, y + 20, fmt(r.get("stars")), 11, TEXT, 700)
            + icon("fork", 463, y + 27, 12, MUTED)
            + tx(479, y + 37, fmt(r.get("forks")), 11, TEXT, 700)
        )
        if r.get("pushedAt"):
            out.append(
                tx(
                    362 + 62,
                    y + 20,
                    "pushed "
                    + rel_secs((ctx.now - parse_dt(r["pushedAt"])).total_seconds()),
                    9.5,
                    DIM,
                    400,
                    "end",
                )
            )
    c.add("".join(out))

    # facts column
    fx = 566
    c.add(rect(558, 48, FULL_W - 574, 276, PANEL, 6, LINE))
    c.add(line(556, 52, 556, 318, LINE))
    facts = [
        ("disk", "All repos disk", size_from_kb(d.get("totalDiskUsage"))),
        ("disk", "Owned repos disk", size_from_kb(d.get("repoDiskUsage"))),
        ("lock", "Private repos", fmt(d.get("private"))),
        (
            "layers",
            "Archived / templates",
            f"{fmt(d.get('archived'))} / {fmt(d.get('templates'))}",
        ),
    ]
    lp, old, new = (
        d.get("lastPushed") or {},
        d.get("oldestRepo") or {},
        d.get("newestRepo") or {},
    )
    out = []
    for i, (ico, lab, val) in enumerate(facts):
        y = 66 + i * 26
        out.append(
            icon(ico, fx, y - 10, 13, DIM)
            + tx(fx + 20, y, lab, 10.5, MUTED)
            + tx(FULL_W - 22, y, val, 11, TEXT, 700, "end")
        )
    y = 66 + len(facts) * 26 + 6
    for lab, ico, rr, key in (
        ("Last push", "bolt", lp, "pushedAt"),
        ("Oldest repo", "clock", old, "createdAt"),
        ("Newest repo", "star", new, "createdAt"),
    ):
        if not rr:
            continue
        nm = str(rr.get("name", "")).split("/")[-1]
        out.append(
            icon(ico, fx, y - 10, 13, DIM)
            + tx(fx + 20, y, lab, 10.5, MUTED)
            + tx(FULL_W - 22, y, fit(nm, 130, 11), 11, TEXT, 700, "end")
            + tx(FULL_W - 22, y + 13, fdate(rr.get(key)), 9, DIM, 400, "end")
        )
        y += 34
    c.add("".join(out))

    lic = d.get("licenses") or []
    if lic:
        mx = max(num(l["repos"]) for l in lic) or 1
        out = [tx(fx, y + 6, "Licenses", 10, MUTED, 600)]
        y += 20
        for i, l in enumerate(lic):
            out.append(
                tx(fx, y, fit(l["name"], 150, 10), 10, TEXT)
                + tx(FULL_W - 22, y, fmt(l["repos"]), 10, MUTED, 700, "end")
                + hbar(
                    fx, y + 5, FULL_W - 22 - fx, num(l["repos"]) / mx, PALETTE[i % 8], 4
                )
            )
            y += 24
        c.add("".join(out))

    topics = d.get("topics") or []
    ty = 338
    c.add(
        line(20, ty - 14, FULL_W - 20, ty - 14, TRACK)
    )
    c.add(
        icon("tag", 20, ty - 4, 13, MUTED)
        + tx(
            40,
            ty + 7,
            f"Top topics · {fmt(d.get('topicCount', len(topics)))} unique · "
            f"{fmt(d.get('topicOccurrences', 0))} uses",
            10.5,
            MUTED,
            600,
        )
    )
    svg, endy = flow(
        20,
        ty + 18,
        FULL_W - 40,
        [(f"{t['name']} · {t['repos']}", PALETTE[i % 8]) for i, t in enumerate(topics)],
        10,
    )
    c.add(svg)
    c.h = endy + 14
    return c.render()
