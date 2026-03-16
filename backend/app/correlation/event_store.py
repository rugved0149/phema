# app/correlation/event_store.py

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from app.correlation.schemas import CorrelationEvent, EntityType


class EventStore:
    """
    In-memory event store for correlation.
    Responsible ONLY for storing and retrieving events.
    """

    def __init__(self):
        # Key: (entity_type, entity_id)
        self._events: Dict[Tuple[EntityType, str], List[CorrelationEvent]] = defaultdict(list)

    # -------------------------
    # WRITE
    # -------------------------

    def add_event(self, event: CorrelationEvent) -> None:
        key = (event.entity_type, event.entity_id)
        self._events[key].append(event)

    # -------------------------
    # READ
    # -------------------------

    def get_events(
        self,
        entity_type: EntityType,
        entity_id: str,
        window_minutes: int
    ) -> List[CorrelationEvent]:
        """
        Retrieve events for an entity within a time window.
        """
        key = (entity_type, entity_id)
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)

        return [
            event for event in self._events.get(key, [])
            if event.timestamp >= window_start
        ]

    # -------------------------
    # CLEANUP (OPTIONAL)
    # -------------------------

    def purge_old_events(self, max_age_minutes: int = 1440) -> None:
        """
        Remove events older than max_age_minutes (default: 24 hours).
        """
        cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)

        for key in list(self._events.keys()):
            self._events[key] = [
                event for event in self._events[key]
                if event.timestamp >= cutoff
            ]

            if not self._events[key]:
                del self._events[key]
