from urllib.parse import urlparse, urlunparse, unquote


def normalize_url(raw_url: str) -> str:
    if not raw_url:
        raise ValueError("Empty URL")

    url = raw_url.strip().lower()
    url = unquote(url)

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
