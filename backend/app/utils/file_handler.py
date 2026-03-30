"""
File upload handler for PHEMA.

Handles:
- Upload validation
- Safe file storage
- File size enforcement
- Extension filtering
- Unique filename generation
- Cleanup support
"""

import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024


ALLOWED_EXTENSIONS = {

    ".pdf",
    ".docx",
    ".txt",
    ".zip",
    ".png",
    ".jpg",
    ".jpeg",
    ".exe",
    ".dll",
    ".ps1",
    ".bin",
    ".bat",
    ".cmd",
    ".js",
    ".vbs"

}


def validate_extension(filename: str):

    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed: {ext}"
        )

    return ext


async def save_upload_file(file: UploadFile) -> Path:

    validate_extension(file.filename)

    unique_name = f"{uuid.uuid4().hex}_{file.filename}"

    destination = UPLOAD_DIR / unique_name

    size = 0

    try:

        with destination.open("wb") as buffer:

            while True:

                chunk = await file.read(8192)

                if not chunk:
                    break

                size += len(chunk)

                if size > MAX_FILE_SIZE:

                    buffer.close()
                    destination.unlink(missing_ok=True)

                    raise HTTPException(
                        status_code=400,
                        detail="File too large (max 10MB)"
                    )

                buffer.write(chunk)

    except Exception:

        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="File upload failed"
        )

    return destination


def delete_file(file_path: str):

    try:

        path = Path(file_path)

        if path.exists():
            path.unlink()

    except Exception:
        pass