"""
app/routers/auth.py
===================

Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.core.database import get_db
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
)
from app.services.auth_service import (
    register_user,
    login_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    try:
        return register_user(db, user_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT.
    """

    try:

        token = login_user(
            db,
            login_data,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """

    return current_user

def require_role(*allowed_roles: str):
    """
    Factory function that creates a dependency to enforce roles.
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker    

from app.dependencies.auth import (
    require_admin,
    require_operator,
    require_viewer,
)    

@router.get("/admin")
def admin_dashboard(
    current_user: User = Depends(require_admin),
):
    return {
        "message": f"Welcome Admin {current_user.username}"
    }


@router.get("/operator")
def operator_dashboard(
    current_user: User = Depends(require_operator),
):
    return {
        "message": f"Welcome Operator {current_user.username}"
    }


@router.get("/viewer")
def viewer_dashboard(
    current_user: User = Depends(require_viewer),
):
    return {
        "message": f"Welcome Viewer {current_user.username}"
    }