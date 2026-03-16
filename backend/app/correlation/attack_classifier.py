# app/correlation/attack_classifier.py

from typing import List, Set


ATTACK_PATTERNS = {

    "social_engineering": {
        "modules": {"phishing", "tone"},
        "description": "Phishing combined with manipulative messaging"
    },

    "malware_delivery": {
        "modules": {"phishing", "file_checker"},
        "description": "Phishing vector delivering suspicious file"
    },

    "credential_harvesting": {
        "signals": {"credential_harvest"},
        "description": "Attempt to collect authentication credentials"
    },

    "intrusion_attempt": {
        "modules": {"honeypot", "anomaly"},
        "description": "Suspicious system interaction detected"
    }

}


def classify_attack(modules: Set[str], signals: List[str]):

    detected_attacks = []

    for attack, rule in ATTACK_PATTERNS.items():

        # Module-based detection
        if "modules" in rule:
            if rule["modules"].issubset(modules):
                detected_attacks.append(attack)

        # Signal-based detection
        if "signals" in rule:
            if any(sig in s for s in signals for sig in rule["signals"]):
                detected_attacks.append(attack)

    if not detected_attacks:
        return {
            "attack_type": "unknown",
            "confidence": "low"
        }

    if len(detected_attacks) == 1:
        return {
            "attack_type": detected_attacks[0],
            "confidence": "medium"
        }

    return {
        "attack_type": "multi_stage_attack",
        "confidence": "high"
    }