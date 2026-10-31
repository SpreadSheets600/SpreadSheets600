from . import anilist, github, steam, wakatime
from .theme import THEMES

CHARTS = [
    ("github-heatmap", "github", github.heatmap),
    ("github-streak", "github", github.streak),
    ("github-overview", "github", github.overview),
    ("github-activity", "github", github.activity),
    ("github-languages", "github", github.languages),
    ("github-weekdays", "github", github.weekdays),
    ("code-time", "wakatime", wakatime.code_time),
    ("anilist-totals", "anilist", anilist.totals),
    ("anilist-anime", "anilist", anilist.latest_anime),
    ("anilist-manga", "anilist", anilist.latest_manga),
    ("steam-totals", "steam", steam.totals),
    ("steam-most-played", "steam", steam.most_played),
    ("steam-latest", "steam", steam.latest_played),
]


def render_all(snapshot, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for stem, source, builder in CHARTS:
        block = snapshot.get(source) or {}
        if not block.get("ok"):
            print(f"{stem}: {source} unavailable, keeping previous file")
            continue
        for theme in THEMES:
            (out_dir / f"{stem}-{theme.name}.svg").write_text(
                builder(block["data"], theme), encoding="utf-8"
            )
            written += 1
    return written
