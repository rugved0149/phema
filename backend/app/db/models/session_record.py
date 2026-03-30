from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from datetime import datetime

from app.db.base import Base


class SessionRecord(Base):

    __tablename__ = "sessions"

    session_id = Column(
        String,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String,
        ForeignKey("users.user_id"),
        index=True,
        nullable=False
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    ended_at = Column(
        DateTime,
        nullable=True
    )


Index(
    "idx_user_sessions",
    SessionRecord.user_id,
    SessionRecord.created_at
)