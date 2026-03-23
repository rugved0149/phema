from app.modules.module_adapter import send_event
from app.modules.honeypot.core.risk_engine import risk_engine


def run_honeypot(ip: str, entity_id: str, score_value: int = 20):

    risk_engine.add_score(ip, score_value)
    current_score = risk_engine.get_score(ip)

    # -------------------------
    # BASE INTERACTION (CONTROLLED)
    # -------------------------
    # Emit only if meaningful interaction level reached
    if current_score >= 10:
        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="honeypot",
            signal="honeypot:interaction:access",
            confidence=0.6,
            severity="low",
            metadata={
                "ip": ip,
                "score": current_score
            }
        )

    # -------------------------
    # ESCALATION: SHADOW BAN
    # -------------------------
    if risk_engine.is_shadow_banned(ip):
        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="honeypot",
            signal="honeypot:action:shadow_ban",
            confidence=0.8,
            severity="medium",
            metadata={
                "ip": ip,
                "score": current_score
            }
        )

    # -------------------------
    # ESCALATION: BLOCK
    # -------------------------
    if risk_engine.should_block(ip):
        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="honeypot",
            signal="honeypot:action:block",
            confidence=0.95,
            severity="high",
            metadata={
                "ip": ip,
                "score": current_score
            }
        )