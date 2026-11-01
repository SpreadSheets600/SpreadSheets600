ICON_URL = "https://skillicons.dev/icons?i={name}&theme={theme}"

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
        f'<img src="{light}" alt="{name}" width="44" height="44"></picture>'
    )


def render():
    rows = "\n".join(
        f'  <tr>\n    <th width="120" align="left">{title}</th>\n'
        f'    <td width="100%">{" ".join(_icon(name) for name in names)}</td>\n  </tr>'
        for title, names in STACK.items()
    )
    return f'<table width="100%">\n  <tr>\n    <th colspan="2"><img src="assets/spacer.svg" width="100%" height="1" alt="">Stack</th>\n  </tr>\n{rows}\n</table>'
