# app/correlation/analytics_engine.py

from typing import Dict
from sqlalchemy import func
from app.db.base import SessionLocal
from app.db.session import EventRecord

class AnalyticsEngine:

    # MODULE DISTRIBUTION
    def get_module_stats(self) -> Dict:
        with SessionLocal() as db:
            rows = (
                db.query(
                    EventRecord.module,
                    func.count(EventRecord.module)
                )
                .group_by(
                    EventRecord.module
                )
                .all()
            )
            return {
                module: count
                for module, count in rows
            }

    # SIGNAL DISTRIBUTION
    def get_signal_stats(self) -> Dict:
        with SessionLocal() as db:
            rows = (
                db.query(
                    EventRecord.signal,
                    func.count(EventRecord.signal)
                )
                .group_by(
                    EventRecord.signal
                )
                .all()
            )
            return {
                signal: count
                for signal, count in rows
            }

    # SEVERITY DISTRIBUTION
    def get_severity_stats(self) -> Dict:
        with SessionLocal() as db:
            rows = (
                db.query(
                    EventRecord.severity,
                    func.count(EventRecord.severity)
                )
                .group_by(
                    EventRecord.severity
                )
                .all()
            )
            return {
                severity: count
                for severity, count in rows
            }

    # TOP ENTITIES
    def get_top_entities(
        self,
        limit: int = 5
    ) -> Dict:
        with SessionLocal() as db:
            rows = (
                db.query(
                    EventRecord.entity_id,
                    func.count(EventRecord.entity_id)
                )
                .group_by(
                    EventRecord.entity_id
                )
                .order_by(
                    func.count(
                        EventRecord.entity_id
                    ).desc()
                )
                .limit(limit)
                .all()
            )
            return {
                entity: count
                for entity, count in rows
            }