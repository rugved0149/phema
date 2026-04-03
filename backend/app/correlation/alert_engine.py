from typing import List,Dict
from datetime import datetime

from app.correlation.correlator import CorrelationContext
from app.correlation.risk_scoring import RiskResult


ALERT_HIGH_RISK_THRESHOLD=70
ALERT_RAPID_RISE_THRESHOLD=20
ALERT_MULTI_HIGH_EVENTS=3


def generate_alerts(
    context:CorrelationContext,
    risk:RiskResult,
    previous_score:int,
    peak_score:int
)->List[Dict]:

    alerts=[]

    current_score=risk.score

    # HIGH RISK ALERT
    if current_score>=ALERT_HIGH_RISK_THRESHOLD:

        alerts.append({
            "type":"HIGH_RISK_REACHED",
            "message":"High risk threshold reached",
            "timestamp":datetime.utcnow()
        })

    # RAPID RISE ALERT
    if previous_score is not None:

        delta=current_score-previous_score

        if delta>=ALERT_RAPID_RISE_THRESHOLD:

            alerts.append({
                "type":"RISK_RAPID_RISE",
                "message":"Risk increased rapidly",
                "timestamp":datetime.utcnow()
            })

    # MULTIPLE HIGH SEVERITY EVENTS
    if context.high_severity_events>=ALERT_MULTI_HIGH_EVENTS:

        alerts.append({
            "type":"MULTIPLE_HIGH_SEVERITY",
            "message":"Multiple high severity events detected",
            "timestamp":datetime.utcnow()
        })

    # HONEYPOT ALERT
    if context.honeypot_hit:

        alerts.append({
            "type":"HONEYPOT_TRIGGERED",
            "message":"Honeypot interaction detected",
            "timestamp":datetime.utcnow()
        })

    # CAMPAIGN ALERT
    for module,count in context.module_counts.items():

        if count>=3:

            alerts.append({
                "type":"CAMPAIGN_DETECTED",
                "message":f"Repeated {module} activity detected",
                "timestamp":datetime.utcnow()
            })

            break

    # PEAK RISK ALERT
    if current_score>peak_score:

        alerts.append({
            "type":"PEAK_RISK_UPDATED",
            "message":"New peak risk detected",
            "timestamp":datetime.utcnow()
        })

    return alerts