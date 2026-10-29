"""Shared theme for the profile cards.

Palette is kept as-is. Layout is constrained to exactly two canvas widths:
FULL_W (830) and HALF_W (410). Every card picks one of them and heights follow
an 8px spacing grid so the whole set looks consistent side by side.
"""

# ----------------------------------------------------------------------------- palette
GROUND, PANEL, LINE, LINE_2 = "#050505", "#0e0e0e", "#222222", "#303030"
TEXT, MUTED, DIM, LIVE = "#f2f2f2", "#a6a9ad", "#8a8d91", "#3fd6c6"
TRACK = "#1a1a1a"
BLUE, PURPLE, GREEN = "#a6a9ad", "#8a8d91", LIVE
ORANGE, PINK, YELLOW = "#96999d", "#c7c9cc", "#f2f2f2"
CYAN, RED = LIVE, "#8a8d91"
PALETTE = [LIVE, "#a6a9ad", "#d0d2d4", "#777b80", "#eceeef", "#565b60", "#92969b", "#3a3d40"]
HEAT = ["#171717", "#202725", "#294a45", "#317a6e", LIVE]

# ----------------------------------------------------------------------------- sizes
# Only two widths exist. Full width cards span the README; half width cards
# are meant to be paired (two per row, ~49% each).
FULL_W = 830
HALF_W = 410

PAD = 20          # outer padding, identical on every card
GAP = 14          # gap between sections
RADIUS = 8        # panel corner radius
HEADER_H = 52     # header band height

# ----------------------------------------------------------------------------- stylesheet
STYLE = """
text{font-family:'Geist','Helvetica Neue',Arial,sans-serif;font-kerning:normal}
text.mono{font-family:'Geist Mono','SFMono-Regular',Menlo,monospace;font-variant-numeric:tabular-nums}
.bar{animation:fadeIn 0.7s ease both}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""
