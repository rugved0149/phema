from urllib.parse import urlparse
import tldextract


def parse_url(url: str) -> dict:
    """
    Parse a normalized URL into security-relevant components.
    """

    parsed = urlparse(url)
    extracted = tldextract.extract(url)

    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "subdomain": extracted.subdomain,
        "domain": extracted.domain,
        "suffix": extracted.suffix,
        "registered_domain": (
            f"{extracted.domain}.{extracted.suffix}"
            if extracted.domain and extracted.suffix
            else ""
        ),
        "full_domain": parsed.netloc,
        "url_length": len(url),
    }
