# app/correlation/attack_replay.py

from typing import List, Dict
from app.correlation.schemas import CorrelationEvent


def build_attack_replay(events: List[CorrelationEvent]) -> List[Dict]:
    """
    Convert raw events into a chronological replay timeline.
    """

    timeline = []

    # sort events by timestamp
    events_sorted = sorted(events, key=lambda e: e.timestamp)

    for event in events_sorted:

        timeline.append({
            "time": event.timestamp,
            "module": event.module.value,
            "signal": event.signal,
            "severity": event.severity.value,
            "confidence": event.confidence
        })

    return timeline