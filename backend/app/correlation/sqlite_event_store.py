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

from app.core.logger import logger


class SQLiteEventStore:
    """
    Persistent SQLite event store.
    Optimized for ordered reads,
    safe sessions, purge support,
    and structured logging.
    """

    # WRITE EVENT

    def add_event(self, event: CorrelationEvent) -> None:
        logger.info(
            f"[DB WRITE CONFIRMED] {event.entity_id} | {event.signal}"
        )
        try:
            logger.info(
                f"[DB WRITE] {event.entity_id} | {event.module.value} | {event.signal}"
            )
            module = event.module.value
            severity = event.severity.value

            with SessionLocal() as db:

                record = EventRecord(
                    event_id=event.event_id,
                    entity_id=event.entity_id,
                    entity_type=event.entity_type.value,
                    module=module,
                    signal=event.signal,
                    confidence=event.confidence,
                    severity=severity,
                    event_metadata=event.metadata,
                    timestamp=event.timestamp
                )

                db.add(record)
                db.flush()
                db.commit()

                if severity in ("medium", "high"):

                    logger.info(
                        f"[EVENT STORED] {module} | {event.signal}"
                    )

        except Exception as e:

            logger.error(
                f"[DB ERROR] Store failed: {e}"
            )

    # READ EVENTS

    def get_events(
        self,
        entity_type: EntityType,
        entity_id: str,
        window_minutes: int,
        limit: int = 500
    ) -> List[CorrelationEvent]:

        try:

            cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)

            with SessionLocal() as db:

                records = (
                    db.query(EventRecord)
                    .filter(
                        EventRecord.entity_type == entity_type.value,
                        EventRecord.entity_id == entity_id,
                        EventRecord.timestamp >= cutoff
                    )
                    .order_by(EventRecord.timestamp.asc())
                    .limit(limit)
                    .all()
                )

                if not records:
                    return []

                events = []

                for r in records:

                    try:
                        events.append(
                            self._record_to_event(r)
                        )

                    except Exception as e:

                        logger.error(
                            f"[DB ERROR] Conversion failed: {e}"
                        )

                return events

        except Exception as e:

            logger.error(
                f"[DB ERROR] Fetch failed: {e}"
            )

            return []

    # READ ALL EVENTS

    def get_all_events(
        self,
        entity_type: EntityType,
        entity_id: str,
        limit: int = 1000
    ) -> List[CorrelationEvent]:

        try:

            with SessionLocal() as db:

                records = (
                    db.query(EventRecord)
                    .filter(
                        EventRecord.entity_type == entity_type.value,
                        EventRecord.entity_id == entity_id
                    )
                    .order_by(EventRecord.timestamp.asc())
                    .limit(limit)
                    .all()
                )

                if not records:
                    return []

                events = []

                for r in records:

                    try:
                        events.append(
                            self._record_to_event(r)
                        )

                    except Exception as e:

                        logger.error(
                            f"[DB ERROR] Conversion failed: {e}"
                        )

                return events

        except Exception as e:

            logger.error(
                f"[DB ERROR] Fetch-all failed: {e}"
            )

            return []

    # PURGE OLD EVENTS

    def purge_old_events(
        self,
        max_age_minutes: int = 1440
    ) -> int:

        try:

            cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)

            with SessionLocal() as db:

                deleted = (
                    db.query(EventRecord)
                    .filter(
                        EventRecord.timestamp < cutoff
                    )
                    .delete()
                )

                db.commit()

                logger.info(
                    f"[DB PURGE] Removed {deleted} events"
                )

                return deleted

        except Exception as e:

            logger.error(
                f"[DB ERROR] Purge failed: {e}"
            )

            return 0

    # RECORD CONVERSION

    @staticmethod
    def _record_to_event(
        r: EventRecord
    ) -> CorrelationEvent:

        return CorrelationEvent(
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