from sqlalchemy import Column, String, Boolean, DateTime, JSON
from datetime import datetime

from app.db.base import Base


class User(Base):

    __tablename__ = "users"

    user_id = Column(
        String,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    metadata_json = Column(
        JSON,
        nullable=True
    )