"""Tiny SVG builder plus the type scale every chart uses."""

from __future__ import annotations

from xml.sax.saxutils import escape

from .theme import Theme

# GitHub serves README SVGs through <img>, which blocks web fonts: system stack only.
FONT = 'ui-sans-serif, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif'

FULL = 800  # full-width card
HALF = 392  # half-width card (two per table row)
PAD = 24    # inner padding on every card


def num(value: float | int) -> str:
    return f"{int(round(value)):,}"


def clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def wrap(text: str, width: int, lines: int) -> list[str]:
    """Greedy word wrap to ``lines`` lines of at most ``width`` characters."""
    out, current = [], ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > width:
            out.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    out.append(current)
    if len(out) > lines:
        out = out[:lines]
        out[-1] = clip(out[-1] + "…", width)
    return out


def duration(seconds: float) -> str:
    minutes = int(seconds // 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


class Svg:
    def __init__(self, width: int, height: int, theme: Theme, label: str) -> None:
        self.width, self.height, self.theme, self.label = width, height, theme, label
        self._parts: list[str] = []
        self._defs: list[str] = []

    def rect(self, x, y, w, h, fill, rx: float = 0) -> None:
        self._parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"/>'
        )

    def text(self, x, y, value, *, size=12, weight=400, fill=None, anchor="start", spacing=None) -> None:
        extra = f' letter-spacing="{spacing}"' if spacing else ""
        self._parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill or self.theme.fg}" text-anchor="{anchor}"{extra}>{escape(str(value))}</text>'
        )

    def image(self, x, y, w, h, href: str, rx: float = 0) -> None:
        clip_id = f"clip{len(self._defs)}"
        self._defs.append(f'<clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>')
        self._parts.append(
            f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{href}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>'
        )

    # -- shared building blocks -------------------------------------------------

    def caption(self, value: str, x: float = PAD, y: float = 34) -> None:
        self.text(x, y, value.upper(), size=11, weight=600, fill=self.theme.muted, spacing="0.08em")

    def stat(self, x: float, y: float, value: str, label: str) -> None:
        self.text(x, y, value, size=22, weight=600)
        self.text(x, y + 18, label, size=11, fill=self.theme.muted)

    def bar_row(self, x: float, y: float, width: float, label: str, fraction: float, value: str) -> None:
        """Label + value on one line, thin bar underneath."""
        self.text(x, y, label)
        self.text(x + width, y, value, fill=self.theme.muted, anchor="end")
        self.rect(x, y + 8, width, 4, self.theme.track, rx=2)
        self.rect(x, y + 8, max(width * fraction, 4) if fraction > 0 else 0, 4, self.theme.accent, rx=2)

    def render(self) -> str:
        defs = f"<defs>{''.join(self._defs)}</defs>\n" if self._defs else ""
        body = defs + "\n".join(self._parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" role="img" aria-label="{escape(self.label)}" '
            f'font-family=\'{FONT}\'>\n{body}\n</svg>\n'
        )
