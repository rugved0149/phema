from app.db.base import SessionLocal
from app.db.session import AuditRecord

import uuid
from datetime import datetime


def log_admin_action(
    user_id:str,
    action:str,
    endpoint:str,
    metadata:dict=None
):

    with SessionLocal() as db:

        record=AuditRecord(

            audit_id=str(uuid.uuid4()),

            user_id=user_id,

            action=action,

            endpoint=endpoint,

            timestamp=datetime.utcnow(),

            audit_metadata=metadata

        )

        db.add(record)

        db.commit()