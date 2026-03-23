from collections import Counter


def detect_campaign(events):
    """
    Detect repeated behavior patterns.
    Uses module repetition instead of signal repetition.
    """

    if not events:
        return []

    # 🔥 FIX: use modules instead of signals
    modules = [e.module.value for e in events]

    counter = Counter(modules)

    campaigns = []

    for module, count in counter.items():

        # Lower realistic threshold
        if count >= 3:

            campaigns.append({
                "module": module,
                "count": count,
                "type": "campaign_activity"
            })

    return campaigns