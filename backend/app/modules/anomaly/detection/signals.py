import json
from math import fabs
from ..baseline.baseline_manager import load_baseline

from app.modules.anomaly.db.database import get_connection


# ============================================
# 1️⃣ Unusual Login Time
# ============================================


def time_deviation_signal(event):
    baseline = load_baseline()

    mean = baseline["mean_access_hour"]
    std = baseline["std_access_hour"]

    if mean is None or std is None or std == 0:
        return None

    z_score = fabs(event["hour"] - mean) / std

    # Only emit if statistically significant
    if z_score < 2:
        return None

    confidence = min(z_score / 5.0, 1.0)

    severity = "medium"
    if z_score >= 4:
        severity = "high"

    return {
        "entity_id": event["source_ip"],
        "entity_type": "ip",
        "signal": "unusual_login_time",
        "confidence": round(confidence, 3),
        "severity": severity,
        "metadata": {
            "baseline_mean_hour": mean,
            "baseline_std_hour": std,
            "observed_hour": event["hour"],
            "z_score": round(z_score, 2),
        },
    }


# ============================================
# 2️⃣ Geographic / ASN Change
# ============================================


def new_network_signal(event):
    baseline = load_baseline()

    known_countries = json.loads(baseline["known_countries"])
    known_asns = json.loads(baseline["known_asns"])

    deviations = []

    if event["country"] not in known_countries:
        deviations.append("geographic_location_change")

    if event["asn"] not in known_asns:
        deviations.append("new_network_asn")

    if not deviations:
        return None

    confidence = 0.8 if len(deviations) == 1 else 0.95
    severity = "medium" if len(deviations) == 1 else "high"

    return {
        "entity_id": event["source_ip"],
        "entity_type": "ip",
        "signal": deviations[0],  # emit first deviation only (single event rule)
        "confidence": confidence,
        "severity": severity,
        "metadata": {
            "known_countries": known_countries,
            "known_asns": known_asns,
            "observed_country": event["country"],
            "observed_asn": event["asn"],
        },
    }


# ============================================
# 3️⃣ Abnormal Request Rate
# ============================================


def burst_signal(event):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*) FROM access_events
        WHERE timestamp >= datetime('now', '-1 hour')
    """
    )

    count = cur.fetchone()[0]
    conn.close()

    baseline = load_baseline()
    threshold = baseline["burst_threshold"]

    if threshold is None or threshold == 0:
        return None

    if count <= threshold:
        return None

    deviation_ratio = count / threshold
    confidence = min(deviation_ratio / 5.0, 1.0)

    severity = "medium"
    if deviation_ratio > 5:
        severity = "high"

    return {
        "entity_id": event["source_ip"],
        "entity_type": "ip",
        "signal": "abnormal_request_rate",
        "confidence": round(confidence, 3),
        "severity": severity,
        "metadata": {
            "baseline_threshold_per_hour": threshold,
            "current_count_last_hour": count,
            "deviation_ratio": round(deviation_ratio, 2),
        },
    }
