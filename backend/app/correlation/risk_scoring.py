# app/correlation/risk_scoring.py

from typing import List
from app.correlation.attack_chains import ATTACK_CHAINS
from app.correlation.correlator import CorrelationContext
from app.correlation.attack_classifier import classify_attack
from app.correlation.mitre_mapper import map_to_mitre
from app.correlation.threat_memory import threat_memory
from app.correlation.campaign_detector import detect_campaign

class RiskResult:

    def __init__(
        self,
        score,
        level,
        reasons,
        attack_type="unknown",
        mitre=None
    ):
        self.score = score
        self.level = level
        self.reasons = reasons
        self.attack_type = attack_type
        self.mitre = mitre or []

class RiskScorer:

    def score(self, context: CorrelationContext) -> RiskResult:

        score = 0
        reasons: List[str] = []

        if context.total_events == 0:
            return RiskResult(
                score=0,
                level="LOW",
                reasons=["No suspicious activity detected"]
            )

        # Multiple modules involved
        if len(context.modules_involved) > 1:
            bonus = 10 * (len(context.modules_involved) - 1)
            score += bonus
            reasons.append(
                f"Multiple detection modules involved ({len(context.modules_involved)})"
            )

        # Repeated signals
        if context.repeated_signals:
            score += 15
            reasons.append(
                f"Repeated signals detected: {', '.join(context.repeated_signals)}"
            )

        # Honeypot interaction
        if context.honeypot_hit:
            score += 40
            reasons.append("Interaction with honeypot resource detected")

        # High severity events
        if context.high_severity_events > 0:
            increment = min(context.high_severity_events * 10, 30)
            score += increment
            reasons.append(
                f"{context.high_severity_events} high-severity event(s) detected"
            )

        # -------------------------
        # ATTACK CHAIN DETECTION
        # -------------------------

        for chain in ATTACK_CHAINS:

            # module-based chain
            if "modules" in chain:
                if chain["modules"].issubset(context.modules_involved):
                    score += chain["score_bonus"]
                    reasons.append(chain["reason"])

            # signal-based chain
            if "signals" in chain:
                if chain["signals"].intersection(set(context.signals)):
                    score += chain["score_bonus"]
                    reasons.append(chain["reason"])

        score = min(score, 100)

        mitre = map_to_mitre(
            context.modules_involved,
            context.signals
        )

        if score >= 70:
            level = "HIGH"
        elif score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        attack = classify_attack(
            context.modules_involved,
            context.signals
        )
        
        campaigns = detect_campaign(context.events)

        if campaigns:
            score += 20
            reasons.append("Attack campaign activity detected")
            
        # persistent attacker detection
        history = threat_memory.get_entity_activity(context.signals[0] if context.signals else "")

        if history["total_events"] > 5:
            score += 15
            reasons.append("Persistent suspicious activity detected")

        reasons.append(f"Attack classification: {attack['attack_type']}")

        return RiskResult(
            score=score,
            level=level,
            reasons=reasons,
            attack_type=attack["attack_type"],
            mitre=mitre
        )