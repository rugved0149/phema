from datetime import datetime
from app.modules.anomaly.ingestion.phema_adapter import emit_phema_event
import logging
from app.modules.anomaly.detection.scorer import evaluate_signals
from app.modules.anomaly.db.database import get_connection
from app.modules.anomaly.utils.time_utils import extract_time_features
from app.modules.anomaly.utils.geoip import lookup_ip
from app.modules.anomaly.baseline.baseline_manager import is_learning_mode, update_baseline_with_event
from app.modules.module_adapter import send_event

REQUIRED_FIELDS = {"timestamp", "source_ip", "client_type", "access_type"}


def validate_event(payload):
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        raise ValueError(f"Missing fields: {missing}")


def get_time_since_last_access():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT timestamp FROM access_events ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    last_time = datetime.fromisoformat(row["timestamp"])
    return (datetime.utcnow() - last_time).total_seconds()


def ingest_event(payload):
    validate_event(payload)

    timestamp = payload["timestamp"]
    source_ip = payload["source_ip"]
    client_type = payload["client_type"]
    access_type = payload["access_type"]

    hour, day = extract_time_features(timestamp)
    country, asn = lookup_ip(source_ip)
    time_since_last = get_time_since_last_access()

    conn = get_connection()
    cur = conn.cursor()

    # Insert event
    cur.execute(
        """
        INSERT INTO access_events (
            timestamp, hour, day,
            source_ip, country, asn,
            client_type, access_type,
            time_since_last
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            timestamp,
            hour,
            day,
            source_ip,
            country,
            asn,
            client_type,
            access_type,
            time_since_last,
        ),
    )

    event_id = cur.lastrowid

    # Fetch inserted event
    cur.execute("SELECT * FROM access_events WHERE id = ?", (event_id,))
    event_row = cur.fetchone()

    conn.commit()
    conn.close()

    logging.info(
        f"Event ingested | id={event_id} ip={source_ip} "
        f"client={client_type} access={access_type}"
    )

    # ============================
    # Behavioral Deviation Detection
    # ============================

    deviations = []
    print("Learning mode:", is_learning_mode())
    if is_learning_mode():
        # Learn baseline only
        update_baseline_with_event(event_row)
    else:
        # Evaluate independent anomaly signals
        deviations = evaluate_signals(event_row)

        # Learn only if no deviations detected
        if not deviations:
            update_baseline_with_event(event_row)

    # ============================
    # Emit PHEMA Events
    # ============================

    for deviation in deviations:
        phema_event = emit_phema_event(**deviation)

        send_event(
            entity_id=phema_event["entity_id"],
            entity_type=phema_event["entity_type"],
            module=phema_event["module"],
            signal=phema_event["signal"],
            confidence=phema_event["confidence"],
            severity=phema_event["severity"],
            metadata=phema_event["metadata"],
    )

    return event_id
