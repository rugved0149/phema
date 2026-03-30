# app/correlation/correlator.py

from collections import Counter
from typing import List, Set

from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.schemas import CorrelationEvent, EntityType


class CorrelationContext:

    def __init__(
        self,
        entity_id: str,
        session_id: str,
        events: List[CorrelationEvent],
        total_events: int,
        modules_involved: Set[str],
        signals: List[str],
        repeated_signals: Set[str],
        honeypot_hit: bool,
        high_severity_events: int,
        ordered_events: List[CorrelationEvent],
        module_sequence: List[str],
        signal_flow: List[tuple],
        module_counts: Counter,
        signal_counts: Counter,
        time_deltas: List[float]
    ):
        self.entity_id = entity_id
        self.session_id = session_id
        self.events = events
        self.total_events = total_events
        self.modules_involved = modules_involved
        self.signals = signals
        self.repeated_signals = repeated_signals
        self.honeypot_hit = honeypot_hit
        self.high_severity_events = high_severity_events
        self.ordered_events = ordered_events
        self.module_sequence = module_sequence
        self.signal_flow = signal_flow
        self.module_counts = module_counts
        self.signal_counts = signal_counts
        self.time_deltas = time_deltas


class Correlator:

    def __init__(self, event_store: SQLiteEventStore):
        self.event_store = event_store

    def build_context(
        self,
        user_id: str,
        session_id: str,
        entity_type: EntityType,
        entity_id: str,
        window_minutes: int
    ) -> CorrelationContext:

        events: List[CorrelationEvent] = self.event_store.get_events(
            user_id=user_id,
            session_id=session_id,
            entity_type=entity_type,
            entity_id=entity_id,
            window_minutes=window_minutes
        )

        from app.core.logger import logger

        logger.info(
            f"[CORRELATOR] User {user_id} | Session {session_id} | {len(events)} events"
        )

        if not events:

            return CorrelationContext(
                entity_id=entity_id,
                session_id=session_id,
                events=[],
                total_events=0,
                modules_involved=set(),
                signals=[],
                repeated_signals=set(),
                honeypot_hit=False,
                high_severity_events=0,
                ordered_events=[],
                module_sequence=[],
                signal_flow=[],
                module_counts=Counter(),
                signal_counts=Counter(),
                time_deltas=[]
            )

        events_sorted = sorted(
            events,
            key=lambda e: e.timestamp
        )

        module_sequence = [
            event.module.value
            for event in events_sorted
        ]

        signal_list = [
            event.signal
            for event in events_sorted
        ]

        module_counts = Counter(module_sequence)
        signal_counts = Counter(signal_list)

        repeated_signals = {
            signal
            for signal, count in signal_counts.items()
            if count > 1
        }

        modules = set(module_sequence)

        honeypot_hit = (
            "honeypot"
            in module_sequence
        )

        high_severity_events = sum(
            1
            for event in events_sorted
            if event.severity.value == "high"
        )

        signal_flow = []
        time_deltas = []

        for i in range(len(events_sorted) - 1):

            current = events_sorted[i]
            nxt = events_sorted[i + 1]

            signal_flow.append(
                (current.signal, nxt.signal)
            )

            delta = (
                nxt.timestamp
                - current.timestamp
            ).total_seconds()

            time_deltas.append(delta)

        return CorrelationContext(
            entity_id=entity_id,
            session_id=session_id,
            events=events_sorted,
            total_events=len(events_sorted),
            modules_involved=modules,
            signals=signal_list,
            repeated_signals=repeated_signals,
            honeypot_hit=honeypot_hit,
            high_severity_events=high_severity_events,
            ordered_events=events_sorted,
            module_sequence=module_sequence,
            signal_flow=signal_flow,
            module_counts=module_counts,
            signal_counts=signal_counts,
            time_deltas=time_deltas
        )