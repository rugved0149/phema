def contains_unicode(text: str) -> bool:
    """
    Detect non-ASCII (Unicode) characters in a string.
    """
    if not text:
        return False

    try:
        text.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True


def is_punycode(domain: str) -> bool:
    """
    Detect punycode domains (xn--).
    """
    if not domain:
        return False

    return domain.startswith("xn--") or ".xn--" in domain
