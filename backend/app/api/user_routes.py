from fastapi import APIRouter
from datetime import datetime,timedelta

from app.db.base import SessionLocal
from app.db.session import SessionRecord,EventRecord

from app.correlation.correlator import Correlator
from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.risk_scoring import RiskScorer
from app.correlation.schemas import EntityType

router=APIRouter(prefix="/user")

event_store=SQLiteEventStore()
correlator=Correlator(event_store)
risk_scorer=RiskScorer()

def update_session_status(session_id:str,new_status:str):
    with SessionLocal() as db:
        session=(
            db.query(SessionRecord)
            .filter(
                SessionRecord.session_id==session_id
            )
            .first()
        )
        if session:
            session.status=new_status
            session.last_activity=datetime.utcnow()
            db.commit()


def expire_old_sessions():
    expiry_time=datetime.utcnow()-timedelta(minutes=60)
    with SessionLocal() as db:
        sessions=(
            db.query(SessionRecord)
            .filter(
                SessionRecord.status=="ACTIVE",
                SessionRecord.last_activity < expiry_time
            )
            .all()
        )
        for s in sessions:
            s.status="EXPIRED"
        db.commit()

def enforce_processing_timeout():
    timeout_time=datetime.utcnow()-timedelta(minutes=5)
    with SessionLocal() as db:
        stuck_sessions=(
            db.query(SessionRecord)
            .filter(
                SessionRecord.status=="PROCESSING",
                SessionRecord.last_activity < timeout_time
            )
            .all()
        )
        for s in stuck_sessions:
            s.status="FAILED"
        db.commit()

@router.post("/{user_id}/session")
def create_session(user_id:str,session_id:str):
    with SessionLocal() as db:
        existing=(
            db.query(SessionRecord)
            .filter(
                SessionRecord.session_id==session_id
            )
            .first()
        )
        if not existing:
            record=SessionRecord(
                session_id=session_id,
                user_id=user_id,
                status="ACTIVE",
                peak_risk_score=0,
                peak_risk_level="LOW",
                peak_risk_timestamp=None
            )
            db.add(record)
            db.commit()
        return{
            "status":"session_created",
            "session_id":session_id
        }

@router.get("/{user_id}/sessions")
def get_user_sessions(user_id:str):
    enforce_processing_timeout()
    expire_old_sessions()
    with SessionLocal() as db:
        sessions=(
            db.query(SessionRecord)
            .filter(
                SessionRecord.user_id==user_id
            )
            .order_by(
                SessionRecord.created_at.desc()
            )
            .all()
        )
        results=[]
        for s in sessions:
            context=correlator.build_context(
                user_id=user_id,
                session_id=s.session_id,
                entity_type=EntityType.session,
                entity_id=s.session_id,
                window_minutes=1440
            )
            risk=risk_scorer.score(context)

            if risk.score > s.peak_risk_score:
                s.peak_risk_score=risk.score
                s.peak_risk_level=risk.level
                s.peak_risk_timestamp=datetime.utcnow()
                db.commit()

            results.append({
                "session_id":s.session_id,
                "created_at":s.created_at,
                "risk_score":risk.score,
                "risk_level":risk.level,
                "peak_risk_score":s.peak_risk_score,
                "peak_risk_level":s.peak_risk_level,
                "peak_risk_timestamp":s.peak_risk_timestamp,
                "status":s.status
            })
        return{
            "sessions":results
        }