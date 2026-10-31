"""AniList cards: lifetime totals, plus the latest anime and manga progress."""

from __future__ import annotations

from .svg import FULL, HALF, PAD, Svg, num, wrap
from .theme import Theme

HEIGHT = 184
COVER_W, COVER_H = 91, 136


def totals(data: dict, theme: Theme) -> str:
    svg = Svg(FULL, 132, theme, "AniList totals")
    anime, manga = data["anime"], data["manga"]
    blocks = [
        (PAD, "Anime", [(num(anime["count"]), "titles"), (num(anime["episodesWatched"]), "episodes"), (f'{anime["daysWatched"]:.0f}d', "watched")]),
        (FULL / 2 + PAD, "Manga", [(num(manga["count"]), "titles"), (num(manga["chaptersRead"]), "chapters"), (num(manga["volumesRead"]), "volumes")]),
    ]
    svg.vline(FULL / 2)
    col_w = (FULL / 2 - 2 * PAD) / 3
    for x, title, stats in blocks:
        svg.caption(title, x=x)
        for i, (value, label) in enumerate(stats):
            svg.stat(x + i * col_w, 80, value, label)
    return svg.render()


def latest_anime(data: dict, theme: Theme) -> str:
    return _latest(data.get("latestAnime"), theme, "Latest anime", "Episode", "Anime")


def latest_manga(data: dict, theme: Theme) -> str:
    return _latest(data.get("latestManga"), theme, "Latest manga", "Chapter", "Manga")


def _latest(entry: dict | None, theme: Theme, caption: str, unit: str, label: str) -> str:
    svg = Svg(HALF, HEIGHT, theme, caption)
    text_x = PAD + COVER_W + 18
    width = HALF - PAD - text_x
    svg.caption(caption, x=text_x)

    if entry:
        if entry.get("cover"):
            svg.image(PAD, (HEIGHT - COVER_H) / 2, COVER_W, COVER_H, entry["cover"], rx=6)
        for i, line in enumerate(wrap(entry["title"], 26, 3)):
            svg.text(text_x, 64 + i * 20, line, size=14, weight=600)

        progress, total = entry["progress"], entry.get("total")
        status = "Completed" if entry["status"] == "COMPLETED" else f"{unit} {num(progress)}"
        if entry["status"] != "COMPLETED" and total:
            status += f" of {num(total)}"
        svg.text(text_x, HEIGHT - 52, status, fill=theme.muted)
        fraction = progress / total if total else 0
        if total:
            svg.rect(text_x, HEIGHT - 38, width, 4, theme.track, rx=2)
            svg.rect(text_x, HEIGHT - 38, max(width * fraction, 4), 4, theme.accent, rx=2)
    else:
        svg.text(text_x, 64, f"No {label.lower()} yet", fill=theme.muted)
    return svg.render()
