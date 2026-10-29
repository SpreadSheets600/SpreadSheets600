"""Network helpers: user agent, image download -> data URI cache."""

import base64
import sys
import urllib.request

UA = "Mozilla/5.0 (compatible; profile-cards/1.0)"

IMG_CACHE = {}


def fetch_img(url, size_hint=None):
    """Download an image and return a data: URI (None on failure)."""
    if not url:
        return None
    if size_hint:
        url += ("&" if "?" in url else "?") + f"s={size_hint}"
    if url in IMG_CACHE:
        return IMG_CACHE[url]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
            mime = (r.headers.get("Content-Type") or "image/jpeg").split(";")[0]
        data = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
    except Exception as e:  # network trouble -> placeholder
        print(
            f"  ! image skipped ({e.__class__.__name__}): {url[:70]}", file=sys.stderr
        )
        data = None
    IMG_CACHE[url] = data
    return data
