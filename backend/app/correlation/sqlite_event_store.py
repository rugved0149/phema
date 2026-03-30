from datetime import datetime,timedelta
from typing import List

from app.db.session import EventRecord
from app.db.base import SessionLocal

from app.correlation.schemas import(
    CorrelationEvent,
    EntityType,
    ModuleName,
    SeverityLevel
)

from app.core.logger import logger


class SQLiteEventStore:

    def add_event(self,event:CorrelationEvent)->None:

        try:

            module=event.module.value
            severity=event.severity.value

            with SessionLocal() as db:

                record=EventRecord(

                    user_id=event.user_id,
                    session_id=event.session_id,

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
                db.commit()

                if severity in("medium","high"):

                    logger.info(

                        f"[EVENT STORED] "
                        f"{event.user_id} | "
                        f"{event.session_id} | "
                        f"{module} | "
                        f"{event.signal}"

                    )

        except Exception as e:

            logger.error(
                f"[DB ERROR] Store failed: {e}"
            )


    def get_events(

        self,

        user_id:str,
        session_id:str,

        entity_type,
        entity_id:str,

        window_minutes:int,

        limit:int=500

    )->List[CorrelationEvent]:

        try:

            if isinstance(entity_type,str):

                entity_type=EntityType(entity_type)

            cutoff=datetime.utcnow()-timedelta(
                minutes=window_minutes
            )

            with SessionLocal() as db:

                records=(

                    db.query(EventRecord)

                    .filter(

                        EventRecord.user_id==user_id,
                        EventRecord.session_id==session_id,

                        EventRecord.entity_type==entity_type.value,

                        EventRecord.entity_id==entity_id,

                        EventRecord.timestamp>=cutoff

                    )

                    .order_by(
                        EventRecord.timestamp.asc()
                    )

                    .limit(limit)

                    .all()

                )

                if not records:

                    return []

                events=[]

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


    def get_all_events(

        self,

        user_id:str,
        session_id:str,

        entity_type:EntityType,
        entity_id:str,

        limit:int=1000

    )->List[CorrelationEvent]:

        try:

            with SessionLocal() as db:

                records=(

                    db.query(EventRecord)

                    .filter(

                        EventRecord.user_id==user_id,
                        EventRecord.session_id==session_id,

                        EventRecord.entity_type==entity_type.value,

                        EventRecord.entity_id==entity_id

                    )

                    .order_by(
                        EventRecord.timestamp.asc()
                    )

                    .limit(limit)

                    .all()

                )

                if not records:

                    return []

                return[
                    self._record_to_event(r)
                    for r in records
                ]

        except Exception as e:

            logger.error(
                f"[DB ERROR] Fetch-all failed: {e}"
            )

            return []


    def purge_old_events(

        self,

        max_age_minutes:int=1440

    )->int:

        try:

            cutoff=datetime.utcnow()-timedelta(
                minutes=max_age_minutes
            )

            with SessionLocal() as db:

                deleted=(

                    db.query(EventRecord)

                    .filter(
                        EventRecord.timestamp<cutoff
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


    @staticmethod
    def _record_to_event(
        r:EventRecord
    )->CorrelationEvent:

        return CorrelationEvent(

            user_id=r.user_id,
            session_id=r.session_id,

            event_id=r.event_id,

            entity_id=r.entity_id,

            entity_type=EntityType(
                r.entity_type
            ),

            module=ModuleName(
                r.module
            ),

            signal=r.signal,

            confidence=r.confidence,

            severity=SeverityLevel(
                r.severity
            ),

            metadata=r.event_metadata or {},

            timestamp=r.timestamp

        )

_store=SQLiteEventStore()
def get_session_events(
    user_id:str,
    session_id:str
):
    return _store.get_all_events(
        user_id=user_id,
        session_id=session_id,
        entity_type=EntityType.session,
        entity_id=session_id
    )