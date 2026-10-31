from .svg import FULL, HALF, HALF_HEIGHT, PAD, Svg, num


def totals(data, theme):
    svg = Svg(FULL, 132, theme, "AniList totals")
    anime, manga = data["anime"], data["manga"]
    blocks = [
        (
            PAD,
            "Anime",
            [
                (num(anime["count"]), "titles"),
                (num(anime["episodesWatched"]), "episodes"),
                (f"{anime['daysWatched']:.0f}d", "watched"),
            ],
        ),
        (
            FULL / 2 + PAD,
            "Manga",
            [
                (num(manga["count"]), "titles"),
                (num(manga["chaptersRead"]), "chapters"),
                (num(manga["volumesRead"]), "volumes"),
            ],
        ),
    ]
    svg.vline(FULL / 2)
    col_w = (FULL / 2 - 2 * PAD) / 3
    for x, title, stats in blocks:
        svg.caption(title, x=x)
        for i, (value, label) in enumerate(stats):
            svg.stat(x + i * col_w, 80, value, label)
    return svg.render()


def latest_anime(data, theme):
    return _latest(data.get("latestAnime"), theme, "Latest anime", "Episode", "Anime")


def latest_manga(data, theme):
    return _latest(data.get("latestManga"), theme, "Latest manga", "Chapter", "Manga")


def _latest(entry, theme, caption, unit, label):
    svg = Svg(HALF, HALF_HEIGHT, theme, caption)
    if not entry:
        svg.caption(caption)
        svg.text(PAD, 64, f"No {label.lower()} yet", fill=theme.muted)
        return svg.render()

    x, width = svg.media(caption, entry["title"], entry.get("cover"))
    progress, total = entry["progress"], entry.get("total")
    done = entry["status"] == "COMPLETED"
    status = (
        "Completed"
        if done
        else f"{unit} {num(progress)}" + (f" of {num(total)}" if total else "")
    )
    svg.text(x, HALF_HEIGHT - 52, status, fill=theme.muted)
    if total:
        svg.rect(x, HALF_HEIGHT - 38, width, 4, theme.track, rx=2)
        svg.rect(
            x, HALF_HEIGHT - 38, max(width * progress / total, 4), 4, theme.accent, rx=2
        )
    return svg.render()
