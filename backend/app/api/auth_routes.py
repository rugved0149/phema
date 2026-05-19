from fastapi import APIRouter
from app.core.rate_limiter import limiter
from fastapi import Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.token_blacklist import revoke_token
from datetime import datetime,timedelta
from app.db.base import SessionLocal
from app.db.session import UserRecord,OTPRecord
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token
)
from app.core.otp_utils import generate_otp
from app.core.email_sender import send_otp_email

import uuid
import re

router=APIRouter(prefix="/auth")

security=HTTPBearer()

ADMIN_EMAIL="rugved0149@gmail.com"

OTP_EXPIRY_MINUTES=5


def validate_password(password:str):

    if len(password)<8:
        return "Password must be at least 8 characters"

    if not re.search(r"[A-Z]",password):
        return "Password must contain uppercase letter"

    if not re.search(r"[a-z]",password):
        return "Password must contain lowercase letter"

    if not re.search(r"[0-9]",password):
        return "Password must contain number"

    if not re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/]",password):
        return "Password must contain special symbol"

    return None


@router.post("/register")
@limiter.limit("5/minute")
def register_user(
    request: Request,
    email:str,
    username:str,
    password:str
):

    password_error=validate_password(password)

    if password_error:

        return{
            "status":"weak_password",
            "message":password_error
        }

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

        db.query(OTPRecord).filter(
            OTPRecord.email==email
        ).delete()

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
@limiter.limit("10/minute")
def verify_otp(
    request: Request,
    email:str,
    username:str,
    password:str,
    otp:str
):

    password_error=validate_password(password)

    if password_error:

        return{
            "status":"weak_password",
            "message":password_error
        }

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

        safe_password=password[:72]

        user=UserRecord(
            user_id=str(uuid.uuid4()),
            email=email,
            username=username,
            password_hash=hash_password(safe_password),
            role=role,
            is_verified="true",
            failed_attempts=0,
            lock_until=None
        )

        db.add(user)

        db.delete(record)

        db.commit()

    return{
        "status":"user_created"
    }


@router.post("/refresh")
@limiter.limit("10/minute")
def refresh_access_token(
    request:Request,
    refresh_token:str
):

    payload=verify_token(refresh_token)

    if not payload:

        return{
            "status":"invalid_refresh"
        }

    if payload.get("type")!="refresh":

        return{
            "status":"invalid_token_type"
        }

    user_id=payload.get("sub")
    role=payload.get("role")

    new_access=create_access_token({

        "sub":user_id,

        "role":role

    })

    return{

        "access_token":new_access,

        "token_type":"bearer"

    }

@router.post("/logout")
def logout_user(

    credentials:
        HTTPAuthorizationCredentials
        =Depends(security)

):

    token=credentials.credentials

    payload=verify_token(token)

    if not payload:

        return{
            "status":"invalid_token"
        }

    expiry_timestamp=payload.get("exp")

    expiry=datetime.utcfromtimestamp(
        expiry_timestamp
    )

    revoke_token(
        token,
        expiry
    )

    return{
        "status":"logged_out"
    }

@router.post("/login")
@limiter.limit("10/minute")
def login_user(
    request: Request,
    username:str,
    password:str
):

    MAX_ATTEMPTS=5
    LOCK_MINUTES=10

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

        if user.lock_until:

            if datetime.utcnow() < user.lock_until:

                return{
                    "status":"account_locked"
                }

            else:

                user.lock_until=None
                user.failed_attempts=0
                db.commit()

        safe_password=password[:72]

        if not verify_password(
            safe_password,
            user.password_hash
        ):

            user.failed_attempts+=1

            if user.failed_attempts>=MAX_ATTEMPTS:

                user.lock_until=(
                    datetime.utcnow()
                    + timedelta(minutes=LOCK_MINUTES)
                )

                db.commit()

                return{
                    "status":"account_locked"
                }

            db.commit()

            return{
                "status":"invalid_password"
            }

        user.failed_attempts=0
        user.lock_until=None

        if user.email==ADMIN_EMAIL:

            if user.role!="admin":

                user.role="admin"

        db.commit()

        access_token=create_access_token({
            "sub":user.user_id,
            "role":user.role
        })

        refresh_token=create_refresh_token({
            "sub":user.user_id
        })

        return{
            "access_token":access_token,
            "refresh_token":refresh_token,
            "token_type":"bearer",
            "user_id":user.user_id,
            "role":user.role
        }