"""WakaTime card: totals, last seven days, top languages and editors."""

from __future__ import annotations

from datetime import date

from .svg import FULL, PAD, Svg, clip, duration, num
from .theme import Theme


def _split_total(label: str) -> tuple[str, str]:
    """'1,235 hrs 41 mins' -> ('1,235', 'hrs')."""
    number, _, unit = label.partition(" ")
    return number, unit.split(" ")[0] if unit else ""


def code_time(data: dict, theme: Theme) -> str:
    svg = Svg(FULL, 210, theme, "WakaTime coding activity")
    svg.caption("Code time")

    hours = int(data["totalSeconds"] // 3600)
    svg.stat(PAD, 80, f"{num(hours)}h", "all time")
    svg.stat(PAD, 140, duration(data["weekSeconds"]), "last 7 days")

    # last seven days
    x0, slot, bar_w, base, max_h = 168, 32, 18, 156, 80
    daily = data["daily"][-7:]
    peak = max((d["seconds"] for d in daily), default=0) or 1
    for i, day in enumerate(daily):
        x = x0 + i * slot
        h = max(max_h * day["seconds"] / peak, 3)
        fill = theme.accent if day["seconds"] == peak else theme.ramp[2] if day["seconds"] else theme.track
        svg.rect(x, base - h, bar_w, h, fill, rx=3)
        letter = date.fromisoformat(day["date"]).strftime("%a")
        svg.text(x + bar_w / 2, base + 18, letter, size=10, fill=theme.muted, anchor="middle")

    svg.vline(FULL / 2)
    _ranked(svg, 424, 160, "Languages", data["languages"][:5], data["weekSeconds"], base=62)
    _ranked(svg, 608, 168, "Editors", data["editors"][:3], data["weekSeconds"], base=62)
    return svg.render()


def _ranked(svg: Svg, x: float, width: float, title: str, rows: list[dict], total: float, base: float) -> None:
    svg.text(x, base - 6, title, size=11, fill=svg.theme.muted)
    for i, row in enumerate(rows):
        share = row["seconds"] / total if total else 0
        svg.bar_row(x, base + 18 + i * 26, width, clip(row["name"], 14), share, f"{round(share * 100)}%")
