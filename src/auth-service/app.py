from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

# NOTE: In a real system this key must be managed securely.
JWT_SECRET = "lab-secret-key"
JWT_ALG = "HS256"
JWT_EXP_MINUTES = 60

app = FastAPI(title="auth-service")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Very small in-memory user store for the lab.
USERS = {
    "alice": {"password": "password123", "user_id": 1001, "role": "user"},
    "bob": {"password": "hunter2", "user_id": 1002, "role": "user"},
}


@app.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    user = USERS.get(body.username)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    now = datetime.utcnow()
    payload = {
        "sub": str(user["user_id"]),
        "username": body.username,
        "role": user["role"],
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXP_MINUTES)).timestamp()),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
    return TokenResponse(access_token=token)


@app.get("/health")
async def health():
    return {"status": "ok"}
