# phema/backend/app/modules/phishing/engine.py

from app.modules.module_adapter import send_event
from app.modules.phishing.core.analyzer import analyze
from app.modules.phishing.core.parser import parse_url

def run_phishing(user_id: str, session_id: str, url: str, entity_id: str):

    parsed = parse_url(url)
    triggers = analyze(parsed)

    if not triggers:
        return

    severity_map = {
        "structural": "medium",
        "hosting": "medium",
        "keyword": "medium",
        "brand": "high",
        "obfuscation": "high"
    }

    for trigger in triggers:

        rule_name = trigger.get("rule", "unknown_rule")
        category = trigger.get("category", "unknown")
        severity = severity_map.get(category, "medium")
        confidence = 0.7 if severity == "medium" else 0.85
        signal = f"phishing:{category}:{rule_name}"
        send_event(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type="session",
            module="phishing",
            signal=signal,
            confidence=confidence,
            severity=severity,
            metadata={
                "category": category,
                "rule": rule_name,
                "url": url
            }
        )