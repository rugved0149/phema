# app/api/phema_routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict

from app.orchestrator.phema_engine import PHEMAEngine
from app.correlation.schemas import EntityType

from app.utils.file_handler import save_upload_file

from app.core.auth_middleware import get_current_user


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

def unified_scan(
    payload: ScanRequest,
    user=Depends(get_current_user)
):

    # Prevent user spoofing
    user_id=user.get("sub")

    engine.run(
        user_id=user_id,
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
        "user_id": user_id,
        "session_id": payload.session_id,
        "entity_id": payload.entity_id,
        "entity_type": payload.entity_type
    }


@router.post("/upload")

async def upload_file(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):

    saved_path = await save_upload_file(file)

    return {
        "status": "uploaded",
        "file_path": str(saved_path)
    }