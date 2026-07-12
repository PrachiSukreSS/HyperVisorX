"""
app/services/auth_service.py
============================

Business logic for authentication.

Responsibilities:
- Register new users
- Authenticate existing users
- Generate JWT tokens
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def register_user(db: Session, user_data: UserRegister) -> User:
    """
    Register a new user.
    """

    # Check username
    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username:
        raise ValueError("Username already exists.")

    # Check email
    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise ValueError("Email already exists.")

    # Create new user
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="viewer",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    login_data: UserLogin,
) -> User | None:
    """
    Verify email and password.
    """

    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if user is None:
        return None

    if not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        return None

    return user


def login_user(
    db: Session,
    login_data: UserLogin,
) -> str:
    """
    Authenticate the user and return a JWT.
    """

    user = authenticate_user(db, login_data)

    if user is None:
        raise ValueError("Invalid email or password.")

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return token