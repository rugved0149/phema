# app/correlation/live_feed.py

from typing import List, Dict
from app.db.base import SessionLocal
from app.db.session import EventRecord


def get_latest_events(limit: int = 20) -> List[Dict]:

    db = SessionLocal()

    try:

        events = (
            db.query(EventRecord)
            .order_by(EventRecord.timestamp.desc())
            .limit(limit)
            .all()
        )

        results = []

        for e in events:

            results.append({
                "time": e.timestamp,
                "entity_id": e.entity_id,
                "entity_type": e.entity_type,
                "module": e.module,
                "signal": e.signal,
                "severity": e.severity
            })

        return results

    finally:
        db.close()