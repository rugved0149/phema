# Scoring weights per rule (points added to risk score)

SCORING_WEIGHTS = {
    # Structural
    "IP address used": 30,
    "Very long URL": 20,
    "Long URL": 10,
    "Excessive subdomains (>5)": 25,
    "Many subdomains (>3)": 15,

    # Hosting / delivery
    "URL shortener used": 20,
    "Suspicious TLD": 20,
    "High-risk country TLD": 10,

    # Keyword-based
    "Authentication keyword": 10,
    "Urgency keyword": 10,

    # Brand-related
    "Brand impersonation": 30,
    "Typosquatted domain": 30,

    # Obfuscation
    "Unicode / homograph domain": 30,
    "High entropy URL": 15,
}

# Category-wise saturation caps (prevents one class dominating)
CATEGORY_CAPS = {
    "structural": 40,
    "hosting": 30,
    "keyword": 30,
    "brand": 40,
    "obfuscation": 30,
}
