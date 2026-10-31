from workers import Response

CORS = {"access-control-allow-origin": "*"}


def json_response(data, status=200, cache="public, max-age=60"):
    return Response.json(
        data,
        status=status,
        headers={**CORS, "cache-control": cache},
    )


def text_response(text, status=200, cache="public, max-age=60"):
    return Response(
        text,
        status=status,
        headers={
            **CORS,
            "content-type": "text/plain; charset=utf-8",
            "cache-control": cache,
        },
    )
