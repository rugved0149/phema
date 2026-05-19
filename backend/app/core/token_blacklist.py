from app.db.base import SessionLocal
from app.db.session import RevokedToken

from datetime import datetime
import uuid


def revoke_token(
    token:str,
    expiry:datetime
):

    with SessionLocal() as db:

        record=RevokedToken(

            token_id=str(uuid.uuid4()),

            token=token,

            revoked_at=datetime.utcnow(),

            expires_at=expiry

        )

        db.add(record)

        db.commit()


def is_token_revoked(
    token:str
):

    with SessionLocal() as db:

        record=(
            db.query(RevokedToken)
            .filter(
                RevokedToken.token==token
            )
            .first()
        )

        return record is not None
    
def cleanup_expired_tokens():

    with SessionLocal() as db:

        db.query(RevokedToken).filter(
            RevokedToken.expires_at < datetime.utcnow()
        ).delete()

        db.commit()