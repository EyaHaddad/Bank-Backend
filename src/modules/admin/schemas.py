"""Admin schemas - Pydantic models for request/response."""

from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AccountType(str, Enum):
    """Enum for account type."""
    COURANT = "COURANT"
    EPARGNE = "EPARGNE"


class PromoteUserRequest(BaseModel):
    """Model for promoting a user to admin."""
    user_id: UUID


class PromoteUserResponse(BaseModel):
    """Model for promote user response."""
    message: str
    user_id: UUID
    new_role: str


class AdminAccountCreate(BaseModel):
    """Model for admin creating an account for a user."""
    user_id: UUID = Field(..., description="ID of the user to create account for")
    initial_balance: float = Field(default=0.0, ge=0, description="Initial balance for the account")
    account_type: AccountType = Field(default=AccountType.COURANT, description="Account type (COURANT or EPARGNE)")


class AdminAccountResponse(BaseModel):
    """Model for admin account list response with user info."""
    id: UUID
    user_id: UUID
    user_name: str
    user_email: str
    balance: float
    currency: str
    account_type: str = "COURANT"
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
