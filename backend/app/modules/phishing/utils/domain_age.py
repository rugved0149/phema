import whois
from datetime import datetime

CACHE = {}

MAX_CACHE_SIZE = 1000

YOUNG_DOMAIN_DAYS = 7


def is_young_domain(domain: str) -> bool:
    """
    Check if domain is recently registered.
    Uses in-memory cache to reduce WHOIS calls.
    """

    if not domain:
        return False

    if domain in CACHE:
        return CACHE[domain]

    try:

        w = whois.whois(domain)

        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if not creation_date:
            CACHE[domain] = False
            return False

        age_days = (datetime.utcnow() - creation_date).days

        is_young = age_days < YOUNG_DOMAIN_DAYS

        if len(CACHE) > MAX_CACHE_SIZE:
            CACHE.clear()

        CACHE[domain] = is_young

        return is_young

    except Exception:

        CACHE[domain] = False
        return False