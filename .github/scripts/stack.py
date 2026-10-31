ICON_URL = "https://skillicons.dev/icons?i={name}&theme={theme}"
PER_ROW = 4
SPACER = '<img align="right" src="assets/spacer.svg" width="200" height="1" alt="">'

STACK = {
    "Languages": ["python", "html", "css", "javascript", "c", "cpp", "java", "bash"],
    "Frameworks": [
        "django",
        "flask",
        "nodejs",
        "vue",
        "tailwind",
        "tensorflow",
        "opencv",
    ],
    "Databases": ["sqlite", "mongo", "mysql", "postgres"],
    "Tools": ["linux", "vscode", "sublime", "replit", "notion", "github", "discord"],
}


def _icon(name):
    dark, light = (ICON_URL.format(name=name, theme=t) for t in ("dark", "light"))
    return (
        f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}">'
        f'<img src="{light}" alt="{name}" width="22%"></picture>'
    )


def _cell(names):
    rows = [names[i : i + PER_ROW] for i in range(0, len(names), PER_ROW)]
    return "<br>\n      ".join(" ".join(_icon(name) for name in row) for row in rows)


def render():
    heads = "\n".join(f"    <th>{title}{SPACER}</th>" for title in STACK)
    cells = "\n".join(
        f'    <td align="center" valign="top">\n      {_cell(names)}\n    </td>'
        for names in STACK.values()
    )
    return f"<table>\n  <tr>\n{heads}\n  </tr>\n  <tr>\n{cells}\n  </tr>\n</table>"
