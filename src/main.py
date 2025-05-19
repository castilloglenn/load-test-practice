from fastapi import FastAPI, HTTPException, Depends, status, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
import secrets

app = FastAPI()

# In-memory "database"
users_db = {
    "alice": {"username": "alice", "password": "wonderland"},
    "bob": {"username": "bob", "password": "builder"},
}

# In-memory session store
sessions = {}

SESSION_COOKIE = "session_token"


def get_current_user(session_token: Optional[str] = Cookie(None)):
    if session_token and session_token in sessions:
        return sessions[session_token]
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    session_token = secrets.token_hex(16)
    sessions[session_token] = user["username"]
    response = JSONResponse(content={"message": "Logged in"})
    response.set_cookie(key=SESSION_COOKIE, value=session_token, httponly=True)
    return response


@app.post("/logout")
def logout(session_token: Optional[str] = Cookie(None)):
    if session_token and session_token in sessions:
        sessions.pop(session_token)
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(SESSION_COOKIE)
    return response


@app.get("/status")
def status_check(user: str = Depends(get_current_user)):
    return {"status": "ok", "user": user}


@app.get("/profile")
def profile(user: str = Depends(get_current_user)):
    return {"username": user, "bio": "This is a sample profile."}
