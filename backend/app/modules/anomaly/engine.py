from app.modules.anomaly.ingestion.event_ingestor import ingest_event
from datetime import datetime


def run_anomaly(entity_id: str, session_context: dict):

    payload = {
        "timestamp": session_context.get("timestamp") or datetime.utcnow().isoformat(),
        "source_ip": session_context.get("source_ip") or "0.0.0.0",
        "client_type": session_context.get("client_type") or "unknown",
        "access_type": session_context.get("access_type") or "unknown"
    }

    ingest_event(payload)