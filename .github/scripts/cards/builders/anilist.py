"""AniList card (half width, 410 wide, height fits content)."""

from ..canvas import Canvas, HALF_W, rect, line, tx
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM
from ..util import num, fmt, fit, flatten


def build_anilist(d, ctx):
    c = Canvas(HALF_W, 168, "AniList")
    c.header(
        "AniList", "bookmark", str(d.get("name") or d.get("username") or "") or None
    )
    pairs = flatten(d)
    pairs = [(k, v) for k, v in pairs if k.lower() not in ("name", "username")]
    out = []
    for i, (k, v) in enumerate(pairs[:8]):
        col, row = divmod(i, 4)
        x, y = 20 + col * 195, 66 + row * 24
        val = (
            fmt(v)
            if isinstance(v, (int, float)) and not isinstance(v, bool)
            else str(v)
        )
        out.append(
            rect(x - 6, y - 15, 181, 21, PANEL, 6, LINE)
            + tx(x, y, fit(k, 120, 10), 10, MUTED)
            + tx(x + 175, y, fit(val, 70, 12), 12, TEXT, 700, "end")
            + line(x, y + 7, x + 175, y + 7, TRACK)
        )
    c.add("".join(out) or tx(20, 80, "No fields in the snapshot", 12, MUTED))
    return c.render()
