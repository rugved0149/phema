from app.modules.module_adapter import send_event
from app.modules.honeypot.core.risk_engine import risk_engine


def run_honeypot(
    user_id: str,
    session_id: str,
    ip: str,
    entity_id: str,
    session_context: dict,
    score_value: int = 20
):

    if not session_context:
        return

    access_type=session_context.get("access_type")

    if not access_type:
        return

    # Only suspicious probe behavior allowed

    suspicious_probe_types=[
        "probe",
        "unauthorized",
        "honeypot_access"
    ]

    if access_type not in suspicious_probe_types:
        return

    #increase score

    risk_engine.add_score(ip, score_value)
    current_score=risk_engine.get_score(ip)

    # BASE INTERACTION

    if current_score >= 30:

        send_event(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type="session",
            module="honeypot",
            signal="honeypot:interaction:access",
            confidence=0.6,
            severity="low",
            metadata={
                "ip":ip,
                "score":current_score
            }
        )

    # SHADOW BAN

    if risk_engine.is_shadow_banned(ip):

        send_event(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type="session",
            module="honeypot",
            signal="honeypot:action:shadow_ban",
            confidence=0.8,
            severity="medium",
            metadata={
                "ip":ip,
                "score":current_score
            }
        )

    # BLOCK

    if risk_engine.should_block(ip):

        send_event(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type="session",
            module="honeypot",
            signal="honeypot:action:block",
            confidence=0.95,
            severity="high",
            metadata={
                "ip":ip,
                "score":current_score
            }
        )