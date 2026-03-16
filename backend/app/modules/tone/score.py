import json
import os
from typing import Dict, Tuple


def load_signal_weights() -> Dict[str, int]:
    base_dir = os.path.dirname(__file__)
    signals_path = os.path.join(base_dir, "signals", "signals.json")
    
    with open(signals_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {category: config.get("weight", 1) for category, config in data.items()}


def calculate_risk(signals: Dict[str, int]) -> Tuple[int, str]:
    if not signals:
        return 0, "low"

    weights = load_signal_weights()
    risk_score = 0

    for category, count in signals.items():
        weight = weights.get(category, 1)
        risk_score += weight * count

    # HARD CAP SCORE AT 10
    risk_score = min(risk_score, 10)

    if risk_score >= 7:
        risk_level = "high"
    elif risk_score >= 4:
        risk_level = "medium"
    else:
        risk_level = "low"

    return risk_score, risk_level
