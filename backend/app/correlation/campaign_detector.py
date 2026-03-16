from collections import Counter


def detect_campaign(events):

    signals = [e.signal for e in events]

    counter = Counter(signals)

    campaigns = []

    for signal, count in counter.items():

        if count >= 5:

            campaigns.append({
                "signal": signal,
                "count": count,
                "type": "campaign_activity"
            })

    return campaigns