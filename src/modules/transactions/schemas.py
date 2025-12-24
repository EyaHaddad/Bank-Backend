"""Transaction schemas - Pydantic models for request/response."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum


class TransactionTypeEnum(str, Enum):
    """Enum for transaction types."""
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    TRANSFER = "TRANSFER"


class TransactionStatusEnum(str, Enum):
    """Enum for transaction status."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransactionBase(BaseModel):
    """Base schema for transaction data."""
    amount: float = Field(..., gt=0, description="Transaction amount must be positive")
    reference: Optional[str] = Field(None, max_length=100, description="Transaction reference")


class CreditRequest(BaseModel):
    """Schema for credit (deposit) request."""
    account_id: UUID = Field(..., description="Account ID to credit")
    amount: float = Field(..., gt=0, description="Amount to credit")
    reference: Optional[str] = Field(None, max_length=100, description="Transaction reference")


class DebitRequest(BaseModel):
    """Schema for debit (withdrawal) request."""
    account_id: UUID = Field(..., description="Account ID to debit")
    amount: float = Field(..., gt=0, description="Amount to debit")
    reference: Optional[str] = Field(None, max_length=100, description="Transaction reference")


class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: UUID
    sender_account_id: UUID
    type: TransactionTypeEnum
    amount: float
    status: TransactionStatusEnum
    reference: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


class TransactionListResponse(BaseModel):
    """Schema for listing transactions."""
    transactions: list[TransactionResponse]
    total: int
    page: int
    page_size: int


class TransactionSummary(BaseModel):
    """Schema for transaction summary/statistics."""
    account_id: UUID
    total_credits: float
    total_debits: float
    total_transfers_sent: float
    transaction_count: int
    period_start: Optional[datetime]
    period_end: Optional[datetime]
