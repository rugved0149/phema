from typing import Dict
from app.correlation.schemas import CorrelationEvent, EntityType, ModuleName, SeverityLevel

def build_signal(
    entity_id: str,
    entity_type: str,
    module: str,
    signal: str,
    confidence: float,
    severity: str,
    metadata: Dict
):
    """
    Standardizes signals emitted by modules.
    """

    return CorrelationEvent(
        entity_id=entity_id,
        entity_type=EntityType(entity_type),
        module=ModuleName(module),
        signal=signal,
        confidence=confidence,
        severity=SeverityLevel(severity),
        metadata=metadata
    )