# app/db/session.py

from sqlalchemy import Column, String, Float, DateTime, JSON
from datetime import datetime

from app.db.base import Base


class EventRecord(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, index=True)
    entity_id = Column(String, index=True)
    entity_type = Column(String, index=True)
    module = Column(String, index=True)
    signal = Column(String)
    confidence = Column(Float)
    severity = Column(String)
    event_metadata = Column(JSON)   # ✅ MUST be this name
    timestamp = Column(DateTime, default=datetime.utcnow)
