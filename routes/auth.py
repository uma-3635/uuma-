import re

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from ..auth import create_access_token
from ..auth import hash_password
from ..auth import verify_password

from ..database import create_user
from ..database import get_user_by_email

from ..dependencies import get_current_user

from ..schemas import LoginRequest
from ..schemas import RegisterRequest


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


def validate_email(email: str) -> bool:

    return bool(
        re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email
        )
    )


@router.post("/register")
def register(
    payload: RegisterRequest,
    response: Response
):

    email = payload.email.lower().strip()

    if not validate_email(email):

        raise HTTPException(
            status_code=400,
            detail="Enter a valid email address."
        )

    if get_user_by_email(email):

        raise HTTPException(
            status_code=409,
            detail=(
                "An account with this email "
                "already exists."
            )
        )

    user = create_user(
        payload.name.strip(),
        email,
        hash_password(payload.password)
    )

    token = create_access_token(
        user["id"]
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {
        "message": "Registration successful.",
        "user": user
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response
):

    user = get_user_by_email(
        payload.email
    )

    if (
        not user
        or
        not verify_password(
            payload.password,
            user["password_hash"]
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_access_token(
        user["id"]
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out."
    }


@router.get("/session-info")
def session_info(
    user=Depends(get_current_user)
):

    return {
        "logged_in": True,
        "user": user
    }


@router.get("/session-data")
def session_data(
    user=Depends(get_current_user)
):

    return {
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "personalization": {
            "currency": "INR"
        }
    }