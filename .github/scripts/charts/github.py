"""GitHub cards: contribution heatmap, overview, activity, languages, weekdays."""

from __future__ import annotations

from datetime import date

from .svg import FULL, HALF, PAD, Svg, num
from .theme import Theme

HALF_HEIGHT = 184


def heatmap(data: dict, theme: Theme) -> str:
    days = data["calendar"]["contributionDays"]
    cell, gap = 12, 2.2
    top = 62
    svg = Svg(FULL, top + 7 * (cell + gap) + PAD - gap, theme, "GitHub contribution heatmap")

    svg.caption("Contributions · last year")
    svg.text(FULL - PAD, 34, num(data["calendar"]["total"]), size=11, weight=600, anchor="end")

    active = sorted(d["count"] for d in days if d["count"])
    quart = [active[int(len(active) * q)] for q in (0.25, 0.5, 0.75)] if active else [1, 2, 3]

    def level(count: int) -> int:
        if count == 0:
            return 0
        return 1 + sum(count > q for q in quart)

    first = date.fromisoformat(days[0]["date"])
    last_month = None
    for i, day in enumerate(days):
        col, row = divmod(i + days[0]["weekday"], 7)
        x, y = PAD + col * (cell + gap), top + row * (cell + gap)
        svg.rect(x, y, cell, cell, theme.ramp[level(day["count"])], rx=2.5)
        month = date.fromisoformat(day["date"]).month
        if row == 0 and month != last_month:
            if last_month is not None or first.day <= 7:
                svg.text(x, top - 8, date.fromisoformat(day["date"]).strftime("%b"), size=10, fill=theme.muted)
            last_month = month
    return svg.render()


def overview(data: dict, theme: Theme) -> str:
    svg = Svg(HALF, HALF_HEIGHT, theme, "GitHub overview")
    svg.caption("Overview")
    items = [
        (num(data["contributions"]), "contributions"),
        (num(data["commits"]), "commits"),
        (num(data["pullRequests"]), "pull requests"),
        (num(data["issues"]), "issues"),
        (num(data["stars"]), "stars"),
        (num(data["followers"]), "followers"),
    ]
    _grid(svg, items)
    return svg.render()


def activity(data: dict, theme: Theme) -> str:
    svg = Svg(HALF, HALF_HEIGHT, theme, "GitHub activity")
    svg.caption("Activity")
    total = max(data["weekdayContributions"] + data["weekendContributions"], 1)
    items = [
        (f'{data["currentStreak"]}d', "current streak"),
        (f'{data["longestStreak"]}d', "longest streak"),
        (num(data["activeDays"]), "active days"),
        (f'{data["averagePerDay"]:.1f}', "per day"),
        (num(data["bestDay"]["count"]), "best day"),
        (f'{round(100 * data["weekendContributions"] / total)}%', "on weekends"),
    ]
    _grid(svg, items)
    return svg.render()


def _grid(svg: Svg, items: list[tuple[str, str]]) -> None:
    col_w = (HALF - 2 * PAD) / 3
    for i, (value, label) in enumerate(items):
        col, row = i % 3, i // 3
        svg.stat(PAD + col * col_w, 80 + row * 60, value, label)


def languages(data: dict, theme: Theme) -> str:
    svg = Svg(HALF, HALF_HEIGHT, theme, "Top languages")
    svg.caption("Languages")
    langs = data["languages"][:5]
    total = sum(lang["repos"] for lang in data["languages"]) or 1
    width = HALF - 2 * PAD
    for i, lang in enumerate(langs):
        share = lang["repos"] / total
        svg.bar_row(PAD, 60 + i * 26, width, lang["name"], share, f"{round(share * 100)}%")
    return svg.render()


def weekdays(data: dict, theme: Theme) -> str:
    svg = Svg(HALF, HALF_HEIGHT, theme, "Contributions by weekday")
    svg.caption("Weekdays")
    counts = data["weekdayCounts"]  # Monday -> Sunday
    names = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    peak = max(counts) or 1
    slot = (HALF - 2 * PAD) / 7
    bar_w, base, max_h = 26, HALF_HEIGHT - 40, 82
    for i, count in enumerate(counts):
        x = PAD + i * slot + (slot - bar_w) / 2
        h = max(max_h * count / peak, 3)
        fill = theme.accent if count == peak else theme.ramp[2]
        svg.rect(x, base - h, bar_w, h, fill, rx=3)
        svg.text(x + bar_w / 2, base + 18, names[i], size=10, fill=theme.muted, anchor="middle")
    return svg.render()
