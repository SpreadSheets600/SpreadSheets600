"""16x16 stroke-based icon pack used by every card."""

from .theme import MUTED

# ----------------------------------------------------------------------------- icons (16x16, stroke based)
ICONS = {
    "star": '<polygon points="8,1.5 10,6 14.5,6.3 11,9.3 12.2,14 8,11.4 3.8,14 5,9.3 1.5,6.3 6,6"/>',
    "commit": '<circle cx="8" cy="8" r="3"/><path d="M1 8H5M11 8H15"/>',
    "pr": '<circle cx="4" cy="3.5" r="1.7"/><circle cx="4" cy="12.5" r="1.7"/><circle cx="12" cy="12.5" r="1.7"/><path d="M4 5.2V10.8M12 10.8V6.5A2 2 0 0 0 10 4.5H8"/>',
    "issue": '<circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="1.2" fill="currentColor"/>',
    "eye": '<path d="M1 8C3 4.5 5.5 3.2 8 3.2S13 4.5 15 8C13 11.5 10.5 12.8 8 12.8S3 11.5 1 8Z"/><circle cx="8" cy="8" r="2"/>',
    "fork": '<circle cx="4" cy="3" r="1.6"/><circle cx="12" cy="3" r="1.6"/><circle cx="8" cy="13" r="1.6"/><path d="M4 4.6V6.5Q4 8 5.5 8H10.5Q12 8 12 6.5V4.6M8 8V11.4"/>',
    "repo": '<rect x="2.5" y="1.5" width="11" height="13" rx="1.6"/><path d="M5.5 5H10.5M5.5 8H10.5"/>',
    "users": '<circle cx="6" cy="5.5" r="2.5"/><path d="M1.5 14C1.5 10.8 3.5 9.5 6 9.5S10.5 10.8 10.5 14"/><circle cx="11.5" cy="6" r="1.8"/><path d="M11.5 9.6C13.5 9.6 14.8 10.6 14.8 13"/>',
    "flame": '<path d="M8 1.5C8 4.5 12 6 12 10A4 4 0 0 1 4 10C4 8.5 5 7.5 5.5 6.5C6.5 7.5 7 7.5 7 7C7 5 8 3.5 8 1.5Z"/>',
    "trophy": '<path d="M5 2H11V6A3 3 0 0 1 5 6ZM5 3.5H2.5V5A2 2 0 0 0 5 7M11 3.5H13.5V5A2 2 0 0 1 11 7M8 9V12M5.5 14H10.5M6.5 12H9.5"/>',
    "calendar": '<rect x="2" y="3" width="12" height="11" rx="1.6"/><path d="M2 6.5H14M5 1.5V4M11 1.5V4"/>',
    "clock": '<circle cx="8" cy="8" r="6"/><path d="M8 4.5V8L10.5 9.5"/>',
    "code": '<path d="M5.5 4L1.5 8L5.5 12M10.5 4L14.5 8L10.5 12"/>',
    "gamepad": '<rect x="1.5" y="4.5" width="13" height="7.5" rx="3.5"/><path d="M5 6.8V9.8M3.5 8.3H6.5"/><circle cx="10.5" cy="7.6" r=".8" fill="currentColor"/><circle cx="12" cy="9.4" r=".8" fill="currentColor"/>',
    "music": '<path d="M6 12V3.2L13 1.8V10.6"/><circle cx="4.5" cy="12.2" r="1.7"/><circle cx="11.5" cy="10.8" r="1.7"/>',
    "disk": '<ellipse cx="8" cy="4" rx="5.5" ry="2.2"/><path d="M2.5 4V12A5.5 2.2 0 0 0 13.5 12V4M2.5 8A5.5 2.2 0 0 0 13.5 8"/>',
    "building": '<rect x="3" y="1.8" width="10" height="12.4" rx="1.2"/><path d="M6 5H7M9 5H10M6 8H7M9 8H10M7 14V11H9V14"/>',
    "package": '<path d="M8 1.5L14 4.5V11.5L8 14.5L2 11.5V4.5ZM2 4.5L8 7.5L14 4.5M8 7.5V14.5"/>',
    "project": '<rect x="2" y="2" width="12" height="12" rx="1.6"/><path d="M6.5 2V14M6.5 7H14"/>',
    "heart": '<path d="M8 13.5C2 9.5 1.5 6 3 4.2C4.5 2.5 7 3 8 5C9 3 11.5 2.5 13 4.2C14.5 6 14 9.5 8 13.5Z"/>',
    "file": '<path d="M3.5 1.5H9.5L12.5 4.5V14.5H3.5ZM9.5 1.5V4.5H12.5"/>',
    "bookmark": '<path d="M4 1.5H12V14.5L8 11.5L4 14.5Z"/>',
    "link": '<path d="M6.5 9.5L9.5 6.5M7 4.5L8 3.5A2.6 2.6 0 0 1 11.7 7.2L10.7 8.2M9 11.5L8 12.5A2.6 2.6 0 0 1 4.3 8.8L5.3 7.8"/>',
    "tag": '<path d="M1.5 8.5V2.5H7.5L14.5 9.5L9.5 14.5Z"/><circle cx="5" cy="5.5" r=".9" fill="currentColor"/>',
    "medal": '<circle cx="8" cy="6" r="4"/><path d="M5.5 9.5L4.5 14.5L8 12.5L11.5 14.5L10.5 9.5"/>',
    "chart": '<path d="M1.5 14H14.5M3.5 11V8M7 11V3.5M10.5 11V6.5M14 11V9"/>',
    "pin": '<path d="M8 14.5C8 14.5 3 9.5 3 6.5A5 5 0 0 1 13 6.5C13 9.5 8 14.5 8 14.5Z"/><circle cx="8" cy="6.5" r="1.8"/>',
    "bolt": '<path d="M9 1.5L3.5 9H8L7 14.5L12.5 7H8Z"/>',
    "layers": '<path d="M8 2L14.5 5.5L8 9L1.5 5.5ZM1.5 8.5L8 12L14.5 8.5"/>',
    "monitor": '<rect x="1.5" y="2.5" width="13" height="8.5" rx="1.4"/><path d="M5.5 14H10.5M8 11V14"/>',
    "lock": '<rect x="3" y="7" width="10" height="7" rx="1.5"/><path d="M5.5 7V5A2.5 2.5 0 0 1 10.5 5V7"/>',
}


def icon(name, x, y, size=16, color=MUTED, sw=1.5):
    s = size / 16.0
    return (
        f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" color="{color}" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" fill="none">'
        f"{ICONS[name]}</g>"
    )
