"""Placeholder card used when a data source is unavailable (half width, 410 x 168)."""

from ..canvas import Canvas, HALF_W, rect, icon, tx
from ..theme import PANEL, TEXT, MUTED, ORANGE, PURPLE
from ..util import fit


def build_unavailable(name, err, ctx, ico="bolt", color=ORANGE):
    c = Canvas(HALF_W, 168, f"{name} unavailable")
    c.header(name, ico, None)
    c.add(
        f'<circle cx="{HALF_W / 2}" cy="84" r="22" fill="{PANEL}" stroke="{color}" stroke-opacity=".5"/>'
        + icon("bolt", HALF_W / 2 - 9, 75, 18, color, 1.7)
        + tx(HALF_W / 2, 128, f"{name} data unavailable", 12.5, TEXT, 700, "middle")
        + tx(
            HALF_W / 2,
            145,
            fit(f"source reported: {err or 'not ok'}", 340, 10),
            10,
            MUTED,
            400,
            "middle",
        )
    )
    return c.render()
