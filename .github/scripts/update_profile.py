import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import stack


def fetch(path: str) -> str:
    base = os.environ.get("PROFILE_API_BASE", "").rstrip("/")
    if not base:
        raise SystemExit("PROFILE_API_BASE is not set")

    request = urllib.request.Request(
        base + path,
        headers={"user-agent": "spreadsheets600-readme-action"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def replace_block(readme: str, name: str, body: str) -> str:
    start = f"<!--START_SECTION:{name}-->"
    end = f"<!--END_SECTION:{name}-->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(readme):
        print(f"marker {name} not found, skipping", file=sys.stderr)
        return readme
    replacement = f"{start}\n{body.strip()}\n{end}"
    return pattern.sub(lambda _match: replacement, readme)


def main() -> None:
    with open("README.md", encoding="utf-8") as handle:
        readme = handle.read()

    readme = replace_block(readme, "stack", stack.render())

    try:
        header = json.loads(fetch("/header?format=json"))
        readme = replace_block(
            readme,
            "header",
            f'<img src="{header["url"]}" alt="Soham Maity" width="100%">',
        )
    except Exception as error:
        print(f"header refresh failed: {error}", file=sys.stderr)

    try:
        snapshot = json.loads(fetch("/snapshot"))

        try:
            from anilist_source import fetch_anilist

            anilist_data = fetch_anilist(
                os.environ.get("ANILIST_USERNAME", "SpreadSheeets")
            )
            snapshot["anilist"] = {"ok": True, "data": anilist_data}
            cache_path = Path("assets/anilist.json")
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(
                json.dumps(anilist_data, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            print("anilist: refreshed cache")
        except Exception as error:
            print(f"anilist refresh failed: {error}", file=sys.stderr)

        from charts import render_all

        written = render_all(snapshot, Path("assets/charts"))
        print(f"charts: wrote {written} SVG files")
    except Exception as error:
        # Charts are static assets. If one refresh fails, keep the previous
        # versions in place rather than blocking the README refresh.
        print(f"chart refresh failed: {error}", file=sys.stderr)

    with open("README.md", "w", encoding="utf-8") as handle:
        handle.write(readme)


if __name__ == "__main__":
    main()
