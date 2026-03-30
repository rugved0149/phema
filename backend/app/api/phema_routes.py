# app/api/phema_routes.py

from fastapi import APIRouter
from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, Dict
from app.orchestrator.phema_engine import PHEMAEngine
from app.correlation.schemas import EntityType
from app.utils.file_handler import save_upload_file
router = APIRouter(prefix="/phema", tags=["PHEMA"])
engine = PHEMAEngine()

class ScanRequest(BaseModel):

    user_id: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    session_id: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    entity_id: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    entity_type: EntityType = Field(
        default=EntityType.session
    )

    url: Optional[str] = None
    text: Optional[str] = None
    file_path: Optional[str] = None
    session_context: Optional[Dict] = None


@router.post("/scan")
def unified_scan(payload: ScanRequest):

    engine.run(
        user_id=payload.user_id,
        session_id=payload.session_id,
        entity_id=payload.entity_id,
        entity_type=payload.entity_type.value,
        url=payload.url,
        text=payload.text,
        file_path=payload.file_path,
        session_context=payload.session_context
    )

    return {
        "status": "scan_executed",
        "user_id": payload.user_id,
        "session_id": payload.session_id,
        "entity_id": payload.entity_id,
        "entity_type": payload.entity_type
    }

@router.post("/upload")

async def upload_file(
    file: UploadFile = File(...)
):

    saved_path = await save_upload_file(file)

    return {
        "status": "uploaded",
        "file_path": str(saved_path)
    }