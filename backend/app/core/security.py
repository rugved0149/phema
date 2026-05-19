from jose import jwt,JWTError
from datetime import datetime,timedelta
from passlib.context import CryptContext


SECRET_KEY="phema_secret_key"
ALGORITHM="HS256"

ACCESS_TOKEN_MINUTES=120
REFRESH_TOKEN_DAYS=7


pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password:str):

    safe_password=password[:72]

    return pwd_context.hash(
        safe_password
    )


def verify_password(
    plain_password:str,
    hashed_password:str
):

    safe_password=plain_password[:72]

    return pwd_context.verify(
        safe_password,
        hashed_password
    )


def create_access_token(data:dict):

    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(
        minutes=ACCESS_TOKEN_MINUTES
    )

    to_encode.update({
        "exp":expire,
        "type":"access"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(data:dict):

    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(
        days=REFRESH_TOKEN_DAYS
    )

    to_encode.update({
        "exp":expire,
        "type":"refresh"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token:str):

    try:

        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None