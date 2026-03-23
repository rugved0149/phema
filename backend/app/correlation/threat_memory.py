# app/correlation/threat_memory.py

from collections import defaultdict
from typing import Dict
from datetime import datetime, timedelta


class ThreatMemory:

    def __init__(self):

        self.entity_activity = defaultdict(int)
        self.module_history = defaultdict(set)
        self.signal_history = defaultdict(list)

        self.last_seen = {}

        self.decay_seconds = 3600
        self.max_signal_history = 50


    def record_event(self, event):

        entity = event.entity_id

        self.entity_activity[entity] += 1

        self.module_history[entity].add(
            event.module.value
        )

        signals = self.signal_history[entity]

        signals.append(event.signal)

        if len(signals) > self.max_signal_history:
            del signals[0]

        self.last_seen[entity] = datetime.utcnow()


    def apply_decay(self):

        now = datetime.utcnow()

        for entity in list(self.entity_activity.keys()):

            last_time = self.last_seen.get(entity)

            if not last_time:
                continue

            delta = (
                now - last_time
            ).total_seconds()

            if delta > self.decay_seconds:

                self.entity_activity[entity] *= 0.5

                if self.entity_activity[entity] < 1:
                    self._remove_entity(entity)


    def _remove_entity(self, entity):

        self.entity_activity.pop(entity, None)
        self.module_history.pop(entity, None)
        self.signal_history.pop(entity, None)
        self.last_seen.pop(entity, None)


    def get_entity_activity(
        self,
        entity_id
    ) -> Dict:

        return {

            "total_events":
                int(self.entity_activity.get(entity_id, 0)),

            "modules":
                list(self.module_history.get(entity_id, [])),

            "signals":
                self.signal_history.get(entity_id, []),

            "last_seen":
                self.last_seen.get(entity_id)

        }


    def cleanup_inactive(
        self,
        inactive_minutes: int = 1440
    ):

        cutoff = datetime.utcnow() - timedelta(
            minutes=inactive_minutes
        )

        for entity in list(self.last_seen.keys()):

            if self.last_seen[entity] < cutoff:
                self._remove_entity(entity)

# singleton instance
threat_memory = ThreatMemory()