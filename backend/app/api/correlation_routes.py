from fastapi import APIRouter
from typing import Dict
from app.core.event_emitter import emit_event
from app.correlation.schemas import CorrelationEvent, EntityType
from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.correlator import Correlator
from app.correlation.risk_scoring import RiskScorer
from app.correlation.explanation_engine import generate_explanation
from app.correlation.graph_engine import build_graph
from app.correlation.threat_memory import threat_memory
from app.correlation.analytics_engine import AnalyticsEngine
from app.correlation.attack_replay import build_attack_replay
from app.correlation.live_feed import get_latest_events
from app.core.dependencies import event_store, correlator, risk_scorer
router = APIRouter(prefix="/correlation", tags=["Correlation"])


# -------------------------
# SINGLETONS
# -------------------------

analytics = AnalyticsEngine()

# -------------------------
# EVENT INGESTION
# -------------------------

@router.post("/event")
def ingest_event(event: CorrelationEvent) -> Dict[str, str]:

    emit_event(event)

    return {
        "status": "accepted",
        "event_id": event.event_id
    }


# -------------------------
# RISK SCORING
# -------------------------

@router.get("/risk/{entity_type}/{entity_id}")
def get_risk(entity_type: EntityType, entity_id: str, window_minutes: int = 120):

    context = correlator.build_context(
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    result = risk_scorer.score(context)

    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "risk_score": result.score,
        "risk_level": result.level,
        "attack_type": result.attack_type,
        "mitre_attack": result.mitre,
        "reasons": result.reasons
    }


# -------------------------
# EXPLANATION ENGINE
# -------------------------

@router.get("/explain/{entity_type}/{entity_id}")
def explain_detection(entity_type: EntityType, entity_id: str, window_minutes: int = 120):

    context = correlator.build_context(
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    explanation = generate_explanation(context)

    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "explanation": explanation
    }


# -------------------------
# ATTACK GRAPH
# -------------------------

@router.get("/graph/{entity_type}/{entity_id}")
def get_attack_graph(entity_type: EntityType, entity_id: str, window_minutes: int = 120):

    context = correlator.build_context(
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    graph = build_graph(context)

    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "graph": graph
    }


# -------------------------
# THREAT MEMORY
# -------------------------

@router.get("/history/{entity_id}")
def get_threat_history(entity_id: str):

    history = threat_memory.get_entity_activity(entity_id)

    return {
        "entity_id": entity_id,
        "history": history
    }


# -------------------------
# ANALYTICS
# -------------------------

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

@router.get("/export/events")
def export_events():

    events = event_store.get_events(
        entity_type=EntityType.session,
        entity_id="*",
        window_minutes=100000
    )

    return {
        "total_events": len(events),
        "events": [e.dict() for e in events]
    }

@router.get("/replay/{entity_type}/{entity_id}")
def attack_replay(entity_type: EntityType, entity_id: str, window_minutes: int = 120):

    events = event_store.get_events(
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    timeline = build_attack_replay(events)

    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "timeline": timeline
    }

@router.get("/live")
def live_threat_feed(limit: int = 20):

    events = get_latest_events(limit)

    return {
        "events": events
    }   