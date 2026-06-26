from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, Header
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET") 
print("SECRET LOADED:", JWT_SECRET)
 # move to env later
ALGO = "HS256"

if not JWT_SECRET:
    raise RuntimeError("SECRET_KEY not set in environment")

DEMO_USER = {
    "username": os.getenv("DEMO_USER"),
    "password": os.getenv("DEMO_PASSWORD")
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

def get_current_user(authorization: str = Header(None)):

    # Skip auth completely in demo mode
    if os.getenv("DEMO_MODE", "true").lower() == "true":
        return {"username": "demo-user"}

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth")

    token = authorization.split(" ")[1]
    return verify_token(token)
