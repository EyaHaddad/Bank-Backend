"""Notification router - API endpoints for notification operations."""

from uuid import UUID
import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.modules.auth.service import CurrentUser, AdminUser
from src.infrastructure.database import get_db

from .schemas import (
    NotificationResponse,
    NotificationListResponse,
    NotificationSentResponse,
    BulkNotificationSentResponse,
    SendOTPNotificationRequest,
    SendTransactionNotificationRequest,
    SendBankNewsNotificationRequest,
    CreateNotificationRequest,
)
from .service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ==================== User Endpoints ====================


@router.get("/", response_model=NotificationListResponse)
def get_my_notifications(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
):
    """Get all notifications for the current authenticated user."""
    service = NotificationService(db)
    notifications, total = service.get_user_notifications(
        user_id=UUID(current_user.user_id),
        page=page,
        page_size=page_size,
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return NotificationListResponse(
        notifications=[NotificationResponse.model_validate(n) for n in notifications],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Get a specific notification by ID."""
    service = NotificationService(db)
    notification = service.get_notification_by_id(notification_id)
    
    # Ensure user can only access their own notifications
    if str(notification.user_id) != current_user.user_id:
        from .exceptions import NotificationNotFoundError
        raise NotificationNotFoundError(notification_id)
    
    return NotificationResponse.model_validate(notification)


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Delete a specific notification."""
    service = NotificationService(db)
    service.delete_notification(
        notification_id=notification_id,
        user_id=UUID(current_user.user_id),
    )
    return {"message": "Notification deleted successfully"}


# ==================== Internal/Admin Endpoints ====================
# These endpoints are protected with admin authentication


@router.post("/send/otp", response_model=NotificationSentResponse)
def send_otp_notification(
    request: SendOTPNotificationRequest,
    current_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Send an OTP notification via email. Admin only.
    
    Note: This endpoint is typically called internally by the OTP service.
    """
    service = NotificationService(db)
    notification = service.send_otp_notification(request)
    
    return NotificationSentResponse(
        success=True,
        message="OTP notification sent successfully",
        notification_id=notification.id,
    )


@router.post("/send/transaction", response_model=NotificationSentResponse)
def send_transaction_notification(
    request: SendTransactionNotificationRequest,
    current_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Send a transaction notification via email. Admin only.
    
    Note: This endpoint is typically called internally by the transaction service.
    """
    service = NotificationService(db)
    notification = service.send_transaction_notification(request)
    
    return NotificationSentResponse(
        success=True,
        message="Transaction notification sent successfully",
        notification_id=notification.id,
    )


@router.post("/send/news", response_model=BulkNotificationSentResponse)
def send_bank_news_notification(
    request: SendBankNewsNotificationRequest,
    current_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Send a bank news notification. Admin only.
    
    - If user_id is provided, sends to that specific user.
    - If user_id is None, sends to all active users.
    """
    service = NotificationService(db)
    notifications = service.send_bank_news_notification(request)
    
    return BulkNotificationSentResponse(
        success=True,
        message=f"Bank news notification sent to {len(notifications)} user(s)",
        total_sent=len(notifications),
        failed=0,
    )


@router.post("/send/custom", response_model=NotificationSentResponse)
def send_custom_notification(
    request: CreateNotificationRequest,
    current_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Send a custom notification to a user. Admin only.
    """
    service = NotificationService(db)
    notification = service.create_notification(request)
    
    return NotificationSentResponse(
        success=True,
        message="Custom notification sent successfully",
        notification_id=notification.id,
    )


# ==================== Admin Endpoints ====================


@router.get("/user/{user_id}", response_model=NotificationListResponse)
def get_user_notifications_admin(
    user_id: UUID,
    current_user: AdminUser,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
):
    """
    Get all notifications for a specific user. Admin only.
    """
    service = NotificationService(db)
    notifications, total = service.get_user_notifications(
        user_id=user_id,
        page=page,
        page_size=page_size,
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return NotificationListResponse(
        notifications=[NotificationResponse.model_validate(n) for n in notifications],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
