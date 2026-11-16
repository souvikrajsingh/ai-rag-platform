import hashlib
from typing import Any

from fastapi import HTTPException, Request, status


def get_session_user(request: Request) -> dict[str, Any] | None:
    user = request.session.get("user")
    if (
        isinstance(user, dict)
        and isinstance(user.get("sub"), str)
        and user["sub"]
    ):
        return user
    return None


def require_authenticated_user(request: Request) -> dict[str, Any]:
    user = get_session_user(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sign in is required.",
        )
    return user


def namespace_for_user(user_sub: str) -> str:
    user_hash = hashlib.sha256(user_sub.encode("utf-8")).hexdigest()
    return f"user-{user_hash}"
