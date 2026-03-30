from app.modules.module_adapter import send_event


def run_anomaly(user_id: str, session_id: str, entity_id: str, session_context: dict):

    if not session_context:
        return

    access_type=session_context.get("access_type")

    if not access_type:
        return

    suspicious_types=[
        "multiple_failures",
        "credential_stuffing",
        "suspicious_login"
    ]

    if access_type not in suspicious_types:
        return

    send_event(
        user_id=user_id,
        session_id=session_id,
        entity_id=entity_id,
        entity_type="session",
        module="anomaly",
        signal="anomaly:behavior:deviation",
        confidence=0.7,
        severity="medium",
        metadata={
            "access_type":access_type,
            "source_ip":session_context.get("source_ip")
        }
    )