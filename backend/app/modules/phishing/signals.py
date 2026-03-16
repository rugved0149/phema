# maps internal rule names → PHEMA signal attributes

SIGNAL_MAP = {
    "IP address used": {
        "signal": "ip_based_url",
        "confidence": 0.9,
        "severity": "high"
    },
    "URL shortener used": {
        "signal": "url_shortener_used",
        "confidence": 0.6,
        "severity": "medium"
    },
    "Suspicious TLD": {
        "signal": "suspicious_tld",
        "confidence": 0.7,
        "severity": "medium"
    },
    "High-risk country TLD": {
        "signal": "high_risk_country_tld",
        "confidence": 0.7,
        "severity": "medium"
    },
    "Unicode / homograph domain": {
        "signal": "homograph_attack",
        "confidence": 0.9,
        "severity": "high"
    },
    "Authentication keyword": {
        "signal": "auth_keyword_detected",
        "confidence": 0.6,
        "severity": "medium"
    },
    "Urgency keyword": {
        "signal": "urgency_keyword_detected",
        "confidence": 0.6,
        "severity": "medium"
    },
    "Brand impersonation": {
        "signal": "brand_impersonation",
        "confidence": 0.85,
        "severity": "high"
    },
    "Typosquatted domain": {
        "signal": "typosquatting_detected",
        "confidence": 0.9,
        "severity": "high"
    },
    "High entropy URL": {
        "signal": "url_obfuscation",
        "confidence": 0.65,
        "severity": "medium"
    },
    "Young domain age": {
        "signal": "young_domain",
        "confidence": 0.6,
        "severity": "low"
    },
    "Known phishing URL": {
        "signal": "known_phishing_indicator",
        "confidence": 0.95,
        "severity": "high"
    }
}
