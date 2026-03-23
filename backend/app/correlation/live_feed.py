# app/correlation/live_feed.py

from typing import List, Dict
from app.db.base import SessionLocal
from app.db.session import EventRecord

def get_latest_events(
    limit: int = 20
) -> List[Dict]:
    # Column selection reduces memory load
    with SessionLocal() as db:
        records = (
            db.query(
                EventRecord.timestamp,
                EventRecord.entity_id,
                EventRecord.entity_type,
                EventRecord.module,
                EventRecord.signal,
                EventRecord.severity
            )
            .order_by(
                EventRecord.timestamp.desc()
            )
            .limit(limit)
            .all()
        )
        # Fast list creation
        results = [
            {
                "time": r.timestamp.isoformat(),
                "entity_id": r.entity_id,
                "entity_type": r.entity_type,
                "module": r.module,
                "signal": r.signal,
                "severity": r.severity,
                "label":
                    f"{r.module}:{r.signal}"
            }
            for r in records
        ]
        return results