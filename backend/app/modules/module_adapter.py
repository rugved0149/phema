from app.correlation.schemas import CorrelationEvent
from app.core.event_bus import event_bus
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
    Standardized event emission.
    """

    payload = build_signal(
        entity_id,
        entity_type,
        module,
        signal,
        confidence,
        severity,
        metadata or {}
    )

    event = CorrelationEvent(**payload)

    event_bus.publish(event)

    return True