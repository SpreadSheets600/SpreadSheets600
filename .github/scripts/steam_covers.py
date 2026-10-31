import base64
import json
import urllib.request

CDN = "https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/{name}"
STORE = "https://store.steampowered.com/api/appdetails?appids={appid}&filters=basic"
USER_AGENT = "spreadsheets600-profile-action"


def _get(url):
    try:
        request = urllib.request.Request(url, headers={"user-agent": USER_AGENT})

        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read(), response.headers.get_content_type()

    except OSError:
        return None


def _cover(appid):
    urls = [
        CDN.format(appid=appid, name=name)
        for name in ("library_600x900.jpg", "header.jpg")
    ]

    for url in urls:
        if found := _get(url):
            body, mime = found
            return f"data:{mime};base64,{base64.b64encode(body).decode()}"

    if found := _get(STORE.format(appid=appid)):
        try:
            art = json.loads(found[0])[str(appid)]["data"]["header_image"]
        except (KeyError, TypeError, ValueError):
            return None

        if image := _get(art):
            return f"data:{image[1]};base64,{base64.b64encode(image[0]).decode()}"

    return None


def attach(steam):
    top = (steam.get("topGames") or [None])[0]
    for key, game in (("mostPlayed", top), ("latestPlayed", steam.get("latestPlayed"))):
        if game:
            steam[key] = {**game, "cover": _cover(game["appid"])}
