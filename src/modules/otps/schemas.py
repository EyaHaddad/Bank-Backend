"""OTP schemas module for request/response validation."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from src.models.otp import OTPPurpose


class OTPGenerateRequest(BaseModel):
    """Schema for OTP generation request."""
    purpose: OTPPurpose = Field(..., description="Purpose of the OTP")


class OTPVerifyRequest(BaseModel):
    """Schema for OTP verification request."""
    code: str = Field(..., min_length=6, max_length=6, description="OTP code to verify")
    purpose: OTPPurpose = Field(..., description="Purpose of the OTP")


class OTPResponse(BaseModel):
    """Schema for OTP response."""
    id: UUID
    purpose: OTPPurpose
    expires_at: datetime
    is_used: bool
    attempts: int
    max_attempts: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class OTPVerifyResponse(BaseModel):
    """Schema for OTP verification response."""
    success: bool
    message: str


class OTPGenerateResponse(BaseModel):
    """Schema for OTP generation response."""
    message: str
    expires_at: datetime
    purpose: OTPPurpose
