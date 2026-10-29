"""GitHub profile card (full width, 830 x 208)."""

import re

from ..canvas import Canvas, FULL_W, rect, line, icon, tx, spark, pill
from ..network import fetch_img
from ..theme import PANEL, LINE, TEXT, MUTED, DIM, BLUE, GREEN, ORANGE, PINK, YELLOW, TRACK
from ..util import num, fmt, fit, parse_dt, rel_secs, emoji, tw


def build_profile(d, ctx):
    c = Canvas(FULL_W, 208, "GitHub profile")
    name = d.get("name") or d.get("login") or "GitHub"
    login = d.get("login") or ""

    # right panel: contributions
    c.add(rect(568, 16, 246, 176, PANEL, 6, LINE))
    c.add(line(560, 28, 560, 178))

    av = fetch_img(d.get("avatarUrl"), 192)
    c.defs.append('<clipPath id="av"><circle cx="74" cy="74" r="46"/></clipPath>')
    c.add(f'<circle cx="74" cy="74" r="49" stroke="#303030" stroke-width="1.5"/>')
    if av:
        c.add(
            f'<image href="{av}" xlink:href="{av}" x="28" y="28" width="92" height="92" clip-path="url(#av)" '
            f'preserveAspectRatio="xMidYMid slice"/>'
        )
    else:
        c.add(
            f'<circle cx="74" cy="74" r="46" fill="{TRACK}"/>'
            + tx(74, 84, name[:1].upper(), 30, MUTED, 700, "middle")
        )

    c.add(
        tx(144, 50, name, 24, TEXT, 700)
        + tx(
            144,
            70,
            "@" + login + (f"  ·  {d['pronouns']}" if d.get("pronouns") else ""),
            13,
            MUTED,
        )
    )
    if d.get("bio"):
        c.add(tx(144, 95, fit(d["bio"], 400, 13), 13, TEXT))

    st = d.get("status") or {}
    msg = st.get("message")
    if msg:
        label = (emoji(st.get("emoji")) + " " + msg).strip()
        w = tw(label, 11) + 20
        c.add(rect(144, 109, w, 22, PANEL, 11, LINE) + tx(154, 124, label, 11, TEXT))

    meta = []
    if d.get("company"):
        meta.append(("building", d["company"]))
    if d.get("location"):
        meta.append(("pin", d["location"]))
    if d.get("websiteUrl"):
        meta.append(("link", re.sub(r"^https?://", "", d["websiteUrl"]).rstrip("/")))
    if d.get("twitterUsername"):
        meta.append(("link", "@" + d["twitterUsername"]))
    created = parse_dt(d.get("createdAt"))
    if created:
        meta.append(("calendar", f"Joined {created:%b %Y}"))
    if d.get("updatedAt"):
        meta.append(
            (
                "clock",
                "Active "
                + rel_secs((ctx.now - parse_dt(d["updatedAt"])).total_seconds()),
            )
        )
    x, y = 144, 150
    for ico, label in meta:
        if ico == "at":
            ico = "link"
        if x + 18 + tw(label, 11) > 548:
            break
        c.add(icon(ico, x, y - 11, 13, MUTED) + tx(x + 18, y, label, 11, MUTED))
        x += 18 + tw(label, 11) + 18

    flags = [
        ("Developer Program", d.get("isDeveloperProgramMember"), GREEN),
        ("Hireable", d.get("isHireable"), BLUE),
        ("Campus Expert", d.get("isCampusExpert"), ORANGE),
        ("GitHub Star", d.get("isGitHubStar"), YELLOW),
        ("Bounty Hunter", d.get("isBountyHunter"), PINK),
    ]
    x = 24
    out = []
    for label, on, color in flags:
        svg, w = pill(x, 166, ("● " if on else "○ ") + label, color, bool(on), 10)
        out.append(svg)
        x += w + 6
    c.add("".join(out))

    # right panel: total + 90 day sparkline
    cal = d.get("calendar") or {}
    days = [num(x.get("count")) for x in cal.get("contributionDays", [])]
    total = d.get("contributions", cal.get("total", sum(days)))
    c.add(
        tx(
            584,
            40,
            "CONTRIBUTIONS · LAST YEAR",
            9.5,
            MUTED,
            600,
            extra='letter-spacing=".8"',
        )
        + tx(584, 76, fmt(total), 32, TEXT, 800)
        + tx(
            584,
            94,
            f"{fmt(cal.get('averagePerDay', d.get('averagePerDay', 0)))} / day · "
            f"{fmt(d.get('activeDays', 0))} active days",
            11,
            MUTED,
        ),
    )
    last = days[-97:]
    roll = [sum(last[max(0, i - 6) : i + 1]) for i in range(6, len(last))][-90:]
    c.add(
        spark(584, 110, 222, 52, roll)
        + tx(584, 178, "7-day rolling total · last 90 days", 9, DIM),
    )
    return c.render()
