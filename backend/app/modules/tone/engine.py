# phema/backend/app/modules/tone/engine.py

from app.modules.module_adapter import send_event
from app.modules.tone.analyzer import analyze_text

def run_tone_analysis(user_id: str, session_id: str, text: str, entity_id: str):

    if not text or not text.strip():
        return

    result = analyze_text(text)
    risk_level = result.get("risk_level", "low")
    detected_tones = result.get("detected_tones", [])
    ml_probability = result.get("ml_probability", 0.0)

    severity_map = {
        "low": "low",
        "medium": "medium",
        "high": "high"
    }

    severity = severity_map.get(risk_level, "medium")

    if not detected_tones:
        return

    for tone in detected_tones:

        send_event(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type="session",
            module="tone",
            signal=f"tone:manipulation:{tone}",
            confidence=0.8,
            severity=severity,
            metadata={
                "ml_probability": ml_probability,
                "text_sample": text[:120]
            }
        )

    if ml_probability >= 0.75:

        send_event(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type="session",
            module="tone",
            signal="tone:ml:high_confidence",
            confidence=ml_probability,
            severity="high",
            metadata={
                "ml_probability": ml_probability
            }
        )