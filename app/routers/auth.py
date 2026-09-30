import secrets
import time

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from ..auth import hash_password, verify_password
from ..database import (
    create_session,
    create_user,
    delete_session,
    get_user_by_email,
)
from ..dependencies import get_current_user
from ..models import UserCreate, UserLogin


router = APIRouter(prefix="/api/auth", tags=["Authentication"])
SESSION_COOKIE = "access_token"
SESSION_LIFETIME = 60 * 60 * 24 * 7


def _set_session_cookie(response: Response, user_id: int) -> None:
    token = secrets.token_urlsafe(32)
    create_session(token, user_id, int(time.time()) + SESSION_LIFETIME)
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=SESSION_LIFETIME,
        httponly=True,
        samesite="lax",
    )


@router.post("/register", status_code=201)
def register(payload: UserCreate, response: Response) -> dict:
    user = create_user(
        payload.username.strip(),
        str(payload.email).lower().strip(),
        hash_password(payload.password),
    )
    if user is None:
        raise HTTPException(status_code=409, detail="Email is already registered.")
    _set_session_cookie(response, user["id"])
    return {"message": "Registration successful.", "user": user}


@router.post("/login")
def login(payload: UserLogin, response: Response) -> dict:
    user = get_user_by_email(str(payload.email).lower().strip())
    if user is None or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    _set_session_cookie(response, user["id"])
    return {
        "message": "Login successful.",
        "user": {"id": user["id"], "username": user["username"], "email": user["email"]},
    }


@router.post("/logout")
def logout(request: Request, response: Response) -> dict:
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        delete_session(token)
    response.delete_cookie(SESSION_COOKIE, httponly=True, samesite="lax")
    return {"message": "Logged out."}


@router.get("/session-info")
def session_info(user: dict = Depends(get_current_user)) -> dict:
    return {
        "logged_in": True,
        "user_id": user["id"],
        "username": user["username"],
        "email": user["email"],
    }


@router.get("/session-data")
def session_data(user: dict = Depends(get_current_user)) -> dict:
    return {
        "user_id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "personalization": {"currency": "INR"},
    }