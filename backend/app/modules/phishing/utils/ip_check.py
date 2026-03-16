import ipaddress


def is_ip_address(hostname: str) -> bool:
    """
    Check if the given hostname is a valid IPv4 or IPv6 address.
    """
    if not hostname:
        return False

    # Remove port if present
    if ":" in hostname and hostname.count(":") == 1:
        hostname = hostname.split(":")[0]

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False
