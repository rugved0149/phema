ATTACK_CHAINS = [

    {
        "name": "social_engineering_attack",

        "sequence": [
            "phishing",
            "tone"
        ],

        "score_bonus": 20,

        "reason":
            "Phishing followed by manipulation"
    },

    {
        "name": "malware_delivery",

        "sequence": [
            "phishing",
            "file_checker"
        ],

        "score_bonus": 30,

        "reason":
            "Phishing delivered suspicious file"
    },

    {
        "name": "intrusion",

        "sequence": [
            "honeypot",
            "anomaly"
        ],

        "score_bonus": 40,

        "reason":
            "Intrusion behavior detected"
    }
]