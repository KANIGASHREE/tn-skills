from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import create_access_token
from ..dependencies import get_password_hash
from ..dependencies import verify_password
from ..dependencies import current_user

from ..models.user import User

from ..schemas import RegisterRequest
from ..schemas import LoginRequest
from ..schemas import TokenResponse


router = APIRouter(
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=201
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    email = payload.email.strip().lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    user = User(
        email=email,
        full_name=payload.full_name.strip(),
        password_hash=get_password_hash(
            payload.password
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user_id": user.id
    }


@router.post(
    "/token",
    response_model=TokenResponse
)
def token(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email ==
            payload.email.strip().lower()
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    return {
        "access_token":
            create_access_token(user.id),

        "token_type":
            "bearer"
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    return token(payload, db)


@router.post("/logout")
def logout(
    user=Depends(current_user)
):

    return {
        "message":
            "Logout acknowledged. Remove the JWT client-side."
    }


@router.get("/session-info")
def session_info(
    user=Depends(current_user)
):

    return {
        "logged_in": True,
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }


@router.get("/session-data")
def session_data(
    user=Depends(current_user)
):

    return {
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }