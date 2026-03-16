# app/correlation/timeline_builder.py

from typing import List, Dict
from app.correlation.schemas import CorrelationEvent


def build_timeline(events: List[CorrelationEvent]) -> List[Dict]:
    """
    Convert correlation events into a chronological timeline.
    """

    if not events:
        return []

    # Sort events chronologically
    events_sorted = sorted(events, key=lambda e: e.timestamp)

    timeline = []

    for event in events_sorted:
        timeline.append({
            "time": event.timestamp.strftime("%H:%M:%S"),
            "module": event.module.value,
            "signal": event.signal,
            "severity": event.severity.value
        })

    return timeline