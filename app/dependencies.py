from fastapi import HTTPException, Request

from .database import get_user_by_session


def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    user = get_user_by_session(token) if token else None
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required.")
    return user