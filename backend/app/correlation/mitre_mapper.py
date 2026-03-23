from typing import List, Dict, Set


# -------------------------
# MITRE MAPPING (MODULE LEVEL)
# -------------------------

MODULE_TO_MITRE = {
    "phishing": [
        {"id": "T1566", "name": "Phishing"}
    ],
    "tone": [
        {"id": "T1566", "name": "Social Engineering"}
    ],
    "file_checker": [
        {"id": "T1204", "name": "User Execution"}
    ],
    "honeypot": [
        {"id": "T1046", "name": "Network Service Discovery"}
    ],
    "anomaly": [
        {"id": "T1078", "name": "Valid Accounts"}
    ]
}


# -------------------------
# SIGNAL LEVEL (STRUCTURED)
# key = final signal token
# -------------------------

SIGNAL_TO_MITRE = {

    # Credential harvesting
    "credential_harvest": [
        {"id": "T1556", "name": "Credential Harvesting"}
    ],

    # Obfuscation
    "high_entropy": [
        {"id": "T1027", "name": "Obfuscated Files"}
    ],

    # Suspicious execution indicators
    "suspicious_string": [
        {"id": "T1059", "name": "Command Execution"}
    ],

    # Honeypot
    "shadow_ban": [
        {"id": "T1562", "name": "Defense Evasion"}
    ],

    "block": [
        {"id": "T1078", "name": "Account Blocking Response"}
    ],

    # Phishing brand impersonation
    "impersonation": [
        {"id": "T1566.002", "name": "Spearphishing Link"}
    ]
}


# -------------------------
# ATTACK TYPE LEVEL
# -------------------------

ATTACK_TYPE_TO_MITRE = {

    "social_engineering": [
        {"id": "T1566", "name": "Phishing"}
    ],

    "malware_delivery": [
        {"id": "T1204", "name": "User Execution"}
    ],

    "credential_harvesting": [
        {"id": "T1556", "name": "Credential Harvesting"}
    ],

    "intrusion_attempt": [
        {"id": "T1046", "name": "Network Discovery"}
    ]
}


# -------------------------
# HELPER FUNCTION
# -------------------------

def extract_signal_token(signal: str) -> str:
    """
    Extract final signal component from structured signal.

    Example:
        'file:obfuscation:high_entropy'
        → 'high_entropy'
    """

    if not signal:
        return ""

    parts = signal.split(":")

    return parts[-1] if parts else signal


# -------------------------
# MAIN FUNCTION
# -------------------------

def map_to_mitre(
    modules: Set[str],
    signals: List[str],
    attack_type: str = None
) -> List[Dict]:

    results: List[Dict] = []
    seen = set()

    # -------------------------
    # MODULE LEVEL
    # -------------------------

    for module in modules:

        techniques = MODULE_TO_MITRE.get(module, [])

        for t in techniques:

            if t["id"] not in seen:

                results.append(t)
                seen.add(t["id"])

    # -------------------------
    # SIGNAL LEVEL
    # -------------------------

    for signal in signals:

        token = extract_signal_token(signal)

        techniques = SIGNAL_TO_MITRE.get(token, [])

        for t in techniques:

            if t["id"] not in seen:

                results.append(t)
                seen.add(t["id"])

    # -------------------------
    # ATTACK TYPE LEVEL
    # -------------------------

    if attack_type:

        techniques = ATTACK_TYPE_TO_MITRE.get(
            attack_type,
            []
        )

        for t in techniques:

            if t["id"] not in seen:

                results.append(t)
                seen.add(t["id"])

    return results