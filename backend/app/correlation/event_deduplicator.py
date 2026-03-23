from collections import defaultdict
import time


class EventDeduplicator:

    def __init__(self):

        self.cache = defaultdict(float)

        # keep your tuned value
        self.window_seconds = 1.5

        # cleanup control
        self.max_cache_size = 5000

    def cleanup(self):

        """
        Remove expired entries.
        Safe and lightweight.
        """

        now = time.time()

        expired_keys = [

            key for key, ts in self.cache.items()

            if now - ts > self.window_seconds

        ]

        for key in expired_keys:
            del self.cache[key]

    def is_duplicate(self, event):

        now = time.time()

        # 🔥 Slightly safer bucket logic
        time_bucket = int(now / self.window_seconds)

        key = (
            f"{event.entity_id}:"
            f"{event.module}:"
            f"{event.signal}:"
            f"{time_bucket}"
        )

        if key in self.cache:

            if now - self.cache[key] < self.window_seconds:
                return True

        self.cache[key] = now

        # periodic cleanup (safe)
        if len(self.cache) > self.max_cache_size:
            self.cleanup()

        return False


event_deduplicator = EventDeduplicator()