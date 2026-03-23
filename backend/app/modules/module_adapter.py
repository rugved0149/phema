# app/modules/module_adapter.py

from app.correlation.schemas import CorrelationEvent
from app.core.event_emitter import emit_event
from app.core.signal_builder import build_signal


def send_event(
    *,
    entity_id: str,
    entity_type: str,
    module: str,
    signal: str,
    confidence: float,
    severity: str,
    metadata=None
):
    """
    Standardized event emission reference point.
    Handles both dict and object returns safely.
    """

    if not signal:
        return

    if metadata is None:
        metadata = {}

    try:

        payload = build_signal(
            entity_id,
            entity_type,
            module,
            signal,
            confidence,
            severity,
            metadata
        )

        # 🔥 FIX: handle both dict and object safely

        if isinstance(payload, CorrelationEvent):

            event = payload

        else:

            event = CorrelationEvent(**payload)

        emit_event(event)

    except Exception as e:

        from app.core.logger import logger

        logger.error(
            f"[MODULE ADAPTER ERROR] {e}"
        )