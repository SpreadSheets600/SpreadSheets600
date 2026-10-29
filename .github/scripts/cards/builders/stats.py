"""GitHub stats card (half width, 410 x 392)."""

from ..canvas import Canvas, HALF_W, rect, line, icon, tx
from ..theme import PANEL, LINE, TRACK, TEXT, MUTED, DIM, BLUE, PURPLE, GREEN, ORANGE, PINK, YELLOW
from ..util import num, fmt

PAIR_H = 392


def build_stats(d, ctx):
    c = Canvas(HALF_W, PAIR_H, "GitHub stats")
    login = d.get("login") or ""
    c.header("GitHub Stats", "chart", "@" + str(login))

    hero = [
        ("star", "Stars earned", d.get("stars"), YELLOW),
        ("commit", "Commits", d.get("commits"), GREEN),
        ("pr", "Pull requests", d.get("pullRequests"), PURPLE),
        ("issue", "Issues", d.get("issues"), ORANGE),
        ("chart", "Contributions", d.get("contributions"), BLUE),
        ("users", "Followers", d.get("followers"), PINK),
    ]
    tw_, gap = 118, 8
    out = []
    for i, (ico, label, val, col) in enumerate(hero):
        x, y = 20 + (i % 3) * (tw_ + gap), 48 + (i // 3) * 58
        out.append(
            rect(x, y, tw_, 50, PANEL, 9, TRACK)
            + icon(ico, x + 10, y + 9, 14, col)
            + tx(x + 30, y + 20, label, 10, MUTED)
            + tx(x + 10, y + 42, fmt(val), 19, TEXT, 800)
        )
    c.add("".join(out))

    left = [
        ("repo", "Repositories", d.get("repos")),
        ("fork", "Forks", d.get("forks")),
        ("users", "Following", d.get("following")),
        ("building", "Organizations", d.get("organizations")),
        ("code", "Contributed to", d.get("contributedTo")),
        ("file", "Gists", d.get("gists")),
        ("bookmark", "Starred", d.get("starred")),
        ("eye", "Watching", d.get("watching")),
        ("package", "Packages", d.get("packages")),
        ("project", "Projects", d.get("projects")),
    ]
    right = [
        ("heart", "Sponsors", d.get("sponsors")),
        ("heart", "Sponsoring", d.get("sponsoring")),
        ("eye", "Reviews", d.get("reviews")),
        ("repo", "Repo contributions", d.get("repositoryContributions")),
        ("commit", "Repos w/ commits", d.get("repositoriesWithCommits")),
        ("issue", "Repos w/ issues", d.get("repositoriesWithIssues")),
        ("pr", "Repos w/ PRs", d.get("repositoriesWithPullRequests")),
        ("eye", "Repos w/ reviews", d.get("repositoriesWithReviews")),
        ("lock", "Restricted contribs", d.get("restrictedContributions")),
    ]

    c.add(
        rect(16, 181, 185, 195, PANEL, 6, LINE)
        + rect(208, 181, 186, 195, PANEL, 6, LINE)
        + line(20, 170, HALF_W - 20, 170, TRACK)
    )
    for col, rows in enumerate((left, right)):
        x0 = 20 + col * 195
        # right edge of each column panel, minus padding
        end_x = (20 + 185) if col == 0 else (HALF_W - 20)
        for i, (ico, label, val) in enumerate(rows):
            yy = 192 + i * 19.5
            out = [
                icon(ico, x0, yy - 10.5, 12, DIM),
                tx(x0 + 18, yy, label, 10.5, MUTED),
                tx(end_x - 2, yy, fmt(val), 11, TEXT, 700, "end"),
            ]
            c.add("".join(out))
    rl = d.get("rateLimit") or {}
    if rl:
        c.add(
            tx(
                20,
                PAIR_H - 10,
                f"API budget {fmt(rl.get('remaining'))}/{fmt(rl.get('limit'))}",
                9,
                DIM,
            )
        )
    return c.render()
