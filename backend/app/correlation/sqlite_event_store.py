# app/correlation/sqlite_event_store.py

from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from app.db.session import EventRecord
from app.db.base import SessionLocal
from app.correlation.schemas import (
    CorrelationEvent,
    EntityType,
    ModuleName,
    SeverityLevel
)

class SQLiteEventStore:
    """
    Persistent event store using SQLite.
    """

    def add_event(self, event: CorrelationEvent) -> None:
        db: Session = SessionLocal()
        try:
            record = EventRecord(
                event_id=event.event_id,
                entity_id=event.entity_id,
                entity_type=event.entity_type.value,
                module=event.module.value,
                signal=event.signal,
                confidence=event.confidence,
                severity=event.severity.value,
                event_metadata=event.metadata,
                timestamp=event.timestamp
)
            db.add(record)
            db.commit()
        finally:
            db.close()

    def get_events(
        self,
        entity_type: EntityType,
        entity_id: str,
        window_minutes: int
    ) -> List[CorrelationEvent]:
        db: Session = SessionLocal()
        try:
            cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)

            records = (
                db.query(EventRecord)
                .filter(
                    EventRecord.entity_type == entity_type.value,
                    EventRecord.entity_id == entity_id,
                    EventRecord.timestamp >= cutoff
                )
                .all()
            )

            return [
                CorrelationEvent(
                    event_id=r.event_id,
                    entity_id=r.entity_id,
                    entity_type=EntityType(r.entity_type),
                    module=ModuleName(r.module),
                    signal=r.signal,
                    confidence=r.confidence,
                    severity=SeverityLevel(r.severity),
                    metadata=r.event_metadata or {},
                    timestamp=r.timestamp
                )
                for r in records
            ]

        finally:
            db.close()

    def get_all_events(
        self,
        entity_type: EntityType,
        entity_id: str
    ):
        db = SessionLocal()
        try:
            records = (
                db.query(EventRecord)
                .filter(
                    EventRecord.entity_type == entity_type.value,
                    EventRecord.entity_id == entity_id
                )
                .order_by(EventRecord.timestamp)
                .all()
            )

            return [
                CorrelationEvent(
                    event_id=r.event_id,
                    entity_id=r.entity_id,
                    entity_type=EntityType(r.entity_type),
                    module=ModuleName(r.module),
                    signal=r.signal,
                    confidence=r.confidence,
                    severity=SeverityLevel(r.severity),
                    metadata=r.event_metadata or {},
                    timestamp=r.timestamp
                )
                for r in records
            ]

        finally:
            db.close()