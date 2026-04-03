from app.correlation.schemas import CorrelationEvent
from app.core.event_emitter import emit_event
from app.core.signal_builder import build_signal
from app.core.logger import logger

def send_event(
    *,
    user_id: str,
    session_id: str,
    entity_id: str,
    entity_type: str,
    module: str,
    signal: str,
    confidence: float,
    severity: str,
    metadata=None
):

    if not signal:
        print("SEND_EVENT BLOCKED: empty signal")
        return

    if metadata is None:
        metadata = {}

    try:

        payload = build_signal(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type=entity_type,
            module=module,
            signal=signal,
            confidence=confidence,
            severity=severity,
            metadata=metadata
        )

        if isinstance(payload, CorrelationEvent):
            event = payload
        else:
            event = CorrelationEvent(**payload)

        emit_event(event)

    except Exception as e:

        logger.error(
            f"[MODULE ADAPTER ERROR] {e}"
        )

        logger.error(
            f"[MODULE ADAPTER ERROR] {e}"
        )