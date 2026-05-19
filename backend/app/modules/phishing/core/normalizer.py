from urllib.parse import urlparse, urlunparse, unquote


def deep_unquote(url: str, max_depth: int = 3):

    previous = url

    for _ in range(max_depth):

        decoded = unquote(previous)

        if decoded == previous:
            break

        previous = decoded

    return previous


def normalize_url(raw_url: str) -> str:

    if not raw_url:
        raise ValueError("Empty URL")

    url = raw_url.strip().lower()

    # Replace single decode with deep decode
    url = deep_unquote(url)

    # Ensure scheme
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    scheme = parsed.scheme
    netloc = parsed.netloc
    path = parsed.path or "/"
    query = parsed.query
    fragment = ""

    # Remove default ports
    if netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif netloc.endswith(":443"):
        netloc = netloc[:-4]

    # Normalize www
    if netloc.startswith("www."):
        netloc = netloc[4:]

    # Normalize trailing slash
    if path != "/" and path.endswith("/"):
        path = path[:-1]

    return urlunparse((scheme, netloc, path, "", query, fragment))