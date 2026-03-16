from app.modules.module_adapter import send_event
from app.modules.phishing.core.analyzer import analyze
from app.modules.phishing.core.parser import parse_url


def run_phishing(url: str, entity_id: str):
    """
    Entry point for PHEMA to run phishing detection.
    """

    parsed = parse_url(url)
    triggers = analyze(parsed)

    for trigger in triggers:

        rule_name = trigger.get("rule")
        category = trigger.get("category")

        severity_map = {
            "structural": "medium",
            "hosting": "medium",
            "keyword": "medium",
            "brand": "high",
            "obfuscation": "high"
        }

        severity = severity_map.get(category, "medium")
        confidence = 0.7 if severity == "medium" else 0.85

        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="phishing",
            signal=rule_name,
            confidence=confidence,
            severity=severity,
            metadata={
                "category": category,
                "url": url
            }
        )
