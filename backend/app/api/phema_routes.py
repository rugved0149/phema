# app/api/phema_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict

from app.orchestrator.phema_engine import PHEMAEngine


router = APIRouter(prefix="/phema", tags=["PHEMA"])

engine = PHEMAEngine()


class ScanRequest(BaseModel):
    entity_id: str
    entity_type: str = "session"

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
        entity_type=payload.entity_type,
        url=payload.url,
        text=payload.text,
        file_path=payload.file_path,
        session_context=payload.session_context
    )

    return {
        "status": "scan_executed",
        "entity_id": payload.entity_id
    }