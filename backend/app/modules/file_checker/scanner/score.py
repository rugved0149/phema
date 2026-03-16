"""
Risk scoring module for Cyber Shield.
Primary static analysis only — analyze, not identify.

Author: Rugved Suryawanshi
"""

from typing import Dict, Any, List


# Category-based weights (intent-driven, not signature-driven)
CATEGORY_WEIGHTS = {
    "execution": 40,
    "loader": 40,
    "injection": 50,
    "credential-access": 60,
    "anti-analysis": 40,
    "persistence": 30,
    "lolbin": 40,
    "obfuscation": 30,
    "surveillance": 50,
    "network": 20,
    "archive": 20,
    "stealth": 20,
    "unknown": 10
}

# Entropy threshold
ENTROPY_THRESHOLD = 7.5


def score_signals(signals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aggregate static analysis signals into a risk score and band.

    Args:
        signals: Dictionary containing entropy and yara_hits

    Returns:
        Dictionary with risk_score, risk_band, and explanation signals
    """
    score = 0
    reasons: List[str] = []

    # ---- Entropy signal ----
    entropy = signals.get("entropy", 0.0)
    if entropy >= ENTROPY_THRESHOLD:
        score += 20
        reasons.append("High entropy (possible packing or obfuscation)")

    # ---- YARA signal aggregation ----
    for hit in signals.get("yara_hits", []):
        category = hit.get("category", "unknown")
        weight = CATEGORY_WEIGHTS.get(category, CATEGORY_WEIGHTS["unknown"])

        score += weight
        reasons.append(
            f"{hit.get('rule')} [{category}] (+{weight})"
        )

    # ---- Score normalization ----
    score = min(score, 100)

    # ---- Risk band assignment ----
    if score >= 70:
        band = "high"
    elif score >= 40:
        band = "medium"
    elif score > 0:
        band = "low"
    else:
        band = "clean"

    return {
        "risk_score": score,
        "risk_band": band,
        "signals": reasons
    }
