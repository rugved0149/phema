# app/correlation/mitre_mapper.py

from typing import List, Set


MITRE_MODULE_MAP = {
    "phishing": [
        ("T1566", "Phishing"),
    ],

    "tone": [
        ("T1566.002", "Spearphishing Link"),
    ],

    "file_checker": [
        ("T1204", "User Execution"),
        ("T1059", "Command Execution"),
    ],

    "honeypot": [
        ("T1190", "Exploit Public-Facing Application"),
    ],

    "anomaly": [
        ("T1078", "Valid Accounts"),
        ("T1036", "Masquerading"),
    ]
}


MITRE_SIGNAL_MAP = {
    "credential_harvest": ("T1556", "Modify Authentication Process"),
    "payload_delivery": ("T1204", "User Execution"),
    "brand_impersonation": ("T1566", "Phishing"),
}


def map_to_mitre(modules: Set[str], signals: List[str]):

    techniques = []

    # Module-based mapping
    for module in modules:
        if module in MITRE_MODULE_MAP:
            techniques.extend(MITRE_MODULE_MAP[module])

    # Signal-based mapping
    for signal in signals:
        for key in MITRE_SIGNAL_MAP:
            if key in signal:
                techniques.append(MITRE_SIGNAL_MAP[key])

    # Remove duplicates
    techniques = list(set(techniques))

    return [
        f"{tech_id}: {name}"
        for tech_id, name in techniques
    ]