from fastapi import APIRouter
from datetime import datetime,timedelta

from app.db.base import SessionLocal
from app.db.session import UserRecord,OTPRecord

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)

from app.core.otp_utils import generate_otp
from app.core.email_sender import send_otp_email

import uuid

router=APIRouter(prefix="/auth")

ADMIN_EMAIL="rugved0149@gmail.com"

OTP_EXPIRY_MINUTES=5


@router.post("/register")

def register_user(
    email:str,
    username:str,
    password:str
):

    otp=generate_otp()

    send_otp_email(
        email,
        otp
    )

    with SessionLocal() as db:

        existing_user=(
            db.query(UserRecord)
            .filter(
                (UserRecord.email==email) |
                (UserRecord.username==username)
            )
            .first()
        )

        if existing_user:

            return{
                "status":"user_exists"
            }

        record=OTPRecord(
            otp_id=str(uuid.uuid4()),
            email=email,
            otp_code=otp,
            created_at=datetime.utcnow()
        )

        db.add(record)
        db.commit()

    return{
        "status":"otp_sent"
    }


@router.post("/verify")

def verify_otp(
    email:str,
    username:str,
    password:str,
    otp:str
):

    with SessionLocal() as db:

        record=(
            db.query(OTPRecord)
            .filter(
                OTPRecord.email==email,
                OTPRecord.otp_code==otp
            )
            .first()
        )

        if not record:

            return{
                "status":"invalid_otp"
            }

        expiry_time=record.created_at + timedelta(
            minutes=OTP_EXPIRY_MINUTES
        )

        if datetime.utcnow() > expiry_time:

            db.delete(record)
            db.commit()

            return{
                "status":"otp_expired"
            }

        role="admin" if email==ADMIN_EMAIL else "user"

        user=UserRecord(
            user_id=str(uuid.uuid4()),
            email=email,
            username=username,
            password_hash=hash_password(password),
            role=role,
            is_verified="true"
        )

        db.add(user)

        db.delete(record)

        db.commit()

    return{
        "status":"user_created"
    }


@router.post("/login")

def login_user(
    username:str,
    password:str
):

    with SessionLocal() as db:

        user=(
            db.query(UserRecord)
            .filter(
                UserRecord.username==username
            )
            .first()
        )

        if not user:

            return{
                "status":"user_not_found"
            }

        if user.is_verified!="true":

            return{
                "status":"email_not_verified"
            }

        if not verify_password(
            password,
            user.password_hash
        ):

            return{
                "status":"invalid_password"
            }

        # AUTO ADMIN PROMOTION (safety)
        if user.email==ADMIN_EMAIL:

            if user.role!="admin":

                user.role="admin"
                db.commit()

        token=create_access_token({
            "sub":user.user_id,
            "role":user.role
        })

        return{
            "access_token":token,
            "token_type":"bearer",
            "user_id":user.user_id,
            "role":user.role
        }