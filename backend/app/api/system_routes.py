from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/status")
def system_status():

    return {
        "status": "operational",
        "time": datetime.utcnow(),
        "modules": [
            "phishing",
            "tone",
            "file_checker",
            "honeypot",
            "anomaly"
        ]
    }