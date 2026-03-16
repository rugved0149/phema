# app/correlation/correlator.py

from collections import Counter
from typing import Dict, List, Set

from app.correlation.event_store import EventStore
from app.correlation.schemas import CorrelationEvent, EntityType

class CorrelationContext:

    def __init__(
        self,
        total_events,
        modules_involved,
        signals,
        repeated_signals,
        honeypot_hit,
        high_severity_events,
        events
    ):
        self.total_events = total_events
        self.modules_involved = modules_involved
        self.signals = signals
        self.repeated_signals = repeated_signals
        self.honeypot_hit = honeypot_hit
        self.high_severity_events = high_severity_events
        self.events = events

class Correlator:
    """
    Aggregates events into a correlation context.
    """

    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def build_context(
        self,
        entity_type: EntityType,
        entity_id: str,
        window_minutes: int
    ) -> CorrelationContext:
        events: List[CorrelationEvent] = self.event_store.get_events(
            entity_type=entity_type,
            entity_id=entity_id,
            window_minutes=window_minutes
        )

        if not events:
            return CorrelationContext(
                total_events=0,
                modules_involved=set(),
                signals=[],
                repeated_signals=set(),
                honeypot_hit=False,
                high_severity_events=0,
                events=[]
            )

        modules = {event.module.value for event in events}
        signal_list = [event.signal for event in events]
        signal_counts = Counter(signal_list)

        repeated_signals = {
            signal for signal, count in signal_counts.items()
            if count > 1
        }

        honeypot_hit = any(
            event.module.value == "honeypot"
            for event in events
        )

        high_severity_events = sum(
            1 for event in events
            if event.severity.value == "high"
        )

        return CorrelationContext(
            total_events=len(events),
            modules_involved=modules,
            signals=signal_list,
            repeated_signals=repeated_signals,
            honeypot_hit=honeypot_hit,
            high_severity_events=high_severity_events,
            events=events
        )