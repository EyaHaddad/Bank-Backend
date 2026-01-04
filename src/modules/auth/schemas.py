"""Authentication schemas - Pydantic models for request/response."""

from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from src.models.user import Role


class RegisterUserRequest(BaseModel):
    """Model for user registration request."""
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    role: Role = Role.USER
    password: str
    confirm_password: str


class VerifyEmailRequest(BaseModel):
    """Model for email verification OTP request."""
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")


class VerifyEmailResponse(BaseModel):
    """Model for email verification response."""
    success: bool
    message: str


class ResendOTPRequest(BaseModel):
    """Model for resending OTP request."""
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    """Model for forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Model for reset password with OTP request."""
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")
    new_password: str = Field(..., min_length=12, description="New password (min 12 chars)")
    confirm_password: str = Field(..., min_length=12, description="Confirm new password")


class ResetPasswordResponse(BaseModel):
    """Model for reset password response."""
    success: bool
    message: str


class LoginUserRequest(BaseModel):
    """Model for user login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Model for token response."""
    access_token: str
    token_type: str = "bearer"
    role: str


class TokenData(BaseModel):
    """Model for token data."""
    user_id: str | None = None
    role: str | None = None

    def get_uuid(self) -> UUID | None:
        """Convert user_id string to UUID object."""
        if self.user_id:
            return UUID(self.user_id)
        return None

    def is_admin(self) -> bool:
        """Check if the user has admin role."""
        return self.role == "admin"
