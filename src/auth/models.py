"""Authentication Models"""

from uuid import UUID
from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    """Model for user registration request."""

    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str


class LoginUserRequest(BaseModel):
    """Model for user login request."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Model for token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Model for token data."""

    user_id:str | None = None
    def get_uuid(self) -> UUID | None:
        """Convert user_id string to UUID object."""
        if self.user_id :
            return UUID(self.user_id)
        return None
