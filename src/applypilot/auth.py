"""JWT and password utilities for ApplyPilot authentication."""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

_SECRET = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-production")
_ALGO = "HS256"
_EXPIRE_DAYS = 30


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_token(user_id: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=_EXPIRE_DAYS)
    return jwt.encode({"sub": user_id, "exp": exp}, _SECRET, algorithm=_ALGO)


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, _SECRET, algorithms=[_ALGO])
        return payload.get("sub")
    except JWTError:
        return None
