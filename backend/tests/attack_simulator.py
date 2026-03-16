import requests
import time

BASE_URL = "http://127.0.0.1:8000"

ENTITY_ID = "attack_sim_1"


def send_phema(payload):
    url = f"{BASE_URL}/phema/scan"
    r = requests.post(url, json=payload)
    print("[SCAN]", r.json())


def get_risk():
    url = f"{BASE_URL}/correlation/risk/session/{ENTITY_ID}"
    r = requests.get(url)
    print("\nFINAL RISK RESULT")
    print(r.json())


# -------------------------
# ATTACK SCENARIOS
# -------------------------

def simulate_phishing_attack():

    print("\n[SIM] Phishing URL")

    send_phema({
        "entity_id": ENTITY_ID,
        "entity_type": "session",
        "url": "http://amazon-login-security.com"
    })


def simulate_social_engineering():

    print("\n[SIM] Manipulative message")

    send_phema({
        "entity_id": ENTITY_ID,
        "entity_type": "session",
        "text": "URGENT action required verify account immediately"
    })


def simulate_malware_delivery():

    print("\n[SIM] Suspicious file")

    send_phema({
        "entity_id": ENTITY_ID,
        "entity_type": "session",
        "file_path": "app/modules/file_checker/sample_files/suspicious_powershell.ps1"
    })


def simulate_honeypot_trigger():

    print("\n[SIM] Honeypot access")

    send_phema({
        "entity_id": ENTITY_ID,
        "entity_type": "session",
        "session_context": {
            "ip": "10.0.0.55"
        }
    })

def simulate_anomaly():

    print("\n[SIM] Behavioral anomaly")

    send_phema({
        "entity_id": ENTITY_ID,
        "entity_type": "session",
        "session_context": {
            "timestamp": "2026-03-17T03:00:00",
            "source_ip": "8.8.8.8",
            "client_type": "browser",
            "access_type": "login_attempt"
        }
    })
    
# -------------------------
# FULL ATTACK CHAIN
# -------------------------

def simulate_full_attack():

    simulate_phishing_attack()
    time.sleep(1)

    simulate_social_engineering()
    time.sleep(1)

    simulate_malware_delivery()
    time.sleep(1)

    simulate_honeypot_trigger()
    time.sleep(1)

    simulate_anomaly()
    time.sleep(1)

    get_risk()


if __name__ == "__main__":
    simulate_full_attack()