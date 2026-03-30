from fastapi import APIRouter

from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.correlator import Correlator
from app.correlation.risk_scoring import RiskScorer


router=APIRouter(prefix="/advice")

event_store=SQLiteEventStore()

correlator=Correlator(
    event_store=event_store
)

scorer=RiskScorer()

@router.get("/{user_id}/{session_id}")

def get_advice(
    user_id:str,
    session_id:str
):

    context=correlator.build_context(

        user_id=user_id,
        session_id=session_id,
        entity_type="session",
        entity_id=session_id,
        window_minutes=60

    )

    result=scorer.score(context)

    advice=[]

    if result.level=="LOW":

        advice.append(
            "No major threats detected"
        )

    elif result.level=="MEDIUM":

        advice.append(
            "Review recent activity carefully"
        )

        advice.append(
            "Avoid interacting with suspicious links"
        )

    elif result.level=="HIGH":

        advice.append(
            "Terminate session immediately"
        )

        advice.append(
            "Reset credentials"
        )

        advice.append(
            "Run full malware scan"
        )

    return {

        "risk_level":result.level,

        "attack_type":result.attack_type,

        "advice":advice

    }