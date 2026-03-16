"""
PHEMA Event Adapter
Converts raw file analysis into standardized backend events.
"""

from app.modules.file_checker.scanner.hash_db import check_hash


def build_event(entity_id, signal, confidence, severity, metadata):
    return {
        "entity_id": entity_id,
        "entity_type": "file",
        "module": "file_checker",
        "signal": signal,
        "confidence": float(confidence),
        "severity": severity,
        "metadata": metadata
    }


def convert_analysis_to_events(raw_result):

    events = []
    entity_id = raw_result["hash"]

    # 1️⃣ Known malicious hash
    hash_match = check_hash(entity_id)
    if hash_match:
        events.append(
            build_event(
                entity_id,
                signal="known_malicious_hash",
                confidence=1.0,
                severity="high",
                metadata={
                    "hash": entity_id,
                    "source": "local_hash_db",
                    "family": hash_match
                }
            )
        )

    # 2️⃣ YARA matches
    for match in raw_result.get("yara_hits", []):
        events.append(
            build_event(
                entity_id,
                signal=f"yara_match:{match['rule']}",
                confidence=0.95,
                severity=match.get("severity", "medium"),
                metadata=match
            )
        )

    # 3️⃣ High entropy detection
    entropy = raw_result.get("entropy", 0)
    if entropy > 7.5:
        events.append(
            build_event(
                entity_id,
                signal="high_entropy_detected",
                confidence=0.7,
                severity="medium",
                metadata={
                    "entropy": entropy,
                    "threshold": 7.5
                }
            )
        )

    # 4️⃣ Suspicious string detections
    for s in raw_result.get("suspicious_strings", []):
        events.append(
            build_event(
                entity_id,
                signal="suspicious_string_detected",
                confidence=0.6,
                severity="medium",
                metadata={"string": s}
            )
        )

    return events
