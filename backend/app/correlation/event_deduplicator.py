from collections import defaultdict
import time

class EventDeduplicator:

    def __init__(self):

        self.cache = defaultdict(float)
        self.window_seconds = 10

    def is_duplicate(self, event):

        key = f"{event.entity_id}:{event.module}:{event.signal}"

        now = time.time()

        if key in self.cache:

            if now - self.cache[key] < self.window_seconds:
                return True

        self.cache[key] = now

        return False


event_deduplicator = EventDeduplicator()