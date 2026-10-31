from .svg import FULL, HALF, HALF_HEIGHT, PAD, Svg, duration, num


def totals(data, theme):
    svg = Svg(FULL, 132, theme, "Steam totals")
    achievements = data["achievements"]
    blocks = [
        (
            PAD,
            "Library",
            [
                (num(data["ownedGames"]), "games"),
                (f"{num(data['totalHours'])}h", "played"),
                (num(data["backlog"]), "unplayed"),
            ],
        ),
        (
            FULL / 2 + PAD,
            "Achievements",
            [
                (num(achievements["unlocked"]), "unlocked"),
                (f"{round(achievements['percent'])}%", "completed"),
                (num(achievements["perfect"]), "perfect games"),
            ],
        ),
    ]
    svg.vline(FULL / 2)
    col_w = (FULL / 2 - 2 * PAD) / 3
    for x, title, stats in blocks:
        svg.caption(title, x=x)
        for i, (value, label) in enumerate(stats):
            svg.stat(x + i * col_w, 80, value, label)
    return svg.render()


def most_played(data, theme):
    return _game(data.get("mostPlayed"), theme, "Most played", "total playtime")


def latest_played(data, theme):
    game = data.get("latestPlayed")
    recent = (
        duration(game["recentMinutes"] * 60)
        if game and game.get("recentMinutes")
        else ""
    )
    return _game(
        game,
        theme,
        "Latest played",
        "total playtime",
        extra=f"{recent} in the last two weeks" if recent else "",
    )


def _game(game, theme, caption, label, extra=""):
    svg = Svg(HALF, HALF_HEIGHT, theme, caption)
    if not game:
        svg.caption(caption)
        svg.text(PAD, 64, "No games yet", fill=theme.muted)
        return svg.render()

    x, _ = svg.media(caption, game["name"], game.get("cover"))
    svg.text(x, HALF_HEIGHT - 58, f"{num(game['minutes'] / 60)}h", size=22, weight=600)
    svg.text(x, HALF_HEIGHT - 40, extra or label, size=11, fill=theme.muted)
    return svg.render()
