"""Steam cards: library and achievement totals, most played and recently played."""

from __future__ import annotations

from .svg import FULL, HALF, HALF_HEIGHT, PAD, Svg, clip, duration, num
from .theme import Theme


def totals(data: dict, theme: Theme) -> str:
    svg = Svg(FULL, 132, theme, "Steam totals")
    achievements = data["achievements"]
    blocks = [
        (PAD, "Library", [(num(data["ownedGames"]), "games"), (f'{num(data["totalHours"])}h', "played"), (num(data["backlog"]), "unplayed")]),
        (FULL / 2 + PAD, "Achievements", [(num(achievements["unlocked"]), "unlocked"), (f'{round(achievements["percent"])}%', "completed"), (num(achievements["perfect"]), "perfect games")]),
    ]
    svg.vline(FULL / 2)
    col_w = (FULL / 2 - 2 * PAD) / 3
    for x, title, stats in blocks:
        svg.caption(title, x=x)
        for i, (value, label) in enumerate(stats):
            svg.stat(x + i * col_w, 80, value, label)
    return svg.render()


def most_played(data: dict, theme: Theme) -> str:
    games = data["topGames"][:5]
    peak = max((game["minutes"] for game in games), default=0) or 1
    rows = [(game["name"], game["minutes"] / peak, f'{num(game["hours"])}h') for game in games]
    return _ranked("Most played", rows, theme)


def recent(data: dict, theme: Theme) -> str:
    games = data["recent"][:5]
    peak = max((game["minutes"] for game in games), default=0) or 1
    rows = [(game["name"], game["minutes"] / peak, duration(game["minutes"] * 60)) for game in games]
    return _ranked("Last two weeks", rows, theme)


def _ranked(caption: str, rows: list[tuple[str, float, str]], theme: Theme) -> str:
    svg = Svg(HALF, HALF_HEIGHT, theme, caption)
    svg.caption(caption)
    for i, (name, fraction, value) in enumerate(rows):
        svg.bar_row(PAD, 60 + i * 26, HALF - 2 * PAD, clip(name, 30), fraction, value)
    return svg.render()
