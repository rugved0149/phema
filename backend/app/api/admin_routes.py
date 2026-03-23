from fastapi import APIRouter, Query
from typing import List
from app.core.dependencies import event_store, correlator, risk_scorer
from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.correlator import Correlator
from app.correlation.risk_scoring import RiskScorer
from app.correlation.schemas import EntityType

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/events/{entity_type}/{entity_id}")
def get_event_timeline(
    entity_type: EntityType,
    entity_id: str,
    window_minutes: int = Query(60, ge=1, le=1440)
):
    events = event_store.get_events(
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    return [
        {
            "timestamp": e.timestamp,
            "module": e.module.value,
            "signal": e.signal,
            "severity": e.severity.value,
            "confidence": e.confidence,
            "metadata": e.metadata
        }
        for e in events
    ]

@router.get("/correlation/{entity_type}/{entity_id}")
def get_correlation_context(
    entity_type: EntityType,
    entity_id: str,
    window_minutes: int = 30
):
    context = correlator.build_context(
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    return {
        "total_events": context.total_events,
        "modules_involved": list(context.modules_involved),
        "signals": context.signals,
        "repeated_signals": list(context.repeated_signals),
        "honeypot_hit": context.honeypot_hit,
        "high_severity_events": context.high_severity_events
    }

@router.get("/risk/{entity_type}/{entity_id}")
def admin_risk_view(
    entity_type: EntityType,
    entity_id: str,
    window_minutes: int = 30
):
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
        "reasons": result.reasons
    }

