from app.modules.module_adapter import send_event
from app.modules.tone.analyzer import analyze_text


def run_tone_analysis(text: str, entity_id: str):

    result = analyze_text(text)

    risk_level = result.get("risk_level")
    detected_tones = result.get("detected_tones", [])
    ml_probability = result.get("ml_probability")

    severity_map = {
        "low": "low",
        "medium": "medium",
        "high": "high"
    }

    severity = severity_map.get(risk_level, "medium")

    for tone in detected_tones:

        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="tone",
            signal=f"tone:{tone}",
            confidence=0.8,
            severity=severity,
            metadata={
                "ml_probability": ml_probability,
                "text_sample": text[:120]
            }
        )