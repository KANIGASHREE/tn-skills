from datetime import datetime
from datetime import timedelta
from datetime import timezone

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError
from jose import jwt

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models.user import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token"
)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed_password: str
):
    return pwd_context.verify(
        password,
        hashed_password
    )


def create_access_token(user_id: int):

    expire_time = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire_time
    }

    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm="HS256"
    )

    return token


def current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"]
        )

        user_id = int(
            payload.get("sub", "0")
        )

    except (
        JWTError,
        ValueError
    ):
        raise error

    user = db.get(User, user_id)

    if not user:
        raise error

    return user