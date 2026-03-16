from app.modules.module_adapter import send_event
from app.modules.honeypot.core.risk_engine import risk_engine


def run_honeypot(ip: str, entity_id: str, score_value: int = 20):

    risk_engine.add_score(ip, score_value)
    current_score = risk_engine.get_score(ip)

    if risk_engine.is_shadow_banned(ip):
        send_event(
            entity_id=ip,  # ✅ FIXED
            entity_type="ip",
            module="honeypot",
            signal="shadow_ban_triggered",
            confidence=0.8,
            severity="medium",
            metadata={
                "ip": ip,
                "score": current_score
            }
        )

    if risk_engine.should_block(ip):
        send_event(
            entity_id=ip,  # ✅ FIXED
            entity_type="ip",
            module="honeypot",
            signal="ip_blocked",
            confidence=0.95,
            severity="high",
            metadata={
                "ip": ip,
                "score": current_score
            }
        )
