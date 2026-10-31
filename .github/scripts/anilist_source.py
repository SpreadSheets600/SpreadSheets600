import base64
import json
import urllib.request

ENDPOINT = "https://graphql.anilist.co"
USER_AGENT = "spreadsheets600-profile-action"

QUERY = """
query($userName: String) {
  User(name: $userName) {
    id
    name
    about
    avatar { large }
    bannerImage
    createdAt
    updatedAt
    statistics {
      anime {
        count
        meanScore
        minutesWatched
        episodesWatched
        statuses { status count meanScore }
        genres(limit: 8, sort: COUNT_DESC) {
          genre
          count
          minutesWatched
        }
      }
      manga {
        count
        chaptersRead
        volumesRead
        meanScore
        statuses { status count meanScore }
        genres(limit: 8, sort: COUNT_DESC) {
          genre
          count
        }
      }
    }
  }
  latestAnime: MediaListCollection(userName: $userName, type: ANIME, sort: [UPDATED_TIME_DESC]) {
    lists { entries { ...Entry } }
  }
  latestManga: MediaListCollection(userName: $userName, type: MANGA, sort: [UPDATED_TIME_DESC]) {
    lists { entries { ...Entry } }
  }
}

fragment Entry on MediaList {
  status
  progress
  updatedAt
  media {
    id
    title { romaji english }
    episodes
    chapters
    coverImage { medium }
  }
}
"""


def _statuses(items):
    return [
        {
            "status": item.get("status"),
            "count": item.get("count") or 0,
            "meanScore": item.get("meanScore") or 0,
        }
        for item in items or []
    ]


def _genres(items, include_minutes=False):
    genres = []

    for item in items or []:
        genre = {
            "genre": item.get("genre"),
            "count": item.get("count") or 0,
        }

        if include_minutes:
            genre["minutesWatched"] = item.get("minutesWatched") or 0

        genres.append(genre)

    return genres


def _latest(payload, key, total_field):
    collection = (payload.get("data") or {}).get(key) or {}
    entries = [
        entry
        for media_list in collection.get("lists") or []
        for entry in media_list.get("entries") or []
        if entry.get("status") != "PLANNING" and (entry.get("progress") or 0) > 0
    ]

    if not entries:
        return None

    entry = max(entries, key=lambda item: item.get("updatedAt") or 0)
    media = entry.get("media") or {}
    title = media.get("title") or {}
    cover_url = (media.get("coverImage") or {}).get("medium")

    return {
        "mediaId": media.get("id"),
        "title": title.get("english") or title.get("romaji"),
        "status": entry.get("status"),
        "progress": entry.get("progress") or 0,
        "total": media.get(total_field),
        "updatedAt": entry.get("updatedAt"),
        "cover": _data_uri(cover_url) if cover_url else None,
    }


def _data_uri(url):
    try:
        request = urllib.request.Request(url, headers={"user-agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=30) as response:
            mime = response.headers.get_content_type()
            return f"data:{mime};base64,{base64.b64encode(response.read()).decode()}"
    except OSError:
        return None


def _normalise(payload):
    data = payload.get("data") or {}
    user = data.get("User")

    if not user:
        return None

    statistics = user.get("statistics") or {}
    anime = statistics.get("anime") or {}
    manga = statistics.get("manga") or {}
    minutes_watched = anime.get("minutesWatched") or 0

    return {
        "user": {
            "id": user.get("id"),
            "name": user.get("name"),
            "about": user.get("about"),
            "avatar": (user.get("avatar") or {}).get("large"),
            "bannerImage": user.get("bannerImage"),
            "createdAt": user.get("createdAt"),
            "updatedAt": user.get("updatedAt"),
        },
        "anime": {
            "count": anime.get("count") or 0,
            "meanScore": anime.get("meanScore") or 0,
            "minutesWatched": minutes_watched,
            "hoursWatched": round(minutes_watched / 60, 2),
            "daysWatched": round(minutes_watched / 1440, 2),
            "episodesWatched": anime.get("episodesWatched") or 0,
            "statuses": _statuses(anime.get("statuses")),
            "genres": _genres(anime.get("genres"), include_minutes=True),
        },
        "manga": {
            "count": manga.get("count") or 0,
            "meanScore": manga.get("meanScore") or 0,
            "chaptersRead": manga.get("chaptersRead") or 0,
            "volumesRead": manga.get("volumesRead") or 0,
            "statuses": _statuses(manga.get("statuses")),
            "genres": _genres(manga.get("genres")),
        },
        "latestAnime": _latest(payload, "latestAnime", "episodes"),
        "latestManga": _latest(payload, "latestManga", "chapters"),
    }


def fetch_anilist(username):
    body = json.dumps(
        {
            "query": QUERY,
            "variables": {"userName": username},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "accept": "application/json",
            "user-agent": USER_AGENT,
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if payload.get("errors"):
        message = payload["errors"][0].get("message", "unknown GraphQL error")
        raise RuntimeError(f"anilist: {message}")

    data = _normalise(payload)

    if not data:
        raise RuntimeError(f"anilist user not found: {username}")

    return data
