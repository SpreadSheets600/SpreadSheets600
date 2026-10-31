"""Colour tokens shared by every chart. One accent, neutral everything else."""

from __future__ import annotations

from dataclasses import dataclass


def mix(a: str, b: str, t: float) -> str:
    """Blend hex colour ``a`` towards ``b`` by ``t`` (0..1)."""
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

    @property
    def ramp(self) -> list[str]:
        """Five-step intensity ramp, empty -> full accent."""
        return [self.track] + [mix(self.track, self.accent, t) for t in (0.3, 0.55, 0.8, 1.0)]


DARK = Theme("dark", fg="#e6edf3", muted="#8b949e", track="#232a33", accent="#3fb950")
LIGHT = Theme("light", fg="#1f2328", muted="#656d76", track="#e8ebef", accent="#1f883d")

THEMES = (DARK, LIGHT)
