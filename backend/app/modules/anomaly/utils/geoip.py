def lookup_ip(ip_address):
    """
    Basic GeoIP mock lookup.
    Must never crash.
    """

    if not ip_address:
        return "unknown", "unknown"

    try:
        if ip_address.startswith("192.168") or ip_address.startswith("10."):
            return "local", "private_asn"

        if ip_address.startswith("8.8"):
            return "US", "google"

        return "unknown", "unknown"

    except Exception:
        return "unknown", "unknown"