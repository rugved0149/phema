import requests

MAX_REDIRECTS = 3
TIMEOUT = 3


def resolve_redirect(url: str) -> str:
    """
    Resolve redirect chains safely.
    Returns final destination URL if redirect exists.
    Falls back to original URL if failure occurs.
    """

    try:

        response = requests.head(
            url,
            allow_redirects=True,
            timeout=TIMEOUT
        )

        final_url = response.url

        if final_url and final_url != url:
            return final_url

        return url

    except Exception:

        return url