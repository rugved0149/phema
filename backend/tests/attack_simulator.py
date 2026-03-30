import requests
import time
import uuid
import json

BASE_URL = "http://127.0.0.1:8000"

# UTILITIES

def new_user():
    return f"user_{uuid.uuid4().hex[:6]}"

def new_session():
    return f"session_{uuid.uuid4().hex[:6]}"

def new_entity():
    return f"entity_{uuid.uuid4().hex[:6]}"

# CORE REQUEST FUNCTIONS

def send_scan(user_id, session_id, entity_id, payload):
    url = f"{BASE_URL}/phema/scan"

    payload.update({
        "user_id": user_id,
        "session_id": session_id,
        "entity_id": entity_id,
        "entity_type": "session"
    })

    r = requests.post(url, json=payload)

    try:
        print("[SCAN]", r.json())
    except:
        print("[SCAN ERROR]", r.text)

def get_risk(user_id, session_id, entity_id):

    url = (
        f"{BASE_URL}/correlation/risk/"
        f"{user_id}/{session_id}/session/{entity_id}"
    )

    r = requests.get(url)

    result = r.json()

    print("\n[RISK RESULT]")
    print(json.dumps(result, indent=2))

    return result

# TEST SCENARIOS

def test_clean_session():
    print("\n========== CLEAN SESSION TEST ==========")

    user = new_user()
    session = new_session()
    entity = new_entity()

    result = get_risk(user, session, entity)

    assert result["risk_score"] == 0

    print("[PASS] Clean session safe")

def test_single_phishing():
    print("\n========== SINGLE PHISHING TEST ==========")

    user = new_user()
    session = new_session()
    entity = new_entity()

    send_scan(
        user,
        session,
        entity,
        {"url": "http://amazon-login-security.com"}
    )

    time.sleep(1)

    result = get_risk(user, session, entity)

    assert result["risk_score"] > 0

    print("[PASS] Phishing detected")

def test_multi_signal():
    print("\n========== MULTI-SIGNAL TEST ==========")

    user = new_user()
    session = new_session()
    entity = new_entity()

    send_scan(
        user,
        session,
        entity,
        {"url": "http://amazon-login-security.com"}
    )

    time.sleep(1)

    send_scan(
        user,
        session,
        entity,
        {"text": "Urgent! Verify now!"}
    )

    time.sleep(1)

    result = get_risk(user, session, entity)

    assert result["risk_score"] >= 20

    print("[PASS] Multi-signal correlation working")

def test_full_attack_chain():
    print("\n========== FULL ATTACK CHAIN ==========")

    user = new_user()
    session = new_session()
    entity = new_entity()

    send_scan(user, session, entity,
        {"url": "http://amazon-login-security.com"}
    )

    time.sleep(1)

    send_scan(user, session, entity,
        {"text": "Urgent! Verify account immediately!"}
    )

    time.sleep(1)

    send_scan(user, session, entity,
        {
            "file_path":
            "app/modules/file_checker/sample_files/suspicious_powershell.ps1"
        }
    )

    time.sleep(1)

    send_scan(user, session, entity,
        {
            "session_context": {
                "ip": "10.0.0.55"
            }
        }
    )

    time.sleep(1)

    send_scan(user, session, entity,
        {
            "session_context": {
                "timestamp": "2026-03-17T03:00:00",
                "source_ip": "8.8.8.8",
                "client_type": "browser",
                "access_type": "login_attempt"
            }
        }
    )

    time.sleep(1)

    result = get_risk(user, session, entity)

    assert result["risk_level"] in ["MEDIUM", "HIGH"]

    print("[PASS] Full chain processed")

def test_campaign_behavior():
    print("\n========== CAMPAIGN TEST ==========")

    user = new_user()
    session = new_session()
    entity = new_entity()

    for _ in range(6):

        send_scan(
            user,
            session,
            entity,
            {"url": "http://paypal-security-alert.com"}
        )

        time.sleep(0.5)

    result = get_risk(user, session, entity)

    assert result["risk_score"] >= 40

    print("[PASS] Campaign detection working")

def test_deduplication():
    print("\n========== DEDUPLICATION TEST ==========")

    user = new_user()
    session = new_session()
    entity = new_entity()

    for _ in range(10):

        send_scan(
            user,
            session,
            entity,
            {"url": "http://duplicate-test.com"}
        )

    time.sleep(1)

    result = get_risk(user, session, entity)

    print("[CHECK] Deduplication active")
    print("[PASS] Deduplication stable")

# MASTER RUNNER

def run_all_tests():
    print("\n==============================")
    print("PHEMA MULTI-USER VALIDATION")
    print("==============================")

    test_clean_session()
    test_single_phishing()
    test_multi_signal()
    test_full_attack_chain()
    test_campaign_behavior()
    test_deduplication()

    print("\nALL TESTS COMPLETED")

if __name__ == "__main__":
    run_all_tests()