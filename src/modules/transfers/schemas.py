"""Transfer schemas - Pydantic models for request/response."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum


class TransferStatusEnum(str, Enum):
    """Enum for transfer status."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransferRequest(BaseModel):
    """Schema for creating a new transfer."""
    sender_account_id: UUID = Field(..., description="Source account ID")
    beneficiary_id: UUID = Field(..., description="Beneficiary ID to transfer to")
    amount: float = Field(..., gt=0, description="Transfer amount must be positive")
    reference: Optional[str] = Field(None, max_length=100, description="Transfer reference/description")


class TransferResponse(BaseModel):
    """Schema for transfer response."""
    id: UUID
    sender_account_id: UUID
    beneficiary_id: UUID
    amount: float
    status: TransferStatusEnum
    reference: Optional[str]
    type: str = "TRANSFER"
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Beneficiary info (denormalized for convenience)
    beneficiary_name: Optional[str] = None
    beneficiary_iban: Optional[str] = None
    beneficiary_bank: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class TransferListResponse(BaseModel):
    """Schema for listing transfers."""
    transfers: list[TransferResponse]
    total: int
    page: int
    page_size: int


class TransferSummary(BaseModel):
    """Schema for transfer summary/statistics."""
    account_id: UUID
    total_sent: float
    transfer_count: int
    average_transfer: float
    period_start: Optional[datetime]
    period_end: Optional[datetime]


# Beneficiary schemas (used in transfers module)
class BeneficiaryBase(BaseModel):
    """Base schema for beneficiary data."""
    name: str = Field(..., min_length=2, max_length=100, description="Beneficiary name")
    bank_name: str = Field(..., min_length=2, max_length=100, description="Bank name")
    iban: str = Field(..., min_length=15, max_length=34, description="IBAN number")
    email: Optional[str] = Field(None, description="Beneficiary email for notifications")


class BeneficiaryCreate(BeneficiaryBase):
    """Schema for creating a new beneficiary."""
    pass


class BeneficiaryUpdate(BaseModel):
    """Schema for updating a beneficiary."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Beneficiary name")
    bank_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Bank name")
    email: Optional[str] = Field(None, description="Beneficiary email")


class BeneficiaryResponse(BeneficiaryBase):
    """Schema for beneficiary response."""
    id: UUID
    user_id: UUID
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


class BeneficiaryListResponse(BaseModel):
    """Schema for listing beneficiaries."""
    beneficiaries: list[BeneficiaryResponse]
    total: int
