from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.db.base import SessionLocal
from app.db.session import SessionRecord

from app.correlation.sqlite_event_store import get_session_events,SQLiteEventStore
from app.correlation.schemas import EntityType
from app.correlation.correlator import Correlator
from app.correlation.risk_scoring import RiskScorer
from app.correlation.explanation_engine import generate_explanation


router=APIRouter(
    prefix="/report",
    tags=["Reports"]
)


@router.get("/{user_id}/{session_id}")
def generate_session_report(
    user_id:str,
    session_id:str
):

    events=get_session_events(
        user_id=user_id,
        session_id=session_id
    )

    if not events:

        return JSONResponse(
            status_code=404,
            content={
                "error":"No events found for session"
            }
        )

    # LOAD PEAK FROM DATABASE
    with SessionLocal() as db:

        session=(
            db.query(SessionRecord)
            .filter(
                SessionRecord.session_id==session_id
            )
            .first()
        )

        peak_score=0
        peak_level="LOW"

        if session:

            peak_score=session.peak_risk_score
            peak_level=session.peak_risk_level

    store=SQLiteEventStore()

    correlator=Correlator(store)

    context=correlator.build_context(
        user_id=user_id,
        session_id=session_id,
        entity_type=EntityType.session,
        entity_id=session_id,
        window_minutes=1440
    )

    scorer=RiskScorer()
    risk=scorer.score(context)

    explanation=generate_explanation(context)

    timeline=[]

    for event in events:

        timeline.append({
            "timestamp":event.timestamp.isoformat(),
            "module":event.module.value,
            "signal":event.signal,
            "severity":event.severity.value
        })

    report={

        "user_id":user_id,
        "session_id":session_id,

        "risk":{
            "score":risk.score,
            "level":risk.level,
            "peak_score":peak_score,
            "peak_level":peak_level,
            "peak_timestamp":session.peak_risk_timestamp.isoformat()
                            if session and session.peak_risk_timestamp 
                            else None
        },

        "modules_triggered":
            list(context.modules_involved),

        "signals":
            context.signals,

        "timeline":
            timeline,

        "explanation":
            explanation.get("analysis",[])

    }

    return JSONResponse(content=report)