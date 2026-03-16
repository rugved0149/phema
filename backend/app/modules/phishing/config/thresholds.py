# Final verdict thresholds based on aggregated risk score

THRESHOLDS = {
    "LEGITIMATE": 0,
    "SUSPICIOUS": 25,
    "PHISHING": 50
}


def get_verdict(score: int) -> str:
    """
    Determine verdict label based on total risk score.
    """
    if score >= THRESHOLDS["PHISHING"]:
        return "Likely Phishing"
    elif score >= THRESHOLDS["SUSPICIOUS"]:
        return "Suspicious"
    return "Legitimate"
