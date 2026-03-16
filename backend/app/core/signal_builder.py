from typing import Dict


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

    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "module": module,
        "signal": signal,
        "confidence": confidence,
        "severity": severity,
        "metadata": metadata
    }