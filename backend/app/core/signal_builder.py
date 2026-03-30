from typing import Dict
from app.correlation.schemas import (
    CorrelationEvent,
    EntityType,
    ModuleName,
    SeverityLevel
)

def build_signal(
    user_id: str,
    session_id: str,
    entity_id: str,
    entity_type: str,
    module: str,
    signal: str,
    confidence: float,
    severity: str,
    metadata: Dict
):

    return CorrelationEvent(
        user_id=user_id,
        session_id=session_id,
        entity_id=entity_id,
        entity_type=EntityType(entity_type),
        module=ModuleName(module),
        signal=signal,
        confidence=confidence,
        severity=SeverityLevel(severity),
        metadata=metadata
    )