ATTACK_CHAINS = [

    {
        "name": "social_engineering_attack",
        "modules": {"phishing", "tone"},
        "score_bonus": 20,
        "reason": "Phishing link combined with manipulative tone"
    },

    {
        "name": "credential_harvest_attack",
        "signals": {"tone:credential_harvest", "phishing"},
        "score_bonus": 25,
        "reason": "Credential harvesting pattern detected"
    },

    {
        "name": "malware_delivery",
        "modules": {"phishing", "file_checker"},
        "score_bonus": 30,
        "reason": "Phishing vector delivering suspicious file"
    },

    {
        "name": "active_intrusion",
        "modules": {"honeypot", "anomaly"},
        "score_bonus": 40,
        "reason": "Intrusion behavior detected through honeypot interaction"
    }
]