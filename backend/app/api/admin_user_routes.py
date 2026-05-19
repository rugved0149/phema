from fastapi import APIRouter, Depends
from app.core.auth_middleware import get_admin_user
from sqlalchemy import distinct

from app.db.base import SessionLocal
from app.db.session import EventRecord,SessionRecord

from app.core.audit_logger import log_admin_action
from app.core.auth_middleware import get_admin_user

router=APIRouter(prefix="/admin", dependencies=[Depends(get_admin_user)])

@router.get("/users")

def get_users(
    admin=Depends(get_admin_user)
):

    log_admin_action(
        user_id=admin.get("sub"),
        action="view_users",
        endpoint="/admin/users"
    )

    with SessionLocal() as db:

        users=(
            db.query(
                distinct(EventRecord.user_id)
            )
            .all()
        )

        return{
            "users":[u[0] for u in users]
        }

@router.get("/sessions")

def get_all_sessions():

    with SessionLocal() as db:

        sessions=(
            db.query(SessionRecord)
            .order_by(
                SessionRecord.created_at.desc()
            )
            .all()
        )

        results=[]

        for s in sessions:

            results.append({

                "session_id":s.session_id,

                "user_id":s.user_id,

                "created_at":s.created_at,

                "status":s.status,

                "last_activity":s.last_activity,

                "last_risk_score":s.last_risk_score,

                "risk_trend":s.risk_trend,

                "peak_risk_score":s.peak_risk_score,

                "peak_risk_level":s.peak_risk_level,

                "peak_risk_timestamp":s.peak_risk_timestamp

            })

        return{
            "sessions":results
        }