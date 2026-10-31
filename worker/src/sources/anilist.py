from workers import fetch

RAW_BASE = "https://raw.githubusercontent.com"


async def fetch_stats(config):
    """Read the AniList cache committed by the profile GitHub Action.

    AniList blocks Cloudflare Workers egress with a 403, so the action fetches
    the public GraphQL API from a GitHub runner and commits the normalised data
    to ``assets/anilist.json``. The worker only reads that public file.
    """

    if not config.anilist_username:
        return None

    url = (
        f"{RAW_BASE}/{config.profile_repo}/{config.profile_branch}"
        "/assets/anilist.json"
    )
    response = await fetch(
        url,
        headers={
            "accept": "application/json",
            "user-agent": "spreadsheets600-api",
        },
    )

    if response.status != 200:
        raise RuntimeError(f"anilist cache returned {response.status}")

    payload = await response.json()
    return payload or None
