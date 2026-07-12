"""
app/schemas/auth.py
===================

Pydantic schemas used for authentication.

These schemas validate incoming requests and define
the structure of responses returned by the API.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------
# User Registration Request
# ---------------------------------------------------------------------

class UserRegister(BaseModel):
    """
    Schema used when a new user registers.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        description="Plain-text password",
    )


# ---------------------------------------------------------------------
# User Login Request
# ---------------------------------------------------------------------

class UserLogin(BaseModel):
    """
    Schema used when an existing user logs in.
    """

    email: EmailStr
    password: str


# ---------------------------------------------------------------------
# JWT Response
# ---------------------------------------------------------------------

class Token(BaseModel):
    """
    Returned after successful login.
    """

    access_token: str
    token_type: str


# ---------------------------------------------------------------------
# JWT Payload
# ---------------------------------------------------------------------

class TokenData(BaseModel):
    """
    Data extracted from a decoded JWT.
    """

    user_id: int
    role: str


# ---------------------------------------------------------------------
# User Response
# ---------------------------------------------------------------------

class UserResponse(BaseModel):
    """
    Public information returned about a user.
    """

    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)