import json
import os
from typing import Dict, List


def load_explanations() -> Dict[str, str]:
    """
    Load explanation text for each signal category from signals.json
    """
    base_dir = os.path.dirname(__file__)
    signals_path = os.path.join(base_dir, "signals", "signals.json")

    with open(signals_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        category: config.get("explanation", "") for category, config in data.items()
    }


def generate_explanation(signals: Dict[str, int]) -> List[str]:
    if not signals:
        return ["No significant manipulation patterns detected"]

    explanations = load_explanations()
    result = []

    for category in signals:
        text = explanations.get(category)
        if text:
            result.append(text)

    return result
