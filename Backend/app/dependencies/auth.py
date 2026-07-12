"""
Authentication dependencies.

These functions are reused by protected endpoints
to verify JWT tokens and retrieve the current user.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_access_token
from app.models.user import User

# Bearer Authentication Scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate JWT token and return the authenticated user.
    """

    token = credentials.credentials

    try:
        payload = verify_access_token(token)

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = int(payload["sub"])

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

def require_role(*allowed_roles: str):
    """
    Dependency factory that allows only specific roles.
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

require_admin = require_role("admin")

require_operator = require_role(
    "operator",
    "admin",
)

require_viewer = require_role(
    "viewer",
    "operator",
    "admin",
)