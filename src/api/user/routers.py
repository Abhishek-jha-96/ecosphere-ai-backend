from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, Response
from firebase_admin import auth

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/auth/session")
def create_session(response: Response, id_token: str):
    try:
        expires_in = timedelta(days=7)
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        response.set_cookie(
            key="session",
            value=session_cookie,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=7 * 24 * 3600,
        )
        return {"message": "Session created"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase ID token")


@router.get("/me")
def get_me(request: Request):
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        raise HTTPException(status_code=401, detail="No session")
    try:
        decoded = auth.verify_session_cookie(session_cookie, check_revoked=True)
        return {"uid": decoded["sub"], "email": decoded.get("email")}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired session")


@router.post("/auth/logout")
def logout(response: Response, request: Request):
    session_cookie = request.cookies.get("session")
    if session_cookie:
        try:
            decoded = auth.verify_session_cookie(session_cookie)
            auth.revoke_refresh_tokens(decoded["sub"])
        except Exception:
            pass
    response.delete_cookie("session")
    return {"message": "Logged out"}
