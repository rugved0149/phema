def lookup_country(ip):
    # Offline-safe placeholder
    # In production, use MaxMind / ipinfo
    if ip.startswith("127.") or ip == "localhost":
        return "Localhost"
    return "Unknown"
