from fastapi import APIRouter,Depends,HTTPException
from datetime import datetime,timedelta

from app.db.base import SessionLocal
from app.db.session import SessionRecord,EventRecord,AlertRecord

from app.correlation.correlator import Correlator
from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.risk_scoring import RiskScorer
from app.correlation.schemas import EntityType

from app.correlation.alert_engine import generate_alerts

from app.core.auth_middleware import get_current_user

import uuid

router=APIRouter(prefix="/user")

event_store=SQLiteEventStore()
correlator=Correlator(event_store)
risk_scorer=RiskScorer()


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


def calculate_risk_trend(previous_score,current_score):

    if previous_score is None:
        return "STABLE"

    if current_score > previous_score + 5:
        return "RISING"

    elif current_score < previous_score - 5:
        return "FALLING"

    return "STABLE"

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

@router.post("/{user_id}/session")

def create_session(
    user_id:str,
    session_id:str,
    user=Depends(get_current_user)
):

    jwt_user_id=user.get("sub")

    if user_id!=jwt_user_id:

        raise HTTPException(
            status_code=403,
            detail="User mismatch"
        )

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
                user_id=jwt_user_id,
                status="ACTIVE",
                peak_risk_score=0,
                peak_risk_level="LOW",
                peak_risk_timestamp=None,
                last_risk_score=0,
                risk_trend="STABLE"
            )

            db.add(record)

            db.commit()

        return{
            "status":"session_created",
            "session_id":session_id
        }


@router.get("/{user_id}/alerts")

def get_user_alerts(
    user_id:str,
    user=Depends(get_current_user)
):

    jwt_user_id=user.get("sub")

    if user_id!=jwt_user_id:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized access"
        )

    with SessionLocal() as db:

        alerts=(
            db.query(AlertRecord)
            .filter(
                AlertRecord.user_id==jwt_user_id
            )
            .order_by(
                AlertRecord.timestamp.desc()
            )
            .limit(50)
            .all()
        )

        results=[]

        for a in alerts:

            results.append({

                "alert_type":a.alert_type,
                "message":a.message,
                "timestamp":a.timestamp,
                "session_id":a.session_id

            })

        return{
            "alerts":results
        }


@router.get("/{user_id}/sessions")

def get_user_sessions(
    user_id:str,
    user=Depends(get_current_user)
):

    jwt_user_id=user.get("sub")

    if user_id!=jwt_user_id:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized session access"
        )

    enforce_processing_timeout()
    expire_old_sessions()

    with SessionLocal() as db:

        sessions=(
            db.query(SessionRecord)
            .filter(
                SessionRecord.user_id==jwt_user_id
            )
            .order_by(
                SessionRecord.created_at.desc()
            )
            .all()
        )

        results=[]

        for s in sessions:

            context=correlator.build_context(
                user_id=jwt_user_id,
                session_id=s.session_id,
                entity_type=EntityType.session,
                entity_id=s.session_id,
                window_minutes=1440
            )

            risk=risk_scorer.score(context)

            previous_score=s.last_risk_score
            previous_peak=s.peak_risk_score

            trend=calculate_risk_trend(
                previous_score,
                risk.score
            )

            s.risk_trend=trend

            if risk.score > previous_peak:

                s.peak_risk_score=risk.score
                s.peak_risk_level=risk.level
                s.peak_risk_timestamp=datetime.utcnow()

            s.last_risk_score=risk.score

            alerts=generate_alerts(
                context,
                risk,
                previous_score,
                previous_peak
            )

            for alert in alerts:

                existing_alert=(
                    db.query(AlertRecord)
                    .filter(
                        AlertRecord.session_id==s.session_id,
                        AlertRecord.alert_type==alert["type"]
                    )
                    .first()
                )

                if not existing_alert:

                    record=AlertRecord(
                        alert_id=str(uuid.uuid4()),
                        session_id=s.session_id,
                        user_id=jwt_user_id,
                        alert_type=alert["type"],
                        message=alert["message"],
                        timestamp=alert["timestamp"]
                    )

                    db.add(record)

            results.append({

                "session_id":s.session_id,
                "created_at":s.created_at,
                "risk_score":risk.score,
                "risk_level":risk.level,
                "peak_risk_score":s.peak_risk_score,
                "peak_risk_level":s.peak_risk_level,
                "peak_risk_timestamp":s.peak_risk_timestamp,
                "risk_trend":s.risk_trend,
                "status":s.status

            })

        db.commit()

        return{
            "sessions":results
        }