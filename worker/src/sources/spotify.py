import base64
from urllib.parse import urlencode

from workers import fetch

TOKEN_URL = "https://accounts.spotify.com/api/token"
NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"

REFRESH_TOKEN_KEY = "spotify:refresh_token"


async def _access_token(config, cache):
    if not (
        config.spotify_client_id
        and config.spotify_client_secret
        and config.spotify_refresh_token
    ):
        return None

    refresh_token = await cache.get(REFRESH_TOKEN_KEY) or config.spotify_refresh_token
    basic = base64.b64encode(
        f"{config.spotify_client_id}:{config.spotify_client_secret}".encode()
    ).decode()

    response = await fetch(
        TOKEN_URL,
        method="POST",
        headers={
            "authorization": f"Basic {basic}",
            "content-type": "application/x-www-form-urlencoded",
        },
        body=urlencode(
            {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        ),
    )

    if response.status != 200:
        raise RuntimeError(f"spotify token returned {response.status}")

    data = await response.json()
    rotated = data.get("refresh_token")

    if rotated and rotated != refresh_token:
        await cache.set(REFRESH_TOKEN_KEY, rotated, 60 * 60 * 24 * 365)

    return data.get("access_token")


async def fetch_stats(config, cache):
    token = await _access_token(config, cache)

    if not token:
        return None

    response = await fetch(
        NOW_PLAYING_URL,
        headers={"authorization": f"Bearer {token}"},
    )

    if response.status == 204:
        return {"playing": False}

    if response.status != 200:
        raise RuntimeError(f"spotify now-playing returned {response.status}")

    data = await response.json()
    item = data.get("item")

    if not item:
        return {"playing": False}

    album = item.get("album") or {}
    images = album.get("images") or [{}]

    return {
        "playing": bool(data.get("is_playing")),
        "title": item.get("name"),
        "artists": ", ".join(
            artist.get("name", "") for artist in item.get("artists") or []
        ),
        "album": album.get("name"),
        "url": (item.get("external_urls") or {}).get("spotify"),
        "image": images[0].get("url"),
        "progress": data.get("progress_ms"),
        "duration": item.get("duration_ms"),
    }
