# app/api/phema_routes.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict

from app.orchestrator.phema_engine import PHEMAEngine
from app.correlation.schemas import EntityType


router = APIRouter(prefix="/phema", tags=["PHEMA"])

engine = PHEMAEngine()


class ScanRequest(BaseModel):

    #VALIDATED ENTITY ID
    entity_id: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Unique identifier for entity (session, user, ip, file)"
    )

    #ENUM-BASED ENTITY TYPE (IMPORTANT)
    entity_type: EntityType = Field(
        default=EntityType.session,
        description="Type of entity being scanned"
    )

    url: Optional[str] = None
    text: Optional[str] = None
    file_path: Optional[str] = None
    session_context: Optional[Dict] = None


@router.post("/scan")
def unified_scan(payload: ScanRequest):
    """
    Unified entry point for running PHEMA modules.
    """

    engine.run(
        entity_id=payload.entity_id,
        entity_type=payload.entity_type.value,  #convert enum -> string
        url=payload.url,
        text=payload.text,
        file_path=payload.file_path,
        session_context=payload.session_context
    )

    return {
        "status": "scan_executed",
        "entity_id": payload.entity_id,
        "entity_type": payload.entity_type
    }