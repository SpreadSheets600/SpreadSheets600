from dataclasses import dataclass


def mix(a, b, t):
    ca = [int(a[i : i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


@dataclass(frozen=True)
class Theme:
    name: str
    fg: str
    muted: str
    track: str
    accent: str
    line: str

    @property
    def ramp(self):
        return [self.track] + [
            mix(self.track, self.accent, t) for t in (0.3, 0.55, 0.8, 1.0)
        ]


DARK = Theme(
    "dark",
    fg="#e6edf3",
    muted="#8b949e",
    track="#232a33",
    accent="#3fb950",
    line="#3d444d",
)
LIGHT = Theme(
    "light",
    fg="#1f2328",
    muted="#656d76",
    track="#e8ebef",
    accent="#1f883d",
    line="#d1d9e0",
)

THEMES = (DARK, LIGHT)
