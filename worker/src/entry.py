import asyncio
import time
from urllib.parse import parse_qs, urlparse

from ascii import render
from cache import Cache
from config import load
from sources import anilist, github, spotify, steam, wakatime
from wallpapers import pick
from web import json_response, text_response
from workers import Response, WorkerEntrypoint

SNAPSHOT_TTL = 60 * 15


class Default(WorkerEntrypoint):
    async def fetch(self, request):

        url = urlparse(request.url)
        path = url.path.rstrip("/") or "/"
        params = parse_qs(url.query)

        if request.method == "OPTIONS":
            return Response(
                None,
                status=204,
                headers={
                    "access-control-allow-origin": "*",
                    "access-control-allow-methods": "GET, OPTIONS",
                    "access-control-allow-headers": "content-type",
                },
            )

        cache = Cache(self.env)
        config = load(self.env)

        try:
            if path == "/":
                return json_response(
                    {
                        "name": "spreadsheets600-api",
                        "routes": [
                            "/health",
                            "/header",
                            "/pfp",
                            "/ascii",
                            "/snapshot",
                        ],
                    }
                )

            if path == "/health":
                return json_response(health(config), cache="no-store")

            if path == "/header":
                return await header(config, cache, params)

            if path == "/pfp":
                return Response.redirect(
                    "https://avatars.githubusercontent.com/u/115402296",
                    302,
                )

            if path == "/ascii":
                snapshot = await snapshot_data(config, cache)
                return text_response(render(snapshot), cache="public, max-age=900")

            if path == "/snapshot":
                snapshot = await snapshot_data(config, cache)
                return json_response(snapshot, cache="public, max-age=900")

            return json_response({"Error": "Not Found"}, status=404)

        except Exception as error:
            print(f"Unhandled Worker Error : {error}")

            return json_response(
                {"error": "Internal Code Error", "message": str(error)},
                status=502,
                cache="no-store",
            )


def health(config):
    return {
        "ok": True,
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources": {
            "github": bool(config.github_token),
            "wakatime": bool(config.wakatime_api_key),
            "steam": bool(config.steam_api_key and config.steam_id),
            "spotify": bool(
                config.spotify_client_id
                and config.spotify_client_secret
                and config.spotify_refresh_token
            ),
            "anilist": bool(config.anilist_username),
        },
    }


async def header(config, cache, params):
    directory = (params.get("dir") or [config.wallpaper_dir])[0]
    chosen = await pick(config, cache, directory)

    if (params.get("format") or [""])[0] == "json":
        return json_response(chosen, cache="public, max-age=300")

    return Response.redirect(chosen["url"], 302)


async def snapshot_data(config, cache):
    cached = await cache.get("snapshot")

    if cached:
        return cached

    async def safe(name, coroutine):
        try:
            data = await coroutine
            return {"ok": data is not None, "data": data}

        except Exception as error:
            print(f"{name} Failed: {error}")
            return {"ok": False, "data": None, "error": type(error).__name__}

    results = await asyncio.gather(
        safe("github", github.fetch_stats(config)),
        safe("wakatime", wakatime.fetch_stats(config)),
        safe("steam", steam.fetch_stats(config)),
        safe("spotify", spotify.fetch_stats(config, cache)),
        safe("anilist", anilist.fetch_stats(config)),
    )

    snapshot = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "github": results[0],
        "wakatime": results[1],
        "steam": results[2],
        "spotify": results[3],
        "anilist": results[4],
    }

    await cache.set("snapshot", snapshot, SNAPSHOT_TTL)
    return snapshot
