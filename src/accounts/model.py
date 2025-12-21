"""Account models module for request/response schemas."""

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class AccountBase(BaseModel):
    """Base schema for account data."""
    currency: str = Field(default="TND", description="Currency code (e.g., TND, EUR, USD)")


class AccountCreate(AccountBase):
    """Schema for creating a new account."""
    initial_balance: float = Field(default=0.0, ge=0, description="Initial balance for the account")


class AccountUpdate(BaseModel):
    """Schema for updating an account."""
    currency: Optional[str] = Field(default=None, description="New currency code")


class AccountResponse(AccountBase):
    """Schema for account response."""
    id: UUID
    user_id: UUID
    balance: float

    class Config:
        from_attributes = True
        orm_mode = True


class DepositRequest(BaseModel):
    """Schema for deposit request."""
    amount: float = Field(..., gt=0, description="Amount to deposit (must be positive)")


class WithdrawRequest(BaseModel):
    """Schema for withdrawal request."""
    amount: float = Field(..., gt=0, description="Amount to withdraw (must be positive)")


class TransferRequest(BaseModel):
    """Schema for transfer request between accounts."""
    target_account_id: UUID = Field(..., description="Target account ID for the transfer")
    amount: float = Field(..., gt=0, description="Amount to transfer (must be positive)")


class BalanceResponse(BaseModel):
    """Schema for balance response."""
    account_id: UUID
    balance: float
    currency: str
