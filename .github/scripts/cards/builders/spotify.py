"""Spotify card (half width, 410 x 168)."""

from ..canvas import Canvas, HALF_W, rect, icon, tx, hbar, pill as pill_at
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM, GREEN
from ..network import fetch_img
from ..util import num, pick, fit, flatten


def build_spotify(d, ctx):
    c = Canvas(HALF_W, 168, "Spotify")
    playing = bool(d.get("playing"))
    c.header("Spotify", "music", None)
    art = (
        fetch_img(
            pick(d, "albumArt", "albumImage", "image", "cover", "thumbnail", "art")
        )
        if playing
        else None
    )
    if art:
        c.add(c.clip_img(art, 22, 52, 86, 86, 12))
    else:
        c.add(
            rect(22, 52, 86, 86, PANEL, 12, TRACK)
            + icon("music", 49, 79, 32, GREEN if playing else DIM, 1.4)
        )
    label = "NOW PLAYING" if playing else "NOT PLAYING"
    svg, _ = pill_at(124, 50, "● " + label, GREEN if playing else DIM, playing, 9.5)
    c.add(svg)
    title = pick(d, "title", "track", "name", "song")
    artist = pick(d, "artist", "artists", "by")
    if isinstance(artist, list):
        artist = ", ".join(
            str(a.get("name", a)) if isinstance(a, dict) else str(a) for a in artist
        )
    album = pick(d, "album", "albumName")
    if playing and title:
        c.add(
            tx(124, 90, fit(title, 270, 15), 15, TEXT, 700)
            + tx(124, 108, fit(artist or "", 270, 11.5), 11.5, MUTED)
            + tx(124, 123, fit(album or "", 270, 10), 10, DIM)
        )
        prog, dur = (
            num(pick(d, "progressMs", "progress_ms", "progress")),
            num(pick(d, "durationMs", "duration_ms", "duration")),
        )
        if dur:
            c.add(hbar(124, 134, 266, prog / dur, GREEN, 4))
    else:
        c.add(
            tx(124, 92, "Nothing playing right now", 13.5, TEXT, 700)
            + tx(124, 110, "Last checked when the snapshot was taken", 10.5, MUTED)
        )
    bars = "".join(
        f'<rect class="{"eq" if playing else ""}" style="animation-delay:{i * 0.17:.2f}s" x="{HALF_W - 70 + i * 9}" y="{34 + (0 if playing else 8)}" '
        f'width="5" height="{[10, 16, 8, 14, 11][i] if playing else 5}" rx="2" fill="{GREEN if playing else DIM}"/>'
        for i in range(5)
    )
    c.add(
        f'<g transform="translate(0 0)">{bars}</g>'
        if playing
        else f'<g opacity=".7">{bars}</g>'
    )
    extra = [
        (k, v)
        for k, v in flatten(d)
        if k.lower()
        not in (
            "playing",
            "title",
            "track",
            "name",
            "artist",
            "album",
            "progress ms",
            "duration ms",
        )
    ]
    if playing and extra:
        c.add(
            tx(
                124,
                152,
                fit(" · ".join(f"{k}: {v}" for k, v in extra[:3]), 270, 9),
                9,
                DIM,
            )
        )
    return c.render()
