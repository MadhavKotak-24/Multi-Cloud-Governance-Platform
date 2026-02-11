from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, Header

SECRET = "super-secret-key"  # move to env later
ALGO = "HS256"

DEMO_USER = {
    "username": "admin",
    "password": "admin123"
}

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=4)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def verify_token(token: str):
    try:
        jwt.decode(token, SECRET, algorithms=[ALGO])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(auth: str = Header(None)):
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth")

    token = auth.split(" ")[1]
    verify_token(token)
