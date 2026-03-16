from config.scoring_weights import SCORING_WEIGHTS, CATEGORY_CAPS


def calculate_score(triggers: list) -> dict:
    """
    Calculate total phishing risk score with category-wise saturation.

    Returns:
        {
            "score": int,
            "category_breakdown": dict,
            "applied_rules": list
        }
    """

    total_score = 0
    category_scores = {}
    applied_rules = []

    for trigger in triggers:
        rule = trigger.get("rule")
        category = trigger.get("category")

        if rule not in SCORING_WEIGHTS:
            continue

        weight = SCORING_WEIGHTS[rule]

        # Initialize category if not present
        if category not in category_scores:
            category_scores[category] = 0

        # Apply category cap
        if category_scores[category] + weight > CATEGORY_CAPS.get(category, weight):
            weight = max(
                0,
                CATEGORY_CAPS.get(category, weight) - category_scores[category]
            )

        if weight <= 0:
            continue

        category_scores[category] += weight
        total_score += weight

        applied_rules.append({
            "rule": rule,
            "category": category,
            "score": weight
        })

    return {
        "score": total_score,
        "category_breakdown": category_scores,
        "applied_rules": applied_rules
    }
