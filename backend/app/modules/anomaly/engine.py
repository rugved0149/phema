from app.modules.module_adapter import send_event
from datetime import datetime


def run_anomaly(entity_id: str, session_context: dict):

    payload = {
        "timestamp": session_context.get("timestamp") or datetime.utcnow().isoformat(),
        "source_ip": session_context.get("source_ip") or "0.0.0.0",
        "client_type": session_context.get("client_type") or "unknown",
        "access_type": session_context.get("access_type") or "unknown"
    }

    send_event(
        entity_id=entity_id,
        entity_type="session",
        module="anomaly",
        signal="anomaly:behavior:deviation", 
        confidence=0.7,
        severity="medium",
        metadata=payload                     
    )