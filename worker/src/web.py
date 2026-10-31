from workers import Response

CORS = {"access-control-allow-origin": "*"}


def json_response(data, status: int = 200, cache: str = "public, max-age=60"):
    return Response.json(
        data,
        status=status,
        headers={**CORS, "cache-control": cache},
    )


def text_response(text: str, status: int = 200, cache: str = "public, max-age=60"):
    return Response(
        text,
        status=status,
        headers={
            **CORS,
            "content-type": "text/plain; charset=utf-8",
            "cache-control": cache,
        },
    )
