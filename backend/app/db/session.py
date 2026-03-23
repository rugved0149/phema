# app/db/session.py

from sqlalchemy import Column, String, Float, DateTime, JSON, Index
from datetime import datetime

from app.db.base import Base


class EventRecord(Base):
    __tablename__ = "events"

    # PRIMARY KEY

    event_id = Column(
        String,
        primary_key=True,
        index=True
    )

    # CORE INDEXED FIELDS

    entity_id = Column(
        String,
        index=True,
        nullable=False
    )

    entity_type = Column(
        String,
        index=True,
        nullable=False
    )

    module = Column(
        String,
        index=True,
        nullable=False
    )

    signal = Column(
        String,
        index=True
    )

    severity = Column(
        String,
        index=True
    )

    confidence = Column(
        Float,
        nullable=False
    )

    # METADATA

    event_metadata = Column(
        JSON,
        nullable=True
    )

    # TIMESTAMP (CRITICAL INDEX)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
        nullable=False
    )

# COMPOSITE INDEXES

Index(
    "idx_entity_lookup",
    EventRecord.entity_type,
    EventRecord.entity_id,
    EventRecord.timestamp
)

Index(
    "idx_module_signal",
    EventRecord.module,
    EventRecord.signal
)