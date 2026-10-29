"""Shared helpers: escaping, numbers, dates, text measuring, emoji, flattening."""

import math
import re
from datetime import UTC, datetime
from html import escape


def esc(s):
    return escape(str(s), quote=True)


def num(v, default=0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def fmt(v):
    v = num(v)
    return (
        f"{int(v):,}" if float(v).is_integer() else f"{v:,.2f}".rstrip("0").rstrip(".")
    )


def compact(v):
    v = num(v)
    if v >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    if v >= 10_000:
        return f"{v / 1000:.1f}k"
    return fmt(v)


def hm(seconds):
    seconds = int(round(num(seconds)))
    h, rem = divmod(seconds, 3600)
    m = rem // 60
    return f"{h}h {m}m" if h else f"{m}m"


def size_from_kb(kb):
    """GitHub GraphQL reports diskUsage in kilobytes."""
    b = num(kb) * 1024
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if b < 1024 or unit == "TB":
            return f"{b:.1f} {unit}" if unit != "B" else f"{int(b)} B"
        b /= 1024.0


def tw(s, size):
    """Approximate text width in px (rough, used for chip wrapping)."""
    return len(str(s)) * size * 0.56


def fit(s, px, size):
    s = str(s)
    n = max(int(px / (size * 0.55)), 3)
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def parse_dt(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def fdate(s):
    d = parse_dt(s)
    return f"{d.day} {d:%b %Y}" if d else "-"


def rel_secs(delta):
    s = max(int(delta), 0)
    for unit, sec in (
        ("y", 31536000),
        ("mo", 2592000),
        ("d", 86400),
        ("h", 3600),
        ("m", 60),
    ):
        if s >= sec:
            return f"{s // sec}{unit} ago"
    return "just now"


def pct(a, b):
    return 0 if not b else a / b * 100.0


def tx(x, y, s, size=12, fill="#f2f2f2", weight=400, anchor="start", extra=""):
    label = str(s)
    mono = anchor == "end" or bool(re.fullmatch(r"[\d\s.,%:/·+\-★✓]+", label))
    klass = ' class="mono"' if mono else ""
    weight = min(weight, 600)
    return (
        f'<text{klass} x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}" {extra}>{esc(label)}</text>'
    )


def emoji(code):
    if not code:
        return ""
    EMOJI = {
        ":pencil2:": "✏️",
        ":rocket:": "🚀",
        ":zap:": "⚡",
        ":books:": "📚",
        ":coffee:": "☕",
        ":thought_balloon:": "💭",
        ":palm_tree:": "🌴",
        ":house:": "🏠",
        ":dart:": "🎯",
        ":fire:": "🔥",
        ":computer:": "💻",
        ":sleeping:": "😴",
        ":seedling:": "🌱",
        ":star:": "⭐",
        ":brain:": "🧠",
        ":hammer_and_wrench:": "🛠️",
        ":wave:": "👋",
        ":eyes:": "👀",
        ":sparkles:": "✨",
        ":bug:": "🐛",
    }
    return EMOJI.get(code, "" if re.fullmatch(r":[\w+-]+:", code) else code)


def nice(key):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(key)).replace("_", " ")
    return s[:1].upper() + s[1:].lower() if s else s


def flatten(o, prefix="", out=None, depth=0):
    out = [] if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, dict) and depth < 2:
                flatten(v, prefix + nice(k) + " · ", out, depth + 1)
            elif (
                isinstance(v, (str, int, float, bool))
                and v != ""
                and not (isinstance(v, str) and v.startswith("http"))
            ):
                out.append((prefix + nice(k), v))
    return out


def pick(d, *keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", []):
            return v
    return None
