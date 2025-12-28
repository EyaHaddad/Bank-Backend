"""Notifications module exports."""

from .router import router
from .service import (
    NotificationService,
    send_otp_notification_helper,
    send_transaction_notification_helper,
    send_welcome_notification_helper,
    send_email_verification_notification_helper,
    send_email_verification_otp,
    send_password_change_notification_helper,
    send_login_otp_notification_helper,
    send_transaction_otp_notification_helper,
    send_password_reset_otp_notification_helper,
)
from .schemas import (
    NotificationTypeEnum,
    NotificationCategory,
    NotificationBase,
    SendOTPNotificationRequest,
    SendTransactionNotificationRequest,
    SendBankNewsNotificationRequest,
    CreateNotificationRequest,
    NotificationResponse,
    NotificationListResponse,
    NotificationSentResponse,
    BulkNotificationSentResponse,
)
from .exceptions import (
    NotificationError,
    NotificationNotFoundError,
    NotificationSendError,
    InvalidNotificationTypeError,
    UserNotFoundForNotificationError,
)

__all__ = [
    # Router
    "router",
    # Service
    "NotificationService",
    "send_otp_notification_helper",
    "send_transaction_notification_helper",
    "send_welcome_notification_helper",
    "send_email_verification_notification_helper",
    "send_password_change_notification_helper",
    "send_login_otp_notification_helper",
    "send_transaction_otp_notification_helper",
    "send_password_reset_otp_notification_helper",
    # Schemas
    "NotificationTypeEnum",
    "NotificationCategory",
    "NotificationBase",
    "SendOTPNotificationRequest",
    "SendTransactionNotificationRequest",
    "SendBankNewsNotificationRequest",
    "CreateNotificationRequest",
    "NotificationResponse",
    "NotificationListResponse",
    "NotificationSentResponse",
    "BulkNotificationSentResponse",
    # Exceptions
    "NotificationError",
    "NotificationNotFoundError",
    "NotificationSendError",
    "InvalidNotificationTypeError",
    "UserNotFoundForNotificationError",
]
