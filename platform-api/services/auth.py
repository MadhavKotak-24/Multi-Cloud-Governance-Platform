from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, Header
import os
JWT_SECRET = os.getenv("JWT_SECRET") 
print("SECRET LOADED:", JWT_SECRET)
 # move to env later
ALGO = "HS256"

if not JWT_SECRET:
    raise RuntimeError("SECRET_KEY not set in environment")

DEMO_USER = {
    "username": "admin",
    "password": "admin123"
}

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=4)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def verify_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(auth: str = Header(None)):
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth")

    token = auth.split(" ")[1]
    verify_token(token)
