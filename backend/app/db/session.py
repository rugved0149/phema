from sqlalchemy import Column, String, Float, DateTime, JSON, Index
from datetime import datetime
from app.db.base import Base

class EventRecord(Base):
    __tablename__ = "events"

    event_id = Column(
        String,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String,
        index=True,
        nullable=False,
        default="system"
    )

    session_id = Column(
        String,
        index=True,
        nullable=False,
        default="default"
    )

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

    event_metadata = Column(
        JSON,
        nullable=True
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
        nullable=False
    )

class SessionRecord(Base):

    __tablename__="sessions"

    session_id=Column(
        String,
        primary_key=True,
        index=True
    )

    user_id=Column(
        String,
        index=True,
        nullable=False
    )

    created_at=Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    status=Column(
        String,
        index=True,
        nullable=False,
        default="CREATED"
    )

    last_activity=Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    peak_risk_score=Column(
        Float,
        default=0,
        nullable=False
    )

    peak_risk_level=Column(
        String,
        default="LOW",
        nullable=False
    )

    peak_risk_timestamp=Column(
        DateTime,
        nullable=True,
        index=True
    )
    
Index(
    "idx_entity_lookup",
    EventRecord.user_id,
    EventRecord.session_id,
    EventRecord.entity_type,
    EventRecord.entity_id,
    EventRecord.timestamp
)

Index(
    "idx_module_signal",
    EventRecord.module,
    EventRecord.signal
)