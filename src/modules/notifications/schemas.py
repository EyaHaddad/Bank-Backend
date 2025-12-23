"""Notification schemas - Pydantic models for request/response."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationTypeEnum(str, Enum):
    """Enum for notification types."""
    EMAIL = "EMAIL"


class NotificationCategory(str, Enum):
    """Enum for notification categories."""
    OTP = "OTP"
    TRANSACTION = "TRANSACTION"
    NEWS = "NEWS"


# ==================== Request Schemas ====================


class NotificationBase(BaseModel):
    """Base schema for notification data."""
    title: str = Field(..., min_length=1, max_length=255, description="Notification title")
    content: str = Field(..., min_length=1, description="Notification content")


class SendOTPNotificationRequest(BaseModel):
    """Schema for sending OTP notification."""
    user_id: UUID = Field(..., description="User ID to send OTP to")
    otp_code: str = Field(..., min_length=4, max_length=10, description="OTP code to send")


class SendTransactionNotificationRequest(BaseModel):
    """Schema for sending transaction notification."""
    user_id: UUID = Field(..., description="User ID to notify")
    transaction_type: str = Field(..., description="Type of transaction (credit/debit)")
    amount: float = Field(..., gt=0, description="Transaction amount")
    account_number: Optional[str] = Field(None, description="Account number involved")
    reference: Optional[str] = Field(None, description="Transaction reference")


class SendBankNewsNotificationRequest(BaseModel):
    """Schema for sending bank news notification to a user or all users."""
    user_id: Optional[UUID] = Field(None, description="User ID to notify (if None, notify all users)")
    title: str = Field(..., min_length=1, max_length=255, description="News title")
    content: str = Field(..., min_length=1, description="News content")


class CreateNotificationRequest(NotificationBase):
    """Schema for creating a custom notification."""
    user_id: UUID = Field(..., description="User ID to send notification to")
    category: NotificationCategory = Field(
        NotificationCategory.NEWS, 
        description="Notification category"
    )


# ==================== Response Schemas ====================


class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    id: UUID
    type: NotificationTypeEnum
    user_id: UUID
    sent_at: datetime

    model_config = {
        "from_attributes": True
    }


class NotificationListResponse(BaseModel):
    """Schema for paginated notification list response."""
    notifications: list[NotificationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class NotificationSentResponse(BaseModel):
    """Schema for notification sent confirmation."""
    success: bool = True
    message: str = "Notification sent successfully"
    notification_id: Optional[UUID] = None


class BulkNotificationSentResponse(BaseModel):
    """Schema for bulk notification sent confirmation."""
    success: bool = True
    message: str = "Notifications sent successfully"
    total_sent: int = 0
    failed: int = 0
