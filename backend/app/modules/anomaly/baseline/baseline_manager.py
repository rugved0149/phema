import json
from datetime import datetime

from app.modules.anomaly.db.database import get_connection
from app.modules.anomaly.baseline.stats import update_ema, update_std

LEARNING_EVENTS_THRESHOLD = 50


def load_baseline():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM baseline_profile WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    return row


def get_event_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM access_events")
    count = cur.fetchone()[0]
    conn.close()
    return count


def is_learning_mode():
    return get_event_count() < LEARNING_EVENTS_THRESHOLD


def update_baseline_with_event(event):
    """
    Update baseline ONLY during learning or normal verdicts
    """
    conn = get_connection()
    cur = conn.cursor()

    baseline = load_baseline()

    mean_hour = update_ema(baseline["mean_access_hour"], event["hour"])
    std_hour = update_std(
        baseline["std_access_hour"],
        baseline["mean_access_hour"],
        event["hour"]
    )

    known_countries = json.loads(baseline["known_countries"])
    known_asns = json.loads(baseline["known_asns"])
    known_clients = json.loads(baseline["known_clients"])

    if event["country"] not in known_countries:
        known_countries.append(event["country"])

    if event["asn"] not in known_asns:
        known_asns.append(event["asn"])

    if event["client_type"] not in known_clients:
        known_clients.append(event["client_type"])

    cur.execute("""
        UPDATE baseline_profile SET
            mean_access_hour = ?,
            std_access_hour = ?,
            known_countries = ?,
            known_asns = ?,
            known_clients = ?,
            last_updated = ?
        WHERE id = 1
    """, (
        mean_hour,
        std_hour,
        json.dumps(known_countries),
        json.dumps(known_asns),
        json.dumps(known_clients),
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
