from typing import List, Dict
from datetime import datetime
import math

from app.correlation.attack_chains import ATTACK_CHAINS
from app.correlation.correlator import CorrelationContext
from app.correlation.attack_classifier import classify_attack
from app.correlation.mitre_mapper import map_to_mitre
from app.correlation.threat_memory import threat_memory
from app.correlation.campaign_detector import detect_campaign

# CATEGORY LIMITS
MAX_MODULE_SCORE = 20
MAX_SEVERITY_SCORE = 30
MAX_BEHAVIOR_SCORE = 40
MAX_REPEAT_SCORE = 15
MAX_MEMORY_SCORE = 15

# DECAY SETTINGS
DECAY_LAMBDA = 0.002
MIN_DECAY_WEIGHT = 0.2


class RiskResult:
    def __init__(
        self,
        score: int,
        level: str,
        reasons: List[str],
        attack_type: str = "unknown",
        mitre: List[dict] = None,
        breakdown: Dict = None
    ):
        self.score = score
        self.level = level
        self.reasons = reasons
        self.attack_type = attack_type
        self.mitre = mitre or []
        self.breakdown = breakdown or {}


class RiskScorer:

    def decay_weight(self, timestamp):

        try:

            now = datetime.utcnow()

            age_seconds = (
                now - timestamp
            ).total_seconds()

            weight = math.exp(
                -DECAY_LAMBDA * age_seconds
            )

            return max(
                MIN_DECAY_WEIGHT,
                weight
            )

        except Exception:

            return 1.0

    def matches_sequence(
        self,
        module_sequence,
        required_sequence
    ):
        idx = 0

        for module in module_sequence:

            if (
                idx < len(required_sequence)
                and module == required_sequence[idx]
            ):
                idx += 1

                if idx == len(required_sequence):

                    return True

        return False

    def score(self, context: CorrelationContext) -> RiskResult:

        reasons: List[str] = []

        if context.total_events == 0:

            return RiskResult(
                score=0,
                level="LOW",
                reasons=["No suspicious activity detected"]
            )

        module_score = 0
        repeat_score = 0
        severity_score = 0
        behavior_score = 0
        memory_score = 0

        # MODULE SCORE
        module_count = len(context.modules_involved)

        if module_count > 1:

            module_score = min(
                MAX_MODULE_SCORE,
                5 * module_count
            )

            reasons.append(
                f"{module_count} detection modules triggered"
            )

        # MODULE DOMINANCE
        if context.module_counts:

            dominant_module = max(
                context.module_counts,
                key=context.module_counts.get
            )

            if context.module_counts[dominant_module] > 3:

                behavior_score += 10

                reasons.append(
                    f"Repeated activity from {dominant_module}"
                )

        # DECAYED REPEAT SCORING
        weighted_repeat = 0.0

        for event in context.events:

            if event.signal in context.repeated_signals:

                weight = self.decay_weight(
                    event.timestamp
                )

                weighted_repeat += weight

        if weighted_repeat > 0:

            repeat_score = min(
                MAX_REPEAT_SCORE,
                int(weighted_repeat * 5)
            )

            reasons.append(
                f"{len(context.repeated_signals)} repeated signals detected"
            )

        # DECAYED SEVERITY SCORING
        weighted_high = 0.0

        for event in context.events:

            if event.severity.value == "high":

                weight = self.decay_weight(
                    event.timestamp
                )

                weighted_high += weight

        if weighted_high > 0:

            severity_score = min(
                MAX_SEVERITY_SCORE,
                int(weighted_high * 8)
            )

            reasons.append(
                f"{context.high_severity_events} high severity events"
            )

        # HONEYPOT (Stricter condition)
        if (
            context.honeypot_hit
            and context.high_severity_events > 0
            and len(context.repeated_signals) > 0
        ):

            behavior_score += 10

            reasons.append(
                "Confirmed honeypot escalation"
            )

        # SEQUENCE DETECTION
        module_sequence = context.module_sequence

        chain_detected = False

        for chain in ATTACK_CHAINS:

            if "sequence" in chain:

                if self.matches_sequence(
                    module_sequence,
                    chain["sequence"]
                ):

                    if not chain_detected:

                        behavior_score += 10

                        reasons.append(
                            chain["reason"]
                        )

                        chain_detected = True

        # CAMPAIGN DETECTION
        campaigns_detected = False

        for module, count in context.module_counts.items():

            if count >= 3:

                campaigns_detected = True

                reasons.append(
                    f"Repeated {module} activity detected ({count} times)"
                )

        if campaigns_detected:

            behavior_score += 15

            reasons.append(
                "Campaign behavior detected"
            )

        behavior_score = min(
            behavior_score,
            MAX_BEHAVIOR_SCORE
        )

        # THREAT MEMORY
        history = threat_memory.get_entity_activity(
            context.entity_id
        )

        activity = history["total_events"]

        if activity >= 5:

            memory_score = min(
                MAX_MEMORY_SCORE,
                activity // 2
            )

            reasons.append(
                "Persistent suspicious behavior detected"
            )

        # FINAL SCORE
        score = (
            module_score
            + repeat_score
            + severity_score
            + behavior_score
            + memory_score
        )

        score = min(score, 100)

        # RISK LEVEL
        if score >= 75:

            level = "HIGH"

        elif score >= 40:

            level = "MEDIUM"

        else:

            level = "LOW"

        # CLASSIFICATION
        attack = classify_attack(
            context.modules_involved,
            context.signals
        )

        # MITRE
        mitre = map_to_mitre(
            context.modules_involved,
            context.signals,
            attack_type=attack["attack_type"]
        )

        reasons.append(
            f"Attack classification: {attack['attack_type']}"
        )

        # BREAKDOWN
        breakdown = {
            "module_score": module_score,
            "repeat_score": repeat_score,
            "severity_score": severity_score,
            "behavior_score": behavior_score,
            "memory_score": memory_score
        }

        return RiskResult(
            score=score,
            level=level,
            reasons=reasons,
            attack_type=attack["attack_type"],
            mitre=mitre,
            breakdown=breakdown
        )