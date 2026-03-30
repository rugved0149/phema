# app/correlation/explanation_engine.py

from typing import Dict, List
from collections import Counter
from app.correlation.correlator import CorrelationContext


MODULE_DESCRIPTIONS = {
    "phishing": "Suspicious or deceptive URL patterns detected",
    "tone": "Manipulative language or social engineering tactics detected",
    "file_checker": "Potentially malicious file indicators detected",
    "honeypot": "Interaction with restricted or trap resources detected",
    "anomaly": "Behavior deviates from normal usage patterns"
}


SIGNAL_DESCRIPTIONS = {
    "brand": "Domain behavior resembles impersonation patterns",
    "typosquatted": "Domain structure suggests typo-based deception",
    "urgency": "Message contains urgency manipulation",
    "credential": "Attempt to collect sensitive authentication data",
    "payload": "Suspicious payload-related activity detected",
    "yara_match": "File matched known malware detection rule",
    "high_entropy": "File characteristics indicate possible obfuscation",
    "multiple_suspicious_strings": "Multiple suspicious code indicators detected"
}


SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 2,
    "high": 3
}


def _count_module_frequency(events) -> Dict[str, int]:

    counter = Counter()

    for event in events:
        module = getattr(event, "module", None)
        if module:
            counter[module] += 1

    return dict(counter)


def _count_severity(events) -> Dict[str, int]:

    counter = Counter()

    for event in events:
        severity = getattr(event, "severity", "low")
        counter[severity] += 1

    return dict(counter)


def _detect_dominant_module(module_counts: Dict[str, int]) -> str:

    if not module_counts:
        return None

    dominant = max(module_counts, key=module_counts.get)

    if module_counts[dominant] > 1:
        return dominant

    return None


def generate_explanation(context: CorrelationContext) -> Dict:

    explanation = {
        "modules_triggered": [],
        "signals_detected": [],
        "analysis": [],
        "module_frequency": {},
        "severity_distribution": {},
        "dominant_module": None
    }

    events = getattr(context, "events", [])

    # Modules explanation
    for module in context.modules_involved:

        explanation["modules_triggered"].append(module)

        description = MODULE_DESCRIPTIONS.get(module)

        if description:
            explanation["analysis"].append(description)

    # Signals explanation
    for signal in context.signals:

        explanation["signals_detected"].append(signal)

        for key in SIGNAL_DESCRIPTIONS:

            if key in signal:
                explanation["analysis"].append(
                    SIGNAL_DESCRIPTIONS[key]
                )

    # Module frequency analysis
    module_counts = _count_module_frequency(events)

    if module_counts:
        explanation["module_frequency"] = module_counts

    # Severity distribution
    severity_counts = _count_severity(events)

    if severity_counts:
        explanation["severity_distribution"] = severity_counts

        if severity_counts.get("high", 0) >= 2:
            explanation["analysis"].append(
                "Multiple high-severity events detected"
            )

    # Dominant module detection
    dominant = _detect_dominant_module(module_counts)

    if dominant:

        explanation["dominant_module"] = dominant

        description = MODULE_DESCRIPTIONS.get(dominant)

        if description:
            explanation["analysis"].append(
                f"Primary activity concentrated in {dominant} module"
            )

    # Honeypot specific explanation
    if context.honeypot_hit:

        explanation["analysis"].append(
            "Entity interacted with honeypot trap resource"
        )

    # Repeated signals explanation
    if context.repeated_signals:

        explanation["analysis"].append(
            "Repeated suspicious signals detected across modules"
        )

    # Multi-module correlation reasoning
    if len(context.modules_involved) >= 2:

        explanation["analysis"].append(
            "Multiple detection modules triggered within the same session"
        )

    # High-risk correlation reasoning
    if severity_counts.get("high", 0) >= 3:

        explanation["analysis"].append(
            "Cluster of high-severity events suggests coordinated threat activity"
        )

    return explanation