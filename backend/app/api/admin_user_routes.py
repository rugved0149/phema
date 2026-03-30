from fastapi import APIRouter
from sqlalchemy import distinct
from app.db.base import SessionLocal
from app.db.session import EventRecord

router=APIRouter(prefix="/admin")

@router.get("/users")

def get_users():

    with SessionLocal() as db:

        users=(
            db.query(
                distinct(EventRecord.user_id)
            )
            .all()
        )

        return {
            "users":[u[0] for u in users]
        }