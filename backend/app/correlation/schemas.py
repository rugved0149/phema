# app/correlation/schemas.py
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field, validator

# ENUMS

class EntityType(str, Enum):
    session = "session"
    user = "user"
    ip = "ip"
    file = "file"

class ModuleName(str, Enum):
    phishing = "phishing"
    tone = "tone"
    anomaly = "anomaly"
    honeypot = "honeypot"
    file_checker = "file_checker"

class SeverityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# CORE EVENT SCHEMA

class CorrelationEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str = Field(
        ...,
        description="User identifier owning the session"
    )
    session_id: str = Field(
        ...,
        description="Session identifier under the user"
    )
    entity_id: str = Field(
        ...,
        description="Primary entity identifier (session_id, ip, user_id, file_hash)"
    )
    entity_type: EntityType
    module: ModuleName
    signal: str = Field(
        ...,
        description="Atomic signal name emitted by the module"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Module confidence score between 0 and 1"
    )
    severity: SeverityLevel
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Module-specific contextual data"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )

    # VALIDATORS

    @validator("signal")
    def signal_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("signal must be a non-empty string")
        return v

    @validator("entity_id")
    def entity_id_not_empty(cls, v):

        if not v or not v.strip():
            raise ValueError("entity_id must be non-empty")
        return v

    @validator("user_id")
    def user_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("user_id must be non-empty")
        return v
    
    @validator("session_id")
    def session_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("session_id must be non-empty")
        return v
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "user_abc123",
                "session_id": "session_xyz789",
                "entity_id": "session_xyz789",
                "entity_type": "session",
                "module": "phishing",
                "signal": "phishing:domain:suspicious",
                "confidence": 0.72,
                "severity": "medium",
                "metadata": {
                    "domain_age_days": 2,
                    "brand_similarity": 0.91
                }
            }
        }