"""Card builder registry.

Each entry: (card id, data source key, builder function, header icon).
"""

from .profile import build_profile
from .stats import build_stats
from .streak import build_streak
from .activity import build_activity
from .languages import build_languages
from .repos import build_repos
from .wakatime import build_wakatime
from .steam import build_steam
from .spotify import build_spotify
from .anilist import build_anilist
from .unavailable import build_unavailable

CARDS = [
    ("profile", "github", build_profile, "bolt"),
    ("stats", "github", build_stats, "chart"),
    ("streak", "github", build_streak, "flame"),
    ("activity", "github", build_activity, "calendar"),
    ("languages", "github", build_languages, "code"),
    ("repos", "github", build_repos, "repo"),
    ("wakatime", "wakatime", build_wakatime, "clock"),
    ("steam", "steam", build_steam, "gamepad"),
    ("spotify", "spotify", build_spotify, "music"),
    ("anilist", "anilist", build_anilist, "bookmark"),
]

__all__ = ["CARDS", "build_unavailable"]
