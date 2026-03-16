# app/correlation/explanation_engine.py

from typing import Dict
from app.correlation.correlator import CorrelationContext


MODULE_DESCRIPTIONS = {
    "phishing": "Suspicious or deceptive URL patterns detected",
    "tone": "Manipulative language or social engineering tactics detected",
    "file_checker": "Potentially malicious file indicators detected",
    "honeypot": "Interaction with restricted or trap resources detected",
    "anomaly": "Behavior deviates from normal usage patterns"
}


SIGNAL_DESCRIPTIONS = {
    "brand_impersonation": "Domain mimics a known brand",
    "urgency": "Message contains urgency manipulation",
    "credential_harvest": "Attempt to collect sensitive authentication data",
    "payload_delivery": "Suspicious file payload detected"
}


def generate_explanation(context: CorrelationContext) -> Dict:

    explanation = {
        "modules_triggered": [],
        "signals_detected": [],
        "analysis": []
    }

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
                explanation["analysis"].append(SIGNAL_DESCRIPTIONS[key])

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

    return explanation