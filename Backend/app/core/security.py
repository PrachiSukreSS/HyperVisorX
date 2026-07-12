"""
app/core/security.py
====================

Security utilities for HyperVisorX.

Responsibilities:
- Hash user passwords
- Verify passwords
- Create JWT access tokens
- Decode and validate JWT tokens
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


# ---------------------------------------------------------------------
# Password Hashing Configuration
# ---------------------------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ---------------------------------------------------------------------
# Password Hashing Functions
# ---------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure bcrypt hash.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify whether a plain password matches its stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password) 

# ---------------------------------------------------------------------
# JWT Token Creation
# ---------------------------------------------------------------------

def create_access_token(data: dict[str, Any]) -> str:
    """
    Create a signed JWT access token.

    Args:
        data: Dictionary containing user information to include in the token.

    Returns:
        Encoded JWT string.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt

# ---------------------------------------------------------------------
# JWT Token Verification
# ---------------------------------------------------------------------

def verify_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Raises:
        jose.JWTError if the token is invalid or expired.
    """

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    return payload