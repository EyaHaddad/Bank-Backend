"""Admin schemas - Pydantic models for request/response."""

from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PromoteUserRequest(BaseModel):
    """Model for promoting a user to admin."""
    user_id: UUID


class PromoteUserResponse(BaseModel):
    """Model for promote user response."""
    message: str
    user_id: UUID
    new_role: str


class AdminAccountResponse(BaseModel):
    """Model for admin account list response with user info."""
    id: UUID
    user_id: UUID
    user_name: str
    user_email: str
    balance: float
    currency: str
    status: str = "ACTIVE"

    class Config:
        from_attributes = True


class AdminUserResponse(BaseModel):
    """Model for admin user response."""
    id: UUID
    firstname: str
    lastname: str
    email: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserStatusResponse(BaseModel):
    """Model for user status change response."""
    message: str
    user_id: UUID
    is_active: bool


class AccountStatusResponse(BaseModel):
    """Model for account status change response."""
    message: str
    account_id: UUID
    status: str


class AccountBalanceUpdate(BaseModel):
    """Model for updating account balance."""
    new_balance: float


class AdminUserUpdate(BaseModel):
    """Model for admin updating a user."""
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
