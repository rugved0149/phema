# app/correlation/attack_classifier.py

from typing import List, Set


# -------------------------
# ATTACK PATTERN RULES
# -------------------------

ATTACK_PATTERNS = {

    "social_engineering": {
        "modules": {"phishing", "tone"},
        "description": "Phishing combined with manipulative messaging",
        "priority": 3
    },

    "malware_delivery": {
        "modules": {"phishing", "file_checker"},
        "description": "Phishing vector delivering suspicious file",
        "priority": 4
    },

    "credential_harvesting": {
        "signals": {"credential_harvest"},
        "description": "Attempt to collect authentication credentials",
        "priority": 5
    },

    "intrusion_attempt": {
        "modules": {"honeypot", "anomaly"},
        "description": "Suspicious system interaction detected",
        "priority": 6
    }

}


# -------------------------
# SIGNAL PARSER
# -------------------------

def extract_signal_name(signal: str) -> str:
    """
    Extract final signal component.

    Example:
        tone:manipulation:urgency → urgency
        file:obfuscation:high_entropy → high_entropy
    """

    parts = signal.split(":")
    return parts[-1] if parts else signal


# -------------------------
# MAIN CLASSIFIER
# -------------------------

def classify_attack(modules: Set[str], signals: List[str]):

    detected_attacks = []

    # Extract clean signal names
    clean_signals = {
        extract_signal_name(s)
        for s in signals
    }

    for attack, rule in ATTACK_PATTERNS.items():

        matched = False

        # -------------------------
        # Module-based detection
        # -------------------------

        if "modules" in rule:
            if rule["modules"].issubset(modules):
                matched = True

        # -------------------------
        # Signal-based detection
        # -------------------------

        if "signals" in rule:
            if rule["signals"].intersection(clean_signals):
                matched = True

        if matched:
            detected_attacks.append({
                "attack": attack,
                "priority": rule.get("priority", 1)
            })

    # -------------------------
    # No detection
    # -------------------------

    if not detected_attacks:
        return {
            "attack_type": "unknown",
            "confidence": "low"
        }

    # -------------------------
    # Select highest priority
    # -------------------------

    detected_attacks.sort(
        key=lambda x: x["priority"],
        reverse=True
    )

    top_attack = detected_attacks[0]["attack"]

    # -------------------------
    # Multi-stage detection
    # -------------------------

    if len(detected_attacks) > 1:
        return {
            "attack_type": top_attack,
            "confidence": "high"
        }

    return {
        "attack_type": top_attack,
        "confidence": "medium"
    }