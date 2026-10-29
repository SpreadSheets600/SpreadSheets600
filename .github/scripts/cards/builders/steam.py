"""Steam card (full width, 830 wide, height fits content)."""

import math

from ..canvas import Canvas, FULL_W, rect, line, icon, tx, hbar, ring
from ..theme import PANEL, LINE, TEXT, MUTED, DIM, LIVE, PURPLE, BLUE, ORANGE, YELLOW, CYAN, PINK, GREEN, PALETTE, TRACK
from ..network import fetch_img
from ..util import num, fmt, hm, rel_secs, parse_dt, fit


def build_steam(d, ctx):
    c = Canvas(FULL_W, 620, "Steam")
    profile_url = d.get("profileUrl", "").replace("https://steamcommunity.com/", "").rstrip("/")
    c.header("Steam", "gamepad", profile_url or None)

    av = fetch_img(d.get("avatar"))
    c.add(c.clip_img(av, 24, 50, 60, 60, 14, d.get("name", "S")))

    status = d.get("status", "offline")
    game = d.get("game")
    scol = LIVE if game or status == "online" else DIM
    c.add(
        tx(100, 76, d.get("name", ""), 21, TEXT, 800)
        + f'<circle cx="106" cy="94" r="4.5" fill="{scol}"/>'
        + tx(
            116,
            98,
            (("Playing " + str(game)) if game else str(status).capitalize())
            + (f"  ·  {d['country']}" if d.get("country") else ""),
            11.5,
            MUTED,
        ),
    )

    lvl, xp, need = int(num(d.get("level"))), num(d.get("xp")), num(d.get("xpNeeded"))
    per_level = 100 * math.ceil((lvl + 1) / 10.0)
    prog = 1 - need / per_level if per_level else 0
    c.add(
        f'<circle cx="580" cy="80" r="26" fill="{PANEL}" stroke="url(#ac)" stroke-width="3"/>'
        + tx(580, 87, str(lvl), 22, TEXT, 800, "middle")
        + tx(580, 124, "LEVEL", 8.5, MUTED, 600, "middle")
        + tx(622, 70, f"{fmt(xp)} XP", 13, TEXT, 700)
        + tx(622 + 80, 70, f"· {fmt(need)} to next level", 10.5, MUTED)
        + hbar(622, 80, 184, prog, "url(#ac)", 8)
        + tx(
            622, 104, f"{max(0, min(prog, 1)) * 100:.0f}% through level {lvl}", 9.5, DIM
        ),
    )

    ach = d.get("achievements") or {}
    tiles = [
        ("clock", "Hours played", fmt(d.get("totalHours")), BLUE),
        ("gamepad", "Owned games", fmt(d.get("ownedGames")), PURPLE),
        ("chart", "Avg / game", f"{fmt(d.get('averageHours'))}h", CYAN),
        ("layers", "Backlog", fmt(d.get("backlog")), ORANGE),
        ("medal", "Badges", fmt(d.get("badges")), PINK),
        (
            "trophy",
            "Achievements",
            f"{fmt(ach.get('unlocked'))}/{fmt(ach.get('total'))}",
            YELLOW,
        ),
    ]
    tw_ = (FULL_W - 40 - 5 * 8) / 6
    out = []
    for i, (ico, lab, val, col) in enumerate(tiles):
        x = 20 + i * (tw_ + 8)
        out.append(
            rect(x, 130, tw_, 52, PANEL, 9, TRACK)
            + icon(ico, x + 10, 139, 13, col)
            + tx(x + 28, 149, lab, 9.5, MUTED)
            + tx(x + 10, 172, val, 17, TEXT, 800)
        )
    c.add("".join(out))

    c.add(rect(16, 198, 398, 250, PANEL, 6, LINE))
    c.add(rect(420, 198, 394, 250, PANEL, 6, LINE))

    def game_rows(x, y, title, sub, rows, line1, line2, frac_fn, color):
        out = [
            tx(x, y, title, 11, TEXT, 700),
            tx(x + 380, y, sub, 9.5, DIM, 400, "end"),
        ]
        for i, g in enumerate(rows[:5]):
            yy = y + 14 + i * 46
            ic = fetch_img(g.get("icon"))
            out.append(
                c.clip_img(ic, x, yy, 38, 38, 8, g.get("name", "?"))
                + tx(x + 48, yy + 14, fit(g.get("name", ""), 250, 12), 12, TEXT, 600)
                + tx(x + 48, yy + 28, line1(g), 10, MUTED)
                + tx(x + 380, yy + 14, line2(g), 10.5, TEXT, 700, "end")
                + hbar(x + 48, yy + 33, 332, frac_fn(g), color, 4)
            )
        return "".join(out)

    recent = d.get("recent") or []
    rmax = sum(num(g.get("minutes")) for g in recent) or 1
    c.add(
        game_rows(
            20,
            208,
            "Recently played",
            "last 2 weeks",
            recent,
            lambda g: f"{hm(num(g.get('totalMinutes')) * 60)} all-time",
            lambda g: hm(num(g.get("minutes")) * 60),
            lambda g: num(g.get("minutes")) / rmax,
            BLUE,
        ),
    )
    top = d.get("topGames") or []
    tmax = max([num(g.get("minutes")) for g in top] + [1])
    c.add(line(415, 198, 415, 448, LINE))
    c.add(
        game_rows(
            430,
            208,
            "Most played",
            "all-time",
            top,
            lambda g: (
                f"last played {rel_secs(ctx.now.timestamp() - num(g.get('lastPlayed')))}"
                if g.get("lastPlayed")
                else ""
            ),
            lambda g: f"{fmt(g.get('hours'))} h",
            lambda g: num(g.get("minutes")) / tmax,
            PURPLE,
        ),
    )

    # achievements
    ay = 472
    c.add(rect(16, ay - 8, 398, 150, PANEL, 6, LINE))
    c.add(rect(420, ay - 8, 394, 150, PANEL, 6, LINE))
    c.add(line(20, ay - 10, FULL_W - 20, ay - 10, TRACK))
    c.add(
        tx(20, ay + 8, "Achievements", 11, TEXT, 700)
        + tx(112, ay + 8, f"checked across {fmt(ach.get('checked'))} games", 9.5, DIM)
    )
    c.add(
        ring(64, ay + 70, 36, 8, num(ach.get("percent")) / 100.0, "url(#ac)")
        + tx(64, ay + 76, f"{num(ach.get('percent')):.1f}%", 15, TEXT, 800, "middle")
        + tx(
            64,
            ay + 122,
            f"{fmt(ach.get('unlocked'))} of {fmt(ach.get('total'))} unlocked",
            9,
            MUTED,
            400,
            "middle",
        ),
    )
    lines = []
    latest, rare = ach.get("latest") or {}, ach.get("rarest") or {}
    yy = ay + 36
    if latest:
        when = (
            rel_secs(ctx.now.timestamp() - num(latest.get("unlockedAt")))
            if latest.get("unlockedAt")
            else ""
        )
        lines += [
            icon("medal", 128, yy - 10, 13, GREEN),
            tx(148, yy, "Latest", 9.5, MUTED),
            tx(190, yy, fit(latest.get("name", ""), 150, 11.5), 11.5, TEXT, 700),
            tx(190, yy + 13, f"{latest.get('game', '')} · {when}", 9.5, DIM),
        ]
        yy += 36
    if rare:
        lines += [
            icon("star", 128, yy - 10, 13, YELLOW),
            tx(148, yy, "Rarest", 9.5, MUTED),
            tx(190, yy, fit(rare.get("name", ""), 150, 11.5), 11.5, TEXT, 700),
            tx(
                190,
                yy + 13,
                f"{rare.get('game', '')} · {num(rare.get('percent')):g}% of players",
                9.5,
                DIM,
            ),
        ]
        yy += 36
    pg = ach.get("perfectGames") or []
    if pg:
        lines += [
            tx(
                128,
                yy + 4,
                f"{fmt(ach.get('perfect'))} perfect: " + ", ".join(pg),
                9.5,
                GREEN,
            )
        ]
    c.add("".join(lines))

    games = ach.get("games") or []
    out = [tx(430, ay + 8, "Per-game progress", 10.5, MUTED, 600)]
    for i, g in enumerate(games[:5]):
        yy = ay + 30 + i * 22
        col = GREEN if g.get("perfect") else BLUE
        out.append(
            tx(430, yy, fit(g.get("name", ""), 130, 10.5), 10.5, TEXT)
            + hbar(570, yy - 8, 160, num(g.get("percent")) / 100, col, 6)
            + tx(
                FULL_W - 20,
                yy,
                f"{fmt(g.get('unlocked'))}/{fmt(g.get('total'))}"
                + (" ✓" if g.get("perfect") else ""),
                10,
                MUTED,
                400,
                "end",
            )
        )
    c.add("".join(out))
    c.h = ay + 150
    return c.render()
