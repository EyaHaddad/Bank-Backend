"""Account schemas - Pydantic models for request/response."""

from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum


class AccountType(str, Enum):
    """Enum for account type."""
    COURANT = "COURANT"   # Compte courant
    EPARGNE = "EPARGNE"   # Compte épargne


class AccountBase(BaseModel):
    """Base schema for account data."""
    pass  # Currency is always TND, no need to specify


class AccountCreate(AccountBase):
    """Schema for creating a new account."""
    initial_balance: float = Field(default=0.0, ge=0, description="Initial balance for the account")
    account_type: AccountType = Field(default=AccountType.COURANT, description="Account type (COURANT or EPARGNE)")


class AccountUpdate(BaseModel):
    """Schema for updating an account - currently no fields can be updated."""
    pass  # No updateable fields - currency is always TND


class AccountResponse(AccountBase):
    """Schema for account response."""
    id: UUID
    user_id: UUID
    balance: float
    currency: str = Field(default="TND", description="Currency code (always TND)")
    account_type: str = Field(default="COURANT", description="Account type (COURANT or EPARGNE)")
    status: str = Field(default="ACTIVE", description="Account status")

    model_config = {
        "from_attributes": True
    }


# NOTE: DepositRequest and WithdrawRequest have been removed.
# Clients cannot directly deposit/withdraw money.


class TransferRequest(BaseModel):
    """Schema for transfer request between the client's own accounts."""
    target_account_id: UUID = Field(..., description="Target account ID for the transfer (must be owned by same user)")
    amount: float = Field(..., gt=0, description="Amount to transfer (must be positive)")


class BalanceResponse(BaseModel):
    """Schema for balance response."""
    account_id: UUID
    balance: float
    currency: str = Field(default="TND", description="Currency code (always TND)")
