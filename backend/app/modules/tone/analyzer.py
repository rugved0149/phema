from app.modules.tone.normalize import normalize_text
from app.modules.tone.detect import detect_signals
from app.modules.tone.score import calculate_risk
from app.modules.tone.explain import generate_explanation
from app.modules.tone.ml_assist import get_ml_probability

def analyze_text(text: str) -> dict:
    # Normalize input
    normalized_text = normalize_text(text)

    # Rule-based detection
    signals = detect_signals(normalized_text)
    risk_score, risk_level = calculate_risk(signals)

    # Explanation
    explanation = generate_explanation(signals)

    # ML probability
    ml_probability = get_ml_probability(normalized_text)

    #  ML CONFIRMATION LOGIC (SAFE & BOUNDED)
    if risk_level == "medium" and ml_probability >= 0.5:
        risk_score = min(risk_score + 1, 10)
        risk_level = "high"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "detected_tones": list(signals.keys()),
        "signals": signals,
        "explanation": explanation,
        "ml_probability": round(ml_probability, 3),
    }
