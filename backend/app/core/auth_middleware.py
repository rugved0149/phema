from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.token_blacklist import is_token_revoked
from jose import jwt, JWTError

SECRET_KEY="phema_secret_key"
ALGORITHM="HS256"

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

security=HTTPBearer()

def get_current_user(
    credentials:HTTPAuthorizationCredentials
        =Depends(security)
):

    token=credentials.credentials

    if is_token_revoked(token):

        raise HTTPException(
            status_code=401,
            detail="Token revoked"
        )

    payload=verify_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload

def get_admin_user(
    user=Depends(get_current_user)
):

    if user.get("role")!="admin":

        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )

    return user