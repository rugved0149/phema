from fastapi import APIRouter, Query, Depends
from typing import List

from app.core.dependencies import event_store, correlator, risk_scorer
from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.schemas import EntityType
from app.correlation.analytics_engine import AnalyticsEngine

from app.db.base import SessionLocal
from app.db.session import EventRecord, AlertRecord

from app.core.auth_middleware import get_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_admin_user)]
)

analytics = AnalyticsEngine()
store = SQLiteEventStore()


@router.get("/events/{user_id}/{session_id}/{entity_type}/{entity_id}")
def get_event_timeline(
    user_id: str,
    session_id: str,
    entity_type: EntityType,
    entity_id: str,
    window_minutes: int = Query(60, ge=1, le=1440)
):

    events = event_store.get_events(
        user_id=user_id,
        session_id=session_id,
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


@router.get("/alerts")
def get_system_alerts():

    with SessionLocal() as db:

        alerts = (
            db.query(AlertRecord)
            .order_by(
                AlertRecord.timestamp.desc()
            )
            .limit(100)
            .all()
        )

        results = []

        for a in alerts:

            results.append({

                "alert_type": a.alert_type,
                "message": a.message,
                "timestamp": a.timestamp,
                "session_id": a.session_id,
                "user_id": a.user_id

            })

        return {
            "alerts": results
        }


@router.get("/risk/{user_id}/{session_id}/{entity_type}/{entity_id}")
def get_correlation_context(
    user_id: str,
    session_id: str,
    entity_type: EntityType,
    entity_id: str,
    window_minutes: int = 120
):

    context = correlator.build_context(
        user_id=user_id,
        session_id=session_id,
        entity_type=entity_type,
        entity_id=entity_id,
        window_minutes=window_minutes
    )

    result = risk_scorer.score(context)

    return {
        "user_id": user_id,
        "session_id": session_id,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "risk_score": result.score,
        "risk_level": result.level,
        "reasons": result.reasons
    }


@router.get("/analytics")
def get_analytics():

    return {
        "modules": analytics.get_module_stats(),
        "signals": analytics.get_signal_stats(),
        "severity": analytics.get_severity_stats(),
        "top_entities": analytics.get_top_entities()
    }


@router.get("/event-count")
def get_event_count():

    with SessionLocal() as db:

        total = db.query(EventRecord).count()

        return {
            "total_events": total
        }


@router.post("/purge")
def purge_old_events():

    store.purge_old_events()

    return {
        "status": "old events purged"
    }