# app/core/event_emitter.py

from app.core.logger import logger
from app.core.dependencies import event_store
from app.correlation.threat_memory import threat_memory
from app.correlation.event_deduplicator import event_deduplicator


def emit_event(event):

    try:

        # Deduplication
        if event_deduplicator.is_duplicate(event):
            return

        # Log only meaningful events
        if event.severity.value in ("medium", "high"):

            logger.info(
                f"[EMIT] {event.module.value}:{event.signal}"
            )

        # Store event
        event_store.add_event(event)

        # Record memory
        threat_memory.record_event(event)

    except Exception as e:

        logger.error(
            f"[PIPELINE ERROR] {e}"
        )