# app/correlation/analytics_engine.py

from collections import Counter
from app.db.base import SessionLocal
from app.db.session import EventRecord


class AnalyticsEngine:

    def get_module_stats(self):

        db = SessionLocal()
        try:
            events = db.query(EventRecord.module).all()
            modules = [e[0] for e in events]

            counter = Counter(modules)

            return dict(counter)

        finally:
            db.close()


    def get_signal_stats(self):

        db = SessionLocal()
        try:
            events = db.query(EventRecord.signal).all()
            signals = [e[0] for e in events]

            counter = Counter(signals)

            return dict(counter)

        finally:
            db.close()


    def get_severity_stats(self):

        db = SessionLocal()
        try:
            events = db.query(EventRecord.severity).all()
            severity = [e[0] for e in events]

            counter = Counter(severity)

            return dict(counter)

        finally:
            db.close()


    def get_top_entities(self, limit=5):

        db = SessionLocal()
        try:
            events = db.query(EventRecord.entity_id).all()
            entities = [e[0] for e in events]

            counter = Counter(entities)

            return dict(counter.most_common(limit))

        finally:
            db.close()