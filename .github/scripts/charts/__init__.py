"""Render every profile chart as a light and dark SVG pair.

Each entry in ``CHARTS`` is ``(file stem, snapshot source, builder)``. A builder
takes that source's ``data`` and a ``Theme`` and returns an SVG string. To add a
chart: write a builder, then register it here.
"""

from __future__ import annotations

from pathlib import Path

from . import anilist, github, wakatime
from .theme import THEMES

CHARTS = [
    ("github-heatmap", "github", github.heatmap),
    ("github-overview", "github", github.overview),
    ("github-activity", "github", github.activity),
    ("github-languages", "github", github.languages),
    ("github-weekdays", "github", github.weekdays),
    ("code-time", "wakatime", wakatime.code_time),
    ("anilist-totals", "anilist", anilist.totals),
    ("anilist-anime", "anilist", anilist.latest_anime),
    ("anilist-manga", "anilist", anilist.latest_manga),
]


def render_all(snapshot: dict, out_dir: Path) -> int:
    """Write ``<stem>-<theme>.svg`` for every chart; return the file count.

    A source that failed (``ok`` is false) keeps its previous files untouched.
    """
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
