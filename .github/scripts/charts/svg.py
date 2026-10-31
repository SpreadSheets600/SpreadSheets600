import math
from xml.sax.saxutils import escape


FONT = 'ui-sans-serif, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif'

FULL = 800
HALF = 392
PAD = 24
HALF_HEIGHT = 184
COVER_W, COVER_H = 91, 136


def num(value):
    return f"{int(round(value)):,}"


def clip(text, limit):
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def wrap(text, width, lines):
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


def duration(seconds):
    minutes = int(seconds // 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


class Svg:
    def __init__(self, width, height, theme, label):
        self.width, self.height, self.theme, self.label = width, height, theme, label
        self._parts = []
        self._defs = []

    def rect(self, x, y, w, h, fill, rx=0):
        self._parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"/>'
        )

    def text(
        self,
        x,
        y,
        value,
        *,
        size=12,
        weight=400,
        fill=None,
        anchor="start",
        spacing=None,
    ):
        extra = f' letter-spacing="{spacing}"' if spacing else ""
        self._parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill or self.theme.fg}" text-anchor="{anchor}"{extra}>{escape(str(value))}</text>'
        )

    def vline(self, x, y1=0, y2=None):
        y2 = self.height if y2 is None else y2
        self.rect(x - 0.5, y1, 1, y2 - y1, self.theme.line)

    def ring(self, cx, cy, r, fraction, width=6):
        c = 2 * math.pi * r
        base = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke-width="{width}"'
        self._parts.append(f'{base} stroke="{self.theme.track}"/>')
        self._parts.append(
            f'{base} stroke="{self.theme.accent}" stroke-linecap="round" '
            f'stroke-dasharray="{max(fraction, 0.02) * c:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})"/>'
        )

    def image(self, x, y, w, h, href, rx=0):
        clip_id = f"clip{len(self._defs)}"
        self._defs.append(
            f'<clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
        )
        self._parts.append(
            f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{href}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>'
        )

    def caption(self, value, x=PAD, y=34):
        self.text(
            x,
            y,
            value.upper(),
            size=11,
            weight=600,
            fill=self.theme.muted,
            spacing="0.08em",
        )

    def stat(self, x, y, value, label):
        self.text(x, y, value, size=22, weight=600)
        self.text(x, y + 18, label, size=11, fill=self.theme.muted)

    def bar_row(self, x, y, width, label, fraction, value):
        self.text(x, y, label)
        self.text(x + width, y, value, fill=self.theme.muted, anchor="end")
        self.rect(x, y + 8, width, 4, self.theme.track, rx=2)
        self.rect(
            x,
            y + 8,
            max(width * fraction, 4) if fraction > 0 else 0,
            4,
            self.theme.accent,
            rx=2,
        )

    def media(self, caption, title, cover):
        x = PAD + COVER_W + 18
        self.caption(caption, x=x)
        if cover:
            self.image(PAD, (self.height - COVER_H) / 2, COVER_W, COVER_H, cover, rx=6)
        for i, line in enumerate(wrap(title, 26, 3)):
            self.text(x, 64 + i * 20, line, size=14, weight=600)
        return x, self.width - PAD - x

    def render(self):
        defs = f"<defs>{''.join(self._defs)}</defs>\n" if self._defs else ""
        body = defs + "\n".join(self._parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" role="img" aria-label="{escape(self.label)}" '
            f"font-family='{FONT}'>\n{body}\n</svg>\n"
        )
