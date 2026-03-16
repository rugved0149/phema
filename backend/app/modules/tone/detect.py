import json
import os
from collections import defaultdict
from typing import Dict


def load_signals() -> Dict:
    """
    Load signal definitions from signals.json
    """
    base_dir = os.path.dirname(__file__)
    signals_path = os.path.join(base_dir, "signals", "signals.json")

    with open(signals_path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_signals(text: str) -> Dict[str, int]:
    """
    Detect signal categories present in the given normalized text.

    Returns:
        dict: {signal_category: count}
    """
    signals = load_signals()
    detected = defaultdict(int)

    if not text:
        return {}

    for category, config in signals.items():
        phrases = config.get("phrases", [])

        for phrase in phrases:
            if phrase in text:
                detected[category] = 1
                break

    return dict(detected)
