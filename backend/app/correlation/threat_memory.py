# app/correlation/threat_memory.py

from collections import defaultdict
from typing import Dict


class ThreatMemory:

    def __init__(self):

        # entity_id → event count
        self.entity_activity = defaultdict(int)

        # entity_id → modules triggered
        self.module_history = defaultdict(set)

        # entity_id → signals seen
        self.signal_history = defaultdict(list)

    def record_event(self, event):

        entity = event.entity_id

        self.entity_activity[entity] += 1
        self.module_history[entity].add(event.module.value)
        self.signal_history[entity].append(event.signal)

    def get_entity_activity(self, entity_id):

        return {
            "total_events": self.entity_activity.get(entity_id, 0),
            "modules": list(self.module_history.get(entity_id, [])),
            "signals": self.signal_history.get(entity_id, [])
        }


# singleton instance
threat_memory = ThreatMemory()