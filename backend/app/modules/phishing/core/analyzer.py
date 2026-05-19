from app.modules.phishing.utils.ip_check import is_ip_address
from app.modules.phishing.utils.string_utils import tokenize, levenshtein_distance
from app.modules.phishing.utils.unicode_check import contains_unicode, is_punycode
from app.modules.phishing.utils.entropy import shannon_entropy
from app.modules.phishing.utils.domain_age import is_young_domain
from app.modules.phishing.rules.keywords import AUTH_KEYWORDS, URGENCY_KEYWORDS
from app.modules.phishing.rules.brands import BRANDS
from app.modules.phishing.rules.shorteners import SHORTENERS
from app.modules.phishing.rules.tlds import SUSPICIOUS_TLDS, COUNTRY_TLDS
from app.modules.phishing.rules.brand_domains import BRAND_DOMAINS


# Move outside function (performance-safe)

REDIRECT_PARAMS = {
    "redirect",
    "url",
    "next",
    "continue",
    "dest",
    "destination",
    "return",
    "returnurl"
}


def analyze(parsed: dict) -> list:
    """
    Run heuristic analysis on parsed URL components.
    Returns a list of triggered rule dictionaries.
    """

    triggers = []

    host = parsed.get("netloc", "")
    path = parsed.get("path", "")
    query = parsed.get("query", "")
    fragment = parsed.get("fragment", "")

    full_domain = parsed.get("full_domain", "")
    subdomain = parsed.get("subdomain", "")
    domain = parsed.get("domain", "")
    suffix = parsed.get("suffix", "")
    url_length = parsed.get("url_length", 0)
    registered_domain = parsed.get("registered_domain", "")
    if registered_domain:
        if is_young_domain(registered_domain):

            triggers.append({
                "rule": "Young domain age",
                "category": "hosting"
            })

    # Normalize once (performance-safe)

    query_lower = query.lower() if query else ""
    fragment_lower = fragment.lower() if fragment else ""

    # -------------------------------------------------
    # Redirect Parameter Detection (Query)
    # -------------------------------------------------

    if query_lower:

        for param in REDIRECT_PARAMS:

            if f"{param}=" in query_lower:

                triggers.append({
                    "rule": "Redirect parameter detected",
                    "category": "obfuscation"
                })

                break

    # -------------------------------------------------
    # Redirect Parameter Detection (Fragment)
    # -------------------------------------------------

    if fragment_lower:

        for param in REDIRECT_PARAMS:

            if f"{param}=" in fragment_lower:

                triggers.append({
                    "rule": "Redirect in fragment",
                    "category": "obfuscation"
                })

                break

    # -------------------------------------------------
    # VERIFIED BRAND DOMAIN CHECK (TRUST BOUNDARY)
    # -------------------------------------------------

    is_verified_brand_domain = False

    for domains in BRAND_DOMAINS.values():

        if registered_domain in domains:

            is_verified_brand_domain = True
            break

    # -------------------------------------------------
    # Structural Checks
    # -------------------------------------------------

    if is_ip_address(host):

        triggers.append({
            "rule": "IP address used",
            "category": "structural"
        })

    if not is_verified_brand_domain:

        if url_length > 120:

            triggers.append({
                "rule": "Very long URL",
                "category": "structural"
            })

        elif url_length > 75:

            triggers.append({
                "rule": "Long URL",
                "category": "structural"
            })

    if subdomain:

        depth = subdomain.count(".") + 1

        if depth > 5:

            triggers.append({
                "rule": "Excessive subdomains (>5)",
                "category": "structural"
            })

        elif depth > 3:

            triggers.append({
                "rule": "Many subdomains (>3)",
                "category": "structural"
            })

    # -------------------------------------------------
    # Hosting Checks
    # -------------------------------------------------

    if domain and suffix:

        reg = f"{domain}.{suffix}"

        if reg in SHORTENERS:

            triggers.append({
                "rule": "URL shortener used",
                "category": "hosting"
            })

    if suffix in SUSPICIOUS_TLDS:

        triggers.append({
            "rule": "Suspicious TLD",
            "category": "hosting"
        })

    if suffix in COUNTRY_TLDS:

        triggers.append({
            "rule": "High-risk country TLD",
            "category": "hosting"
        })

    # -------------------------------------------------
    # Unicode / Homograph Detection
    # -------------------------------------------------

    if contains_unicode(full_domain) or is_punycode(full_domain):

        triggers.append({
            "rule": "Unicode / homograph domain",
            "category": "obfuscation"
        })

    # -------------------------------------------------
    # Tokenization
    # -------------------------------------------------

    domain_tokens = tokenize(domain.replace("-", " "))

    tokens = (
        domain_tokens
        + tokenize(subdomain)
        + tokenize(path)
        + tokenize(query)
        + tokenize(fragment)
    )

    # -------------------------------------------------
    # Keyword Detection
    # -------------------------------------------------

    if not is_verified_brand_domain:

        for token in tokens:

            if token in AUTH_KEYWORDS:

                triggers.append({
                    "rule": "Authentication keyword",
                    "category": "keyword"
                })

            if token in URGENCY_KEYWORDS:

                triggers.append({
                    "rule": "Urgency keyword",
                    "category": "keyword"
                })

    # -------------------------------------------------
    # Brand Impersonation & Typosquatting
    # -------------------------------------------------

    for brand in BRANDS:

        official_domains = BRAND_DOMAINS.get(brand, set())

        if registered_domain in official_domains:
            continue

        if levenshtein_distance(domain, brand) <= 1 and domain != brand:

            triggers.append({
                "rule": "Typosquatted domain",
                "category": "brand"
            })

            continue

        if brand in tokens:

            triggers.append({
                "rule": "Brand impersonation",
                "category": "brand"
            })

    # -------------------------------------------------
    # Entropy Detection
    # -------------------------------------------------

    if not is_verified_brand_domain:

        entropy_target = path + query + fragment

        if shannon_entropy(entropy_target) > 4.0:

            triggers.append({
                "rule": "High entropy URL",
                "category": "obfuscation"
            })

    return triggers