from fastapi import APIRouter
from typing import Dict

from app.core.event_emitter import emit_event
from app.correlation.schemas import CorrelationEvent, EntityType
from app.correlation.explanation_engine import generate_explanation
from app.correlation.graph_engine import build_graph
from app.correlation.threat_memory import threat_memory
from app.correlation.analytics_engine import AnalyticsEngine
from app.correlation.attack_replay import build_attack_replay
from app.correlation.live_feed import get_latest_events

from app.core.dependencies import event_store, correlator, risk_scorer

router=APIRouter(prefix="/correlation",tags=["Correlation"])

analytics=AnalyticsEngine()


@router.post("/event")
def ingest_event(event:CorrelationEvent)->Dict[str,str]:

    emit_event(event)

    return{
        "status":"accepted",
        "event_id":event.event_id
    }


@router.get("/risk/{user_id}/{session_id}/{entity_type}/{entity_id}")
def get_risk(
    user_id:str,
    session_id:str,
    entity_type:EntityType,
    entity_id:str,
    window_minutes:int=120
):

    context=correlator.build_context(
        user_id=user_id,
        session_id=session_id,
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    result=risk_scorer.score(context)

    return{
        "user_id":user_id,
        "session_id":session_id,
        "entity_id":entity_id,
        "entity_type":entity_type,
        "risk_score":result.score,
        "risk_level":result.level,
        "attack_type":result.attack_type,
        "mitre_attack":result.mitre,
        "reasons":result.reasons,
        "breakdown":result.breakdown
    }


@router.get("/explain/{user_id}/{session_id}/{entity_type}/{entity_id}")
def explain_detection(
    user_id:str,
    session_id:str,
    entity_type:EntityType,
    entity_id:str,
    window_minutes:int=120
):

    context=correlator.build_context(
        user_id=user_id,
        session_id=session_id,
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    explanation=generate_explanation(context)

    return{
        "user_id":user_id,
        "session_id":session_id,
        "entity_id":entity_id,
        "entity_type":entity_type,
        "explanation":explanation
    }


@router.get("/events/{user_id}/{session_id}")
def get_session_events(
    user_id:str,
    session_id:str,
    window_minutes:int=1440
):

    events=event_store.get_events(

        user_id=user_id,

        session_id=session_id,

        entity_type="session",

        entity_id=session_id,

        window_minutes=window_minutes

    )

    return{

        "events":[

            {

                "module":(
                    e.module.value
                    if hasattr(e.module,"value")
                    else e.module
                ),

                "signal":e.signal,

                "severity":(
                    e.severity.value
                    if hasattr(e.severity,"value")
                    else e.severity
                ),

                "timestamp":e.timestamp.isoformat(),

                "entity_id":e.entity_id

            }

            for e in events

        ]

    }


@router.get("/graph/{user_id}/{session_id}/{entity_type}/{entity_id}")
def get_attack_graph(
    user_id:str,
    session_id:str,
    entity_type:EntityType,
    entity_id:str,
    window_minutes:int=120
):

    context=correlator.build_context(
        user_id=user_id,
        session_id=session_id,
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    graph=build_graph(context)

    return{
        "user_id":user_id,
        "session_id":session_id,
        "entity_id":entity_id,
        "entity_type":entity_type,
        "graph":graph
    }


@router.get("/history/{entity_id}")
def get_threat_history(entity_id:str):

    history=threat_memory.get_entity_activity(entity_id)

    return{
        "entity_id":entity_id,
        "history":history
    }


@router.get("/stats/modules")
def module_stats():
    return analytics.get_module_stats()


@router.get("/stats/signals")
def signal_stats():
    return analytics.get_signal_stats()


@router.get("/stats/severity")
def severity_stats():
    return analytics.get_severity_stats()


@router.get("/stats/top_entities")
def top_entities():
    return analytics.get_top_entities()


@router.get("/replay/{user_id}/{session_id}/{entity_type}/{entity_id}")
def attack_replay(
    user_id:str,
    session_id:str,
    entity_type:EntityType,
    entity_id:str,
    window_minutes:int=120
):

    events=event_store.get_events(
        user_id=user_id,
        session_id=session_id,
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    timeline=build_attack_replay(events)

    return{
        "user_id":user_id,
        "session_id":session_id,
        "entity_id":entity_id,
        "entity_type":entity_type,
        "timeline":timeline
    }


@router.get("/live")
def live_threat_feed(limit:int=20):

    events=get_latest_events(limit)

    return{
        "events":events
    }